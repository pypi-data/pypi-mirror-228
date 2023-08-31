import json
import ast

import click
import os, shutil
import re
import sys
import platform
import subprocess
from json import load as json_load
from datetime import datetime
from json import dumps as json_dumps

isWindows = platform.system() == 'Windows'

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

directories = {
    'main': '',
    'pipeline': '',
    'artifacts': '',
    'models': '',
    'vocabs': '',
    'other': '',
    'preprocessor': '',
    'predictables': '',
    'predictors': '',
    'forcers': '',
    'postprocessor': '',
    'schema': '',
    'tester': '',
    'test_schema': '',
    'trainer': '',
    'server': '',
    'dsp': '',
    'documentation': ''
}


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)

@click.group(cls=AliasedGroup)
@click.version_option(package_name='gaiaFramework')
def cli():
    """
    DS framework cli

    ** how to use **

    g = generate

    p = project

    create project

    gaia-cli g project my-new-project

    gaia-cli g p my-new-project

    gaia-cli generate project my-new-project

    gaia-cli generate p my-new-project

    cd my-new-project

    create forcer

    gaia-cli g forcer my-new-forcer

    create predictable

    gaia-cli g predictable my-new-predictable

    create tester files

    gaia-cli create-tester-files

    run server

    gaia-cli run-server

    create deploy files

    gaia-cli create-deploy-files

    create scripts files

    gaia-cli create-scripts-files

    create cloud eval files

    gaia-cli create-cloud-eval-files

    run evaluation on a csv input

    gaia-cli evaluate input-csv-file batch-size

    ==============
    Documentation
    ==============

    ========================
    Batch project abilities
    ========================

    DataProc Cluster Manipulation
    =============================
    gaia-cli dataproc-cluster <create / stop / start / delete / connect>

    Workflow Template Manipulation
    ==============================
    gaia-cli workflow-template <create / create_yaml / delete / instantiate>

    DAG Manipulation
    ================
    gaia-cli dag <create / import / delete>

    Upload files to bucket
    ======================
    gaia-cli upload-batch-files <jars, stages, whl , cluster_init, all>

    """
# @click.option("--type", prompt="type", help="type of component")
# @click.option("--project_name", prompt="project_name", help="project_name")
# def apis(type, project_name):


@cli.command()
@click.argument('gen_type')
@click.argument('project_name')
def generate(gen_type, project_name):
    """List all cataloged APIs."""
    try:
        if gen_type in FUNC_ALIASES:
            gen_type = FUNC_ALIASES[gen_type]
        f = globals()["generate_%s" % gen_type]
    except Exception as e:
        click.echo('type ' + gen_type + ' not found')
        return
    f(project_name)


@cli.command()
def run_server():
    currentPipelineFolder = os.path.abspath(os.getcwd())
    currentParentFolder = os.path.join(currentPipelineFolder,"..")
    os.environ["PYTHONPATH"] = currentPipelineFolder
    folder = currentPipelineFolder + '/server/main.py'
    subprocess.call('python ' + folder, shell=True)

@cli.command()
@click.argument('tag')
@click.argument('env', default="prd")
def cloud_eval(tag, env):
    currentPipelineFolder = os.path.abspath(os.getcwd())
    currentParentFolder = os.path.join(currentPipelineFolder,"..")
    os.environ["PYTHONPATH"] = currentPipelineFolder
    folder = currentPipelineFolder + '/tester/dsp/get_model_options.py'
    output = subprocess.check_output('python ' + folder + ' ' + env, shell=True, encoding='utf-8').strip()
    if output:
        # print('output', output)
        l = output.split('\n')
        m = l[-1]
        try:
            l = ast.literal_eval(m)
            o = l[0]
            model = {
                'name': o['name'],
                'id': o['id'],
                'repo': o['repo'],
            }
            folder = currentPipelineFolder + '/tester/dsp/get_dataset_options.py'
            output = subprocess.check_output('python ' + folder + ' ' + env + ' ' + model['name'] + ' ' + str(model['id']),
                                             shell=True, encoding='utf-8').strip()
            l = output.split('\n')
            m = l[-1]
            l = ast.literal_eval(m)
            selected = let_user_pick(l)
            # print('selected', selected)
            if not selected == None:
                selected_dataset = l[selected]
                # print('model',model)
                # print('selected_dataset', selected_dataset)
                folder = currentPipelineFolder + '/tester/dsp/add_experiment.py'
                subprocess.call(('scripts/dvc_push.sh'), shell=True)
                output = subprocess.call(('python', folder, env, json.dumps(model), json.dumps(selected_dataset), tag), shell=True)
                print('you can see your experiment in que')
            else:
                print('selection does not exist')
        except Exception as e:
            print(m)
    else:
        print('could not get models')


# @cli.command()
# def create_deploy_files():
#     copy_deploy_files('')


def create_deploy_files():
    """! Create deploy files (created through 'Create project', but can be used as a standalone function) """
    copy_deploy_files('')


def create_cloud_eval_files():
    """! Create cloud evaluation files (created through 'Create project', but can be used as a standalone function) """
    currentPipelineFolder = os.path.abspath(os.getcwd())
    copy_cloud_eval_files(currentPipelineFolder)


def create_tester_files():
    """! Create tester files (created through 'Create project', but can be used as a standalone function) """
    create_tester_env()


def create_documentation_files():
    """! Create documentation files (created through 'Create project', but can be used as a standalone function) """
    project_name = os.path.basename(os.getcwd())
    copy_documentation_files(os.path.join(directories['main'], 'documentation'))
    update_doc_configuration(project_name, os.path.join(directories['main'], 'documentation'))


def create_batch_files():
    """! Create batch files (created through 'Create project', but can be used as a standalone function) """
    copy_batch_files(directories['main'])

def create_aws_batch_files():
    """! Create batch files (created through 'Create project', but can be used as a standalone function) """
    copy_aws_batch_files(directories['main'])


def create_trainer_files():
    """! Create trainer files (created through 'Create project', but can be used as a standalone function) """
    copy_trainer_files()


@cli.command()
@click.argument('csv_file_path')
@click.argument('batch_size')
def evaluate(csv_file_path, batch_size):
    if os.path.isfile(csv_file_path):
        current_pipeline_folder = os.path.abspath(os.getcwd())
        os.environ["PYTHONPATH"] = current_pipeline_folder
        folder = current_pipeline_folder + '/tester/general_tester.py'
        subprocess.call('python ' + folder + ' ' + csv_file_path + ' ' + batch_size, shell=True)
    else:
        click.echo('file: ' + csv_file_path + ' not found')



@cli.command()
@click.argument('action')
def dataproc_cluster(action: str):
    """! Handle cluster action, either create,  start, stop, delete, or connect to the Dataproc cluster
            Args:
                 action: an action to perform, chosen from: {create, start, stop, delete, connect}
    """
    valid_actions = {'create', 'start', 'connect', 'stop', 'delete'}
    if action not in valid_actions:
        print(f"Can't determine file type {action}. Please use one of: {valid_actions}")
        return

    batch_helper = config_batch_helper()

    if action == 'create':
        # Create DataProc cluster according to project specific configuration
        batch_helper.create_dataproc_cluster()
    elif action == 'start':
        # Start an existing DataProc cluster according to project specific configuration
        batch_helper.start_dataproc_cluster()
    elif action == 'connect':
        # Connect via ssh to an existing DataProc cluster according to project specific configuration.
        # Connection will be made to the master node
        batch_helper.connect_dataproc_cluster()
    elif action == 'stop':
        # Stop an existing DataProc cluster according to project specific configuration
        batch_helper.stop_dataproc_cluster()
    elif action == 'delete':
        # Delete an existing DataProc cluster according to project specific configuration.
        # Since we can't update certain parameters on an existing cluster, we need the option
        # to delete it
        batch_helper.delete_dataproc_cluster()


@cli.command()
@click.argument('action')
def workflow_template(action: str):
    """! Handle workflow action, either create, instantiate or delete the template
        Args:
             action: an action to perform, chosen from: {create, create_yaml, instantiate, delete}
    """
    valid_actions = {'create', 'create_yaml', 'delete', 'instantiate'}
    if action not in valid_actions:
        print(f"Can't determine action type: {action}. Please use one of: {valid_actions}")
        return

    current_folder = os.path.abspath(os.getcwd())

    os.environ["PYTHONPATH"] = current_folder
    workflow_folder = current_folder + '/batch_files/workflow/workflow.py'
    basic_command = 'python ' + workflow_folder

    print(f"Attempting to {action} a workflow template")
    subprocess.call(basic_command + ' ' + action, shell=True)


@cli.command()
@click.argument('action')
def dag(action: str):
    """! Handle DAG actions, either create, delete, or import a DAG
    Once imported, it will start as paused and will be set up for a daily activation
        Args:
             action: an action to perform, chosen from: {create, import, delete}
    """
    valid_actions = {'create', 'import', 'delete'}
    if action not in valid_actions:
        print(f"Can't determine action type: {action}. Please use one of: {valid_actions}")
        return

    current_folder = os.path.abspath(os.getcwd())

    os.environ["PYTHONPATH"] = current_folder
    dag_folder = current_folder + '/batch_files/workflow_dag/dag.py'
    basic_command = 'python ' + dag_folder

    print(f"Attempting to {action} a DAG")
    subprocess.call(basic_command + ' ' + action, shell=True)


@cli.command()
@click.argument('file_type')
def upload_batch_files(file_type: str, provider: str='google'):
    """! Upload all files needed for a batch project to the predefined bucket
        Args:
            file_type: String containing the types of files to upload (jars, stages, whl , cluster_init, or "all")
    """
    batch_helper = config_batch_helper()
    batch_helper.upload_files_to_bucket(file_type, provider)


def config_batch_helper():
    """! Configure the batch file helper for a variety of cli actions
        Returns:
            ZIDSBatchHelper: Instantiation of the batch helper class
    """
    from gaiaframework.cli.batch.batch_helper_functions import ZIDSBatchHelper
    current_folder = os.path.abspath(os.getcwd())
    batch_helper_cls = None
    with open(current_folder + '/batch_files/batch_config.json') as config_file:
        config_dict = json_load(config_file)
        batch_helper_cls = ZIDSBatchHelper(config_dict)
    return batch_helper_cls




ALIASES = {
    "g": generate
}

FUNC_ALIASES = {
    "p": "project"
}


def generate_project(project_name):
    # project_name = clean_name(project_name)
    click.echo('Generating project: ' + project_name)
    create_project(project_name)


def generate_forcer(fileName):
    fileName = clean_name(fileName)
    create_exist_pipeline_file('forcer', fileName)


def generate_predictable(fileName):
    fileName = clean_name(fileName)
    create_exist_pipeline_file('predictable', fileName)


def clean_name(name):
    name = name.replace('-', '_')
    return name


def create_folders(project_name):
    global directories
    directories['main'] = project_name
    if not os.path.exists(directories['main']):
        os.mkdir(directories['main'])

    create_main_folders('config', 'main')
    create_main_folders('pipeline', 'main')
    create_main_folders('deploy', 'main')
    create_main_folders('deploy_eks', 'main')
    create_main_folders('scripts', 'main')
    create_main_folders('artifacts', 'pipeline')
    create_main_folders('models', 'artifacts')
    create_main_folders('vocabs', 'artifacts')
    # create_main_folders('other', 'artifacts')
    create_main_folders('preprocessor', 'pipeline')
    create_main_folders('predictables', 'pipeline')
    create_main_folders('predictors', 'pipeline')
    create_main_folders('forcers', 'pipeline')
    create_main_folders('postprocessor', 'pipeline')
    create_main_folders('schema', 'pipeline')
    create_main_folders('tester', 'main')
    create_main_folders('test_schema', 'tester')
    create_main_folders('dsp', 'tester')
    create_main_folders('trainer', 'main')
    create_main_folders('examples', 'trainer')
    create_main_folders('datasets', 'trainer')
    create_main_folders('my_dataset_name', 'datasets')
    create_main_folders(datetime.today().strftime('%Y%m%d_v1'), 'my_dataset_name')
    create_main_folders('server', 'main')


def create_project(project_name):
    create_folders(project_name)
    original_project_name = project_name
    project_name = clean_name(project_name)

    # Create pipeline files
    create_pipeline_file(project_name, directories['artifacts'], 'shared_artifacts')
    create_pipeline_file(project_name, directories['preprocessor'], 'preprocess')
    create_pipeline_file(project_name, directories['predictors'], 'predictor')
    create_pipeline_file(project_name, directories['forcers'], 'forcer')
    create_pipeline_file(project_name, directories['postprocessor'], 'postprocess')
    create_pipeline_file(project_name, directories['predictables'], 'predictable')
    create_pipeline_file(project_name, directories['pipeline'], 'pipeline')
    create_pipeline_file(project_name, directories['main'], 'pipeline_test', False)

    # Create schema files
    create_schema_file(project_name, directories['schema'], 'inputs')
    create_schema_file(project_name, directories['schema'], 'outputs')
    create_schema_file(project_name, directories['schema'], '__init__', False)

    # Create tester files
    create_tester_file(project_name, directories['tester'], 'general_tester', False)
    create_tester_file(project_name, directories['tester'], 'evaluator', False)
    create_schema_file(project_name, directories['test_schema'], 'test_input', False)
    create_schema_file(project_name, directories['test_schema'], 'test_output', False)

    create_dsp_file(original_project_name, directories['dsp'], 'get_model_options', False)
    create_dsp_file(original_project_name, directories['dsp'], 'get_dataset_options', False)
    create_dsp_file(original_project_name, directories['dsp'], 'add_experiment', False)

    # Create server files
    create_server_file(project_name, directories['server'], 'main', False)
    create_server_file(project_name, directories['server'], 'test_server_post', False)
    create_server_file(project_name, directories['server'], 'test_server_post_stream', False)
    create_server_file(project_name, directories['server'], 'pool', False)
    create_server_file(project_name, directories['server'], 'token_generator', False)
    create_server_file(project_name, directories['server'], '__init__', False)

    create_project_config_json()
    create_project_gitignore()
    create_server_config_json()
    copy_deploy_files(directories['main'])
    copy_scripts_files(directories['main'])
    copy_cloud_eval_files(directories['main'])
    copy_batch_files(directories['main'])
    copy_aws_batch_files(directories['main'])
    copy_documentation_files(os.path.join(directories['main'], 'documentation'))
    update_doc_configuration(project_name, os.path.join(directories['main'], 'documentation'))


    change_to_project_dir()
    run_dvc_init()
    run_git_init()


def create_main_folders(targetDir, baseDir):
    global directories
    directories[targetDir] = directories[baseDir] + '/' + targetDir
    if not os.path.exists(directories[targetDir]):
        os.mkdir(directories[targetDir])


def create_pipeline_file(project_name, folder, pipelineType, createInitFile=True):
    data = read_template_file(pipelineType)
    replace_in_template_and_create_file(project_name, folder, pipelineType, data, createInitFile)


def create_schema_file(project_name, folder, pipelineType, createInitFile=True):
    data = read_template_file('schema/' + pipelineType)
    replace_in_template_and_create_file(project_name, folder, pipelineType, data, createInitFile)


def create_server_file(project_name, folder, pipelineType, createInitFile=True):
    data = read_template_file('tester/server/' + pipelineType)
    replace_in_template_and_create_file(project_name, folder, pipelineType, data, createInitFile)


def create_tester_file(project_name, folder, test_file_type, createInitFile=True):
    data = read_template_file('tester/' + test_file_type)
    replace_in_template_and_create_file(project_name, folder, test_file_type, data, createInitFile)

def create_dsp_file(project_name, folder, test_file_type, createInitFile=True):
    data = read_template_file('tester/dsp/' + test_file_type)
    replace_in_template_and_create_file(project_name, folder, test_file_type, data, createInitFile)


def create_exist_pipeline_file(type, fileName):
    pipelineType = type + 's'
    folder = 'pipeline/' + pipelineType
    if os.path.exists(folder):
        data = read_template_file(type)
        fileNameNoUnderscore = to_capitalize_no_underscore(fileName)
        className = fileNameNoUnderscore + type.capitalize()
        currentPipelineFolder = os.path.basename(os.getcwd())
        currentDir = folder.replace('/', '.')

        data = data.replace('generatedClass', className)

        new_file = folder + "/" + fileName + ".py"
        current_init_file = folder + "/__init__.py"
        new_init_export = "from " + '.' + fileName + " import " + className

        create_file(new_file, data)
        create_init_file(current_init_file, new_init_export)
        inject_to_pipeline(fileName, type, className, new_init_export)
    else:
        print('please create a project and go to project location first')
    pass


def create_tester_env():
    """
    This function will create a testing environment, if one does not already exist in the project.
    It will create the testing, evaluation, and relevant schema files.
    """
    project_name = os.getcwd().split('/')[-1]
    dst_folder = 'tester/'
    schema_dst_folder = 'tester/test_schema/'
    tester_file_list = ["tester/general_tester",
                        "tester/evaluator",
                        "schema/test_input",
                        "schema/test_output"]

    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)
        os.mkdir(schema_dst_folder)

        for filename_with_path in tester_file_list:
            file_only = filename_with_path.split('/')[-1]
            if file_only.startswith('test'):
                dst_folder = schema_dst_folder

            data = read_template_file(filename_with_path)

            clean_project_name = clean_existing_project_name(project_name)
            filename_no_underscore = to_capitalize_no_underscore(file_only)

            class_name = clean_project_name + filename_no_underscore

            data = data.replace('generatedClass', class_name)
            data = data.replace('generatedProjectName', clean_project_name)

            new_file = dst_folder + "/" + file_only + ".py"
            create_file(new_file, data)

            # Test schema does not use generated class name for now, so this code should be modified before uncommenting
            # current_init_file = dst_folder + "/" + "__init__.py"
            # new_init_export = "from " + dst_folder.replace('/', '.') + "." + file_only + " import " + class_name
            # create_init_file(current_init_file, new_init_export)
    else:
        print('Tester folder Already exists. If you wish to recreate, please erase folder and retry')
    pass


def read_template_file(filename):
    with open(os.path.join(__location__, 'gaiaframework/cli/' + filename + '_template.py'), 'r') as file:
        data = file.read()
        return data


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)
        file.close()


def replace_in_template_and_create_file(project_name, folder, pipelineType, data, createInitFile):
    """! Get & Replace the template file and create new one with project_name
    @verbatim
    Args:
        project_name : The project name
        folder       : The folder we want to create the new file.
        pipelineType : Which File.
        data         : The template file.
        createInitFile(=True): Create init file - if doesnt exist.
    @endverbatim
    """

    pipeline_type_no_underscore = to_capitalize_no_underscore(pipelineType)
    project_name_no_underscore = to_capitalize_no_underscore(project_name)
    className = project_name_no_underscore + pipeline_type_no_underscore
    classNameForBaseObject = project_name_no_underscore + pipeline_type_no_underscore
    currentDir = folder.replace('/', '.')
    currentDirNoMainDir = folder.replace(directories['main'] + '/', '').replace('/', '.')
    currentBaseDir = directories['main'].replace('/', '.')
    currentPipelineDir = directories['pipeline'].replace('/', '.')

    data = data.replace('generatedClassName', classNameForBaseObject)
    data = data.replace('generatedClass', className)
    data = data.replace('original_project_name', project_name)
    data = data.replace('generatedProjectName', project_name_no_underscore)
    data = data.replace('generatedDirectory', currentDir)
    data = data.replace('generatedBaseDir', currentBaseDir)
    data = data.replace('generatedPipelineDir', currentPipelineDir)

    new_file = folder + "/" + pipelineType + ".py"
    create_file(new_file, data)

    if createInitFile:
        new_init_file = folder + "/__init__.py"
        new_init_export = "from " + '.' + pipelineType + " import " + className
        create_init_file(new_init_file, new_init_export)


def create_predictable_file(fileName):
    pass


def create_file(new_file_path, data):
    """! Create new file and write the data file into it
    @verbatim
    Args:
        new_file_path : New file name path.
        data          : The content of the new file.
    @endverbatim
    """

    if not os.path.exists(new_file_path):
        f = open(new_file_path, "w")
        f.write(data)
        f.close()


def create_init_file(init_path, init_export):
    """! if init file doesnt exist - create it and add the export line
         if init file exist - check if the init_export line appears in the init file : if not add it.

    @verbatim
    Args:
        init_path   : Init file.
        init_export : Import line to add if needed.
    @endverbatim
    """

    if not os.path.exists(init_path):
        f = open(init_path, "w")
        f.write(init_export)
        f.close()
    else:
        f = open(init_path, 'r+')
        data = f.read()
        if init_export not in data:
            if len(data) and not data.endswith('\n'):
                f.write('\n')
            f.write(init_export)
            f.close()

def save_file(file_name_path, data):
    f = open(file_name_path, "w")
    f.write(data)
    f.close()


def inject_to_pipeline(fileName, type, className, new_init_export):
    """! Building the component in the pipeline file
    @verbatim
    Args:
        fileName       : New file name.
        type           : New component type (forcer or predictable)
        className      : New component class.
        new_init_export: Create init file - if doesnt exist.
    @endverbatim
    """

    file_path = 'pipeline/pipeline.py'
    if os.path.exists(file_path):
        data = read_file(file_path)
        new_tab_line = '\n'
        data_changed = False
        last_index_of_import = -1
        first_index_of_add_component = -1
        index_of_class = re.search(r'class[^\n]*', data)

        # finding current indent config
        index_of_build_pipeline = re.search(r'def build_pipeline[^\n]*', data)
        index_of_build_preprocessor = re.search(r'self.preprocessor =[^\n]*', data)
        index_of_build_postprocessor = re.search(r'self.postprocessor =[^\n]*', data)
        index_of_build_pipeline_row = re.search(r'.*def build_pipeline[^\n]*', data)
        if index_of_build_pipeline:
            build_pipeline_indent = (index_of_build_pipeline.start() - index_of_build_pipeline_row.start()) * 2
            new_tab_line = new_tab_line.ljust(build_pipeline_indent + 1)

        attr = fileName + type.title()
        new_component_line = 'self.' + attr + ' = ' + className + '()'
        add_component_line = 'self.add_component(self.' + attr + ')'

        # finding imports and add components indexes
        last_index_of_add_component = -1
        all_from_import = [i.end() for i in re.finditer(r'from[^\n]*', data)]
        all_add_components = [[i.start(), i.end()] for i in re.finditer(r'self.add_component[^\n]*', data)]
        if len(all_from_import):
            last_index_of_import = all_from_import[-1]
        if len(all_add_components):
            first_index_of_add_component = all_add_components[0][0]
            last_index_of_add_component = all_add_components[-1][-1]
        # finding imports and add components indexes


        index_to_add = 0

        # add import to end of imports or to top of file
        if last_index_of_import > -1 and new_init_export not in data:
            s = '\n' + new_init_export
            index_to_add += len(s)
            data = data[:last_index_of_import] + s + data[last_index_of_import:]
            data_changed = True
        elif index_of_class and new_init_export not in data:
            s = new_init_export + '\n\n'
            index_to_add += len(s)
            data = data[:index_of_class.start()] + s + data[index_of_class.start():]
            data_changed = True

        # check if build_pipeline exist but with no components yet
        if first_index_of_add_component == -1 and last_index_of_add_component == -1 and index_of_build_pipeline:
            s = new_tab_line
            current_end = index_of_build_pipeline.end()
            if index_of_build_preprocessor:
                current_end = index_of_build_preprocessor.end()
            if index_of_build_postprocessor:
                current_end = index_of_build_postprocessor.end()
            index = current_end + index_to_add
            index_to_add += len(s)
            data = data[:index] + s + data[index:]
            data_changed = True
            first_index_of_add_component = current_end
            last_index_of_add_component = current_end

        # adding new component line
        if first_index_of_add_component > -1 and new_component_line not in data:
            first_index_of_add_component += index_to_add
            if len(all_add_components):
                new_component_line = new_component_line + new_tab_line
            index_to_add += len(new_component_line)
            data = data[:first_index_of_add_component] + new_component_line + data[first_index_of_add_component:]
            data_changed = True

        #adding add_component line
        if last_index_of_add_component > -1 and add_component_line not in data:
            last_index_of_add_component += index_to_add
            add_component_line = new_tab_line + add_component_line
            index_to_add += len(add_component_line)
            data = data[:last_index_of_add_component] + add_component_line + data[last_index_of_add_component:]
            data_changed = True

        if data_changed:
            write_to_file(file_path, data)


def inject_to_pipeline(fileName, type, className, new_init_export):
    file_path = 'pipeline/pipeline.py'
    if os.path.exists(file_path):
        data = read_file(file_path)
        new_tab_line = '\n'
        data_changed = False
        last_index_of_import = -1
        first_index_of_add_component = -1
        index_of_class = re.search(r'class[^\n]*', data)

        # finding current indent config
        index_of_build_pipeline = re.search(r'def build_pipeline[^\n]*', data)
        index_of_build_preprocessor = re.search(r'self.preprocessor =[^\n]*', data)
        index_of_build_postprocessor = re.search(r'self.postprocessor =[^\n]*', data)
        index_of_build_pipeline_row = re.search(r'.*def build_pipeline[^\n]*', data)
        if index_of_build_pipeline:
            build_pipeline_indent = (index_of_build_pipeline.start() - index_of_build_pipeline_row.start()) * 2
            new_tab_line = new_tab_line.ljust(build_pipeline_indent + 1)

        attr = fileName + type.title()
        new_component_line = 'self.' + attr + ' = ' + className + '()'
        add_component_line = 'self.add_component(self.' + attr + ')'

        # finding imports and add components indexes
        last_index_of_add_component = -1
        all_from_import = [i.end() for i in re.finditer(r'from[^\n]*', data)]
        all_add_components = [[i.start(), i.end()] for i in re.finditer(r'self.add_component[^\n]*', data)]
        if len(all_from_import):
            last_index_of_import = all_from_import[-1]
        if len(all_add_components):
            first_index_of_add_component = all_add_components[0][0]
            last_index_of_add_component = all_add_components[-1][-1]
        # finding imports and add components indexes


        index_to_add = 0

        # add import to end of imports or to top of file
        if last_index_of_import > -1 and new_init_export not in data:
            s = '\n' + new_init_export
            index_to_add += len(s)
            data = data[:last_index_of_import] + s + data[last_index_of_import:]
            data_changed = True
        elif index_of_class and new_init_export not in data:
            s = new_init_export + '\n\n'
            index_to_add += len(s)
            data = data[:index_of_class.start()] + s + data[index_of_class.start():]
            data_changed = True

        # check if build_pipeline exist but with no components yet
        if first_index_of_add_component == -1 and last_index_of_add_component == -1 and index_of_build_pipeline:
            s = new_tab_line
            current_end = index_of_build_pipeline.end()
            if index_of_build_preprocessor:
                current_end = index_of_build_preprocessor.end()
            if index_of_build_postprocessor:
                current_end = index_of_build_postprocessor.end()
            index = current_end + index_to_add
            index_to_add += len(s)
            data = data[:index] + s + data[index:]
            data_changed = True
            first_index_of_add_component = current_end
            last_index_of_add_component = current_end

        # adding new component line
        if first_index_of_add_component > -1 and new_component_line not in data:
            first_index_of_add_component += index_to_add
            if len(all_add_components):
                new_component_line = new_component_line + new_tab_line
            index_to_add += len(new_component_line)
            data = data[:first_index_of_add_component] + new_component_line + data[first_index_of_add_component:]
            data_changed = True

        #adding add_component line
        if last_index_of_add_component > -1 and add_component_line not in data:
            last_index_of_add_component += index_to_add
            add_component_line = new_tab_line + add_component_line
            index_to_add += len(add_component_line)
            data = data[:last_index_of_add_component] + add_component_line + data[last_index_of_add_component:]
            data_changed = True

        if data_changed:
            write_to_file(file_path, data)


def create_project_config_yaml():
    with open(os.path.join(__location__, 'gaiaframework/cli/config.yaml'), 'r') as file:
        data = file.read()
        data = data.replace('generatedDirectory', directories['main'])
        new_file = directories['main'] + '/pipeline/config.yaml'
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()


def create_project_config_json():
    with open(os.path.join(__location__, 'gaiaframework/cli/config.json'), 'r') as file:
        data = file.read()
        data = data.replace('generatedDirectory', directories['main'])
        new_file = directories['main'] + '/config/config.json'
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()


def create_project_gitignore():
    with open(os.path.join(__location__, 'gaiaframework/cli/.gitignore'), 'r') as file:
        data = file.read()
        new_file = directories['main'] + '/.gitignore'
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()


def create_server_config_json():
    with open(os.path.join(__location__, 'gaiaframework/cli/cors_allowed_origins.json'), 'r') as file:
        data = file.read()
        data = data.replace('generatedDirectory', directories['main'])
        new_file = directories['server'] + '/cors_allowed_origins.json'
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()


def change_to_project_dir():
    os.chdir(directories['main'])


def run_dvc_init():
    dir_path = os.getcwd()
    if not os.path.isdir(dir_path + '/.dvc'):
        command = dir_path + '/scripts/dvc_init.sh'
        if not isWindows:
            command = './' + command
        subprocess.call(command, shell=True)


def run_git_init():
    dir_path = os.getcwd()
    if not os.path.isdir(dir_path + '/.git'):
        command = dir_path + '/scripts/git_init.sh'
        if not isWindows:
            command = './' + command
        subprocess.call(command, shell=True)


def copy_deploy_files(main_dir):
    currentPipelineFolder = os.path.basename(os.getcwd())
    if main_dir:
        currentPipelineFolder = main_dir
    dir = os.path.join(__location__, 'gaiaframework/cli/tester/deploy_files/')
    listOfFiles = list()
    for (dirpath, dirname, filenames) in os.walk(dir):
        dirpath = dirpath.replace(dir, '')
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for file_path in listOfFiles:
            with open(os.path.join(dir, file_path), 'r', encoding="utf8") as file:
                try:
                    data = file.read()
                    data = data.replace('{name-your-service}', currentPipelineFolder)
                    data = data.replace('{name-your-service-dashed}', currentPipelineFolder.replace('_', '-'))
                    data = data.replace('{name-your-artifacts}', currentPipelineFolder)
                    dirToCreate = ''
                    if main_dir:
                        dirToCreate = main_dir + '/'
                    if not os.path.exists(dirToCreate + file_path):
                        f = open(dirToCreate + file_path, "w")
                        f.write(data)
                        f.close()
                        # Make sure that .sh files can be executed
                        if (dirToCreate + file_path).endswith('.sh'):
                            os.chmod(dirToCreate + file_path, 0o744)
                except Exception as ex:
                    pass
    # for item in os.listdir(dir):
    #     s = os.path.join(dir, item)
    #     d = os.path.join(main_dir, item)
    #     if os.path.isdir(s):
    #         shutil.copytree(s, d, False, None)
    #     else:
    #         shutil.copy2(s, d)

def copy_scripts_files(main_dir):
    currentPipelineFolder = os.path.basename(os.getcwd())
    if main_dir:
        currentPipelineFolder = main_dir
    dir = os.path.join(__location__, 'gaiaframework/cli/tester/scripts/')
    listOfFiles = list()
    for (dirpath, dirname, filenames) in os.walk(dir):
        dirpath = dirpath.replace(dir, '')
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for file_path in listOfFiles:
            with open(os.path.join(dir, file_path), 'r', encoding="utf8") as file:
                try:
                    data = file.read()
                    data = data.replace('{name-your-service}', currentPipelineFolder)
                    data = data.replace('{name-your-artifacts}', currentPipelineFolder)
                    dirToCreate = ''
                    if main_dir:
                        dirToCreate = main_dir + '/scripts/'
                    if not os.path.exists(dirToCreate + file_path):
                        f = open(dirToCreate + file_path, "wb")
                        f.write(data.encode('utf-8'))
                        f.close()
                        # Make sure that .sh files can be executed
                        if (dirToCreate + file_path).endswith('.sh'):
                            os.chmod(dirToCreate + file_path, 0o744)
                except Exception as ex:
                    pass
    # for item in os.listdir(dir):
    #     s = os.path.join(dir, item)
    #     d = os.path.join(main_dir, item)
    #     if os.path.isdir(s):
    #         shutil.copytree(s, d, False, None)
    #     else:
    #         shutil.copy2(s, d)


def copy_cloud_eval_files(main_dir):
    currentPipelineFolder = os.path.basename(os.getcwd())
    if main_dir:
        currentPipelineFolder = main_dir
    service_folder = str(currentPipelineFolder)
    service_name = service_folder.split('/')[-1]
    project_name_no_underscore = clean_existing_project_name(service_name)
    dir = os.path.join(__location__, 'gaiaframework/cli/tester/cloud_eval/')
    listOfFiles = list()
    conflicted_files = []
    for (dirpath, dirname, filenames) in os.walk(dir):
        if "__pycache__" in dirpath:
            continue
        dirpath = dirpath.replace(dir, '')
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for file_path in listOfFiles:
            framework_source_file = os.path.join(dir, file_path)
            with open(framework_source_file, 'r', encoding="utf8") as file:
                try:
                    data = file.read()
                    data = data.replace('{name-your-service}', service_name)
                    data = data.replace('{name-your-artifacts}', service_name)
                    data = data.replace('generatedProjectName', project_name_no_underscore)
                    dirToCreate = ''
                    if main_dir:
                        dirToCreate = main_dir + '/cloud_eval/'
                    if not os.path.exists(dirToCreate):
                        os.makedirs(dirToCreate)
                    # if "#cli_file_dest=[" in data:
                    #     start_ix = data.index("#cli_file_dest=[") + len("#cli_file_dest=[")
                    #     end_ix = data.index("]", start_ix)
                    #     destination_dir = data[start_ix:end_ix]
                    #     data = data[:data.index("#cli_file_dest=[")] + data[end_ix+1:]
                    #     dirToCreate = main_dir + '/' + destination_dir

                    if not os.path.exists(dirToCreate + file_path):
                        f = open(dirToCreate + file_path, "w")
                        f.write(data)
                        f.close()
                        # Make sure that .sh files can be executed
                        if (dirToCreate + file_path).endswith('.sh'):
                            os.chmod(dirToCreate + file_path, 0o744)
                    else:
                        with open(dirToCreate + file_path, "r") as f:
                            existing_data = f.read()
                        if existing_data != data:
                            conflicted_file = f"{dirToCreate + file_path}"
                            conflicted_files.append((conflicted_file, str(framework_source_file)))

                except Exception as ex:
                    pass

    if conflicted_files:
        print("The following files already exists, so not overwriting them. "
              "However, notice it is different from the framework version in")
        for conflicted_file in conflicted_files:
            print(f"Existing: [{conflicted_file[0]}] \t\t Framework source file [{conflicted_file[1]}]")
def copy_batch_files(main_dir):
    """! Generate batch files needed for batch projects. Creates 3 stages:
    1. Get Data
    2. Run Pipeline
    3. Set Data

    Along with a matching workflow file, and a configuration file
    """

    current_folder = os.path.basename(os.getcwd())
    if main_dir:
        current_folder = main_dir
    service_name = current_folder.split('/')[-1]
    project_name_no_underscore = clean_existing_project_name(service_name)
    source_dir = os.path.join(__location__, 'gaiaframework/cli/tester/batch_files/')

    for (dir_path, dir_name, filenames) in os.walk(source_dir):
        if "__pycache__" in dir_path:
            continue
        dir_path = dir_path.replace(source_dir, '')
        file_list = [os.path.join(dir_path, file) for file in filenames]
        for file_path in file_list:
            with open(os.path.join(source_dir, file_path), 'r', encoding="utf8") as file:
                try:
                    data = file.read()
                    data = data.replace('{name-your-service}', current_folder)
                    data = data.replace('generatedProjectName', project_name_no_underscore)
                    dir_to_create = ''
                    target_dir = ''
                    if main_dir:
                        target_dir = main_dir + '/batch_files/'
                        dir_to_create = main_dir + '/batch_files/' + dir_path + '/'
                    if not os.path.exists(dir_to_create):
                        os.makedirs(dir_to_create)
                    if not os.path.exists(target_dir + file_path):
                        f = open(target_dir + file_path, "w")
                        f.write(data)
                        f.close()
                except Exception as ex:
                    if file_path.rsplit('.', 1)[-1] == 'jar':
                        d = f'{main_dir}/batch_files/{dir_path}/'
                        if not os.path.exists(d):
                            os.makedirs(d)
                        shutil.copy(os.path.join(source_dir, file_path), d)
                    else:
                        print(f'Error when trying to open: {file_path}: {ex}')
                    pass

def copy_aws_batch_files(main_dir):
    """! Generate batch files needed for batch projects. Creates 3 stages:
    1. Get Data
    2. Run Pipeline
    3. Set Data

    Along with a matching workflow file, and a configuration file
    """

    current_folder = os.path.basename(os.getcwd())
    if main_dir:
        current_folder = main_dir
    service_name = current_folder.split('/')[-1]
    project_name_no_underscore = clean_existing_project_name(service_name)
    source_dir = os.path.join(__location__, 'gaiaframework/cli/tester/aws_batch_files/')

    for (dir_path, dir_name, filenames) in os.walk(source_dir):
        if "__pycache__" in dir_path:
            continue
        dir_path = dir_path.replace(source_dir, '')
        file_list = [os.path.join(dir_path, file) for file in filenames]
        for file_path in file_list:
            with open(os.path.join(source_dir, file_path), 'r', encoding="utf8") as file:
                try:
                    data = file.read()
                    data = data.replace('{name-your-service}', current_folder)
                    data = data.replace('generatedProjectName', project_name_no_underscore)
                    dir_to_create = ''
                    target_dir = ''
                    if main_dir:
                        target_dir = main_dir + '/aws_batch_files/'
                        dir_to_create = main_dir + '/aws_batch_files/' + dir_path + '/'
                    if not os.path.exists(dir_to_create):
                        os.makedirs(dir_to_create)
                    if not os.path.exists(target_dir + file_path):
                        f = open(target_dir + file_path, "w")
                        f.write(data)
                        f.close()
                except Exception as ex:
                    if file_path.rsplit('.', 1)[-1] == 'jar':
                        d = f'{main_dir}/batch_files/{dir_path}/'
                        if not os.path.exists(d):
                            os.makedirs(d)
                        shutil.copy(os.path.join(source_dir, file_path), d)
                    else:
                        print(f'Error when trying to open: {file_path}: {ex}')
                    pass


def copy_trainer_files():
    """! This function will create a trainer environment."""

    project_name = os.getcwd().split('/')[-1]
    trainer_main_folder = 'trainer/'
    trainer_datasets_folder = 'trainer/datasets/'
    trainer_datasets_versions_folder = 'trainer/datasets/my_dataset_name/' + datetime.today().strftime('%Y%m%d_v1') + '/'
    trainer_examples_folder = 'trainer/examples/'

    trainer_file_list = ["trainer/custom_dataset",
                         "trainer/data_module",
                         "trainer/iterable_dataset",
                         "trainer/model",
                         "trainer/network_module",
                         "trainer/trainer",
                         "trainer/examples/example1_mnist",
                         "trainer/examples/example2_wine_quality"]

    if not os.path.exists(trainer_main_folder):
        os.mkdir(trainer_main_folder)

    if not os.path.exists(trainer_datasets_folder):
        os.makedirs(trainer_datasets_versions_folder)

    if not os.path.exists(trainer_examples_folder):
        os.mkdir(trainer_examples_folder)

    for filename_path in trainer_file_list:
        file_only = filename_path.split('/')[-1]
        parent_folder = filename_path.split('/')[-2]

        dst_folder = ''
        if parent_folder == 'datasets':
            dst_folder = trainer_datasets_folder
        elif parent_folder == 'examples':
            dst_folder = trainer_examples_folder

        data = read_template_file(filename_path)

        clean_project_name = clean_existing_project_name(project_name)
        filename_no_underscore = to_capitalize_no_underscore(file_only)

        class_name = clean_project_name + filename_no_underscore

        data = data.replace('generatedClass', class_name)
        data = data.replace('generatedProjectName', clean_project_name)

        new_file = trainer_main_folder + file_only + ".py"
        if dst_folder != '':
            new_file = dst_folder + file_only + ".py"

        if not os.path.isfile(new_file):
            create_file(new_file, data)
        else:
            print(f'File \'{new_file}\' exists, skipping.')

    source_path = os.path.join(__location__, 'gaiaframework/cli/', 'trainer/requirements_trainer.txt')
    shutil.copyfile(source_path, trainer_main_folder + '/requirements_trainer.txt')

    print("Creating trainer environment done !")


def copy_documentation_files(target_dir):
    """! Copy documentation folder to newly created project.

    Args:
        target_dir: Newly created project location
    """
    source_dir = os.path.join(__location__, 'gaiaframework/documentation/')
    shutil.copytree(source_dir, target_dir, ignore=shutil.ignore_patterns('dsf*'))


def update_doc_configuration(project_name, target_dir):
    """! Update project doxygen configuration file, adding project name.

    Args:
        project_name: Newly created project name
        target_dir: Configuration file location.
    """
    project_name_no_underscore = to_capitalize_no_underscore(project_name)
    source_dir = os.path.join(target_dir, 'project_doxyfile')
    data = read_file(source_dir)
    data = data.replace('generatedProjectName', project_name_no_underscore)
    save_file(source_dir, data)


@cli.command()
def install_trainer_packages():
    command = 'pip install -r trainer/requirements_trainer.txt'
    subprocess.call(command, shell=True)

def to_capitalize_no_underscore(text):
    return ''.join(elem.capitalize() for elem in text.split('_'))


def clean_existing_project_name(text):
    no_underscore_text = to_capitalize_no_underscore(text)
    return ''.join(elem.capitalize() for elem in no_underscore_text.split('-'))

def let_user_pick(options):
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)-1
    except:
        pass
    return None


if __name__ == '__main__':
    cli(prog_name='cli')
