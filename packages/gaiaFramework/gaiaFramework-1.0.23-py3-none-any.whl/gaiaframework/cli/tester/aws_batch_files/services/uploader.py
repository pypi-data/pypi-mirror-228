import boto3
from boto3.s3.transfer import TransferConfig
import datetime
import sys
import os
import subprocess
from json import load as json_load
# from airflow.api.common.experimental.trigger_dag import trigger_dag
from airflow.api.common import trigger_dag
from airflow.models import DagBag

class S3Uploader:
    def __init__(self, AWS_PROFILE=None):

        if AWS_PROFILE:
            boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.storage_client = boto3.resource('s3')

        file_path = sys.modules[self.__class__.__module__].__file__
        curr_path = file_path[:file_path.rfind("aws_batch_files")]

        with open(curr_path + '/aws_batch_files/batch_config.json') as batch_cfg_file:
            self.config = json_load(batch_cfg_file)

        stage_config = self.config
        self.user_id = ''
        env_type = os.environ.get('SPRING_PROFILES_ACTIVE')
        if (not env_type == 'production') and (not env_type == 'staging'):
            command = 'gcloud config get-value account'
            self.user_id = boto3.client('sts').get_caller_identity().get('UserId').replace(':', '_')

        self.bucket_name = stage_config['bucket_name']
        self.project_id = stage_config['project_id']
        self.project_name = stage_config['project_name']
        self.target = stage_config['target']
        self.unique_template_id = stage_config['unique_template_id']
        self.region = stage_config['region']
        self.zone = self.region + '-b'  # TODO: Check if we can configure this as well
        self.template_id = stage_config['template_id']
        self.unique_iteration_id = stage_config['unique_iteration_id']
        # self.cluster_name = stage_config['cluster_conf']['managed_cluster']['cluster_name']
        # self.cluster_duration = stage_config['cluster_duration_sec']
        # self.managed_cluster = stage_config['cluster_conf']['managed_cluster']
        if self.unique_iteration_id:
            self.folder_path = self.project_name + self.user_id + \
                               '/unique_iteration_id_' + self.unique_iteration_id
        else:
            self.folder_path = self.project_name + self.user_id + '/main'

        self.bucket_path = f's3://{self.bucket_name}/{self.folder_path}'
        self.project_path = 'projects/{project_id}/regions/{region}'.format(project_id=self.project_id,
                                                                            region=self.region)

        self.bucket = self.storage_client.Bucket(self.bucket_name)

    def upload_script(self, local_path, remote_folder):
        remote_key = f"{remote_folder}/spark_script.py"
        self.storage_client.upload_file(local_path, self.bucket_name, remote_key)
        print(f"Uploaded {local_path} to s3://{self.bucket_name}/{remote_key}")

    def upload_dag(self, local_path, remote_folder):
        remote_key = f"{remote_folder}/{local_path.split('/')[-1]}"
        self.storage_client.upload_file(local_path, self.bucket_name, remote_key)
        print(f"Uploaded {local_path} to s3://{self.bucket_name}/{remote_key}")

    def start_paused_dag(self, dag_id):
        dag_bag = DagBag()
        if dag_id in dag_bag.dags:
            dag = dag_bag.dags[dag_id]
            execution_date = datetime.datetime.now()
            run_id = f"manual__{execution_date.isoformat()}"
            conf = {}  # You can provide any additional configuration if needed
            execution_date_str = execution_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            trigger_dag(dag_id, run_id=run_id, execution_date=execution_date_str, conf=conf)
            print(f"Started DAG run for {dag_id} manually with run_id: {run_id}")
        else:
            print(f"DAG {dag_id} not found in DAG bag.")

    def upload_cluster_init_to_bucket(self, root_dir):
        """! Upload cluster initialization script to a given bucket
                Args:
                    root_dir: Directory in which we search for the cluster initialization script
        """
        name = 'cluster-init-actions.sh'
        path_local = os.path.join(root_dir, name)
        bucket_blob_path = path_local[path_local.index(self.project_name) + len(self.project_name):].replace('\\',
                                                                                                             '/')
        self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)
        # blob = self.bucket.blob(self.folder_path + bucket_blob_path)
        # blob.upload_from_filename(path_local)
        # self.gsutils_upload_one_file(path_local, bucket_blob_path)
        print(f'uploaded cluster init script to: {self.folder_path + bucket_blob_path}')

    def upload_requirements_to_bucket(self, root_dir):
        """! Upload cluster initialization script to a given bucket
                Args:
                    root_dir: Directory in which we search for the cluster initialization script
        """
        name = 'requirements_docker.txt'
        path_local = os.path.join(root_dir, name)
        bucket_blob_path = path_local[path_local.index(self.project_name) + len(self.project_name):].replace('\\',
                                                                                                             '/')
        self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)
        # blob = self.bucket.blob(self.folder_path + bucket_blob_path)
        # blob.upload_from_filename(path_local)
        # self.gsutils_upload_one_file(path_local, bucket_blob_path)
        print(f'uploaded requirements to: {self.folder_path + bucket_blob_path}')

    def upload_jars_to_bucket(self, root_dir):
        """! Upload relevant jars to a given bucket
            Args:
                root_dir: Directory in which we search for the jars directory
        """

        for path, subdirs, files in os.walk(root_dir + '/jars'):
            for name in files:
                path_local = os.path.join(path, name)
                bucket_blob_path = path_local[path_local.index(self.project_name) +
                                              len(self.project_name):].replace('\\', '/')
                self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)
            # print(path_local)
            # print(bucket_blob_path)
        print('uploaded jars main successfully')

    def upload_stages_main_to_bucket(self, root_dir):
        """! Upload relevant stages to a given bucket
            Args:
                root_dir: Directory in which we search for the stages directory
        """

        for path, subdirs, files in os.walk(root_dir + '/stages'):
            for name in files:
                if name == 'main.py':
                    path_local = os.path.join(path, name)
                    bucket_blob_path = path_local[path_local.index(self.project_name) +
                                                  len(self.project_name):].replace('\\', '/')
                    self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)
                # print(path_local)
                # print(bucket_blob_path)
                # print(name)
        print('uploaded stages main successfully')

    def upload_whl_to_bucket(self, root_dir):
        """! Upload relevant wheel file to a given bucket
            Args:
                root_dir: Directory in which we search for the wheel archive
        """

        parent_path = os.path.abspath(os.path.join(root_dir, ".."))
        dist = parent_path + '/dist'

        # config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
        #                         multipart_chunksize=1024 * 25, use_threads=True)
        onlyfiles = [os.path.join(dist, f) for f in os.listdir(dist) if os.path.isfile(os.path.join(dist, f))]
        for path_local in onlyfiles:
            bucket_blob_path = path_local[path_local.index(self.project_name) +
                                          len(self.project_name):].replace('\\', '/')
            self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)

            # blob = self.bucket.blob(self.folder_path + bucket_blob_path)
            # blob.chunk_size = 1024 * 1024
            # blob.upload_from_filename(path_local)
        # print(path_local)
        # print(project_bucket_folder + bucket_blob_path)

        print(f'uploaded package whl successfully to: {self.folder_path}')

    def upload_files_to_bucket(self, upload_type: str):
        """! Upload jars, stages, cluster init script and wheel file to a given bucket
                Args:
                    upload_type: String reflecting which file type we wish to upload to
                                 bucket (jars, stages, whl, cluster-init, all)
        """
        valid_types = {'all', 'jars', 'stages', 'whl', 'cluster-init', 'requirements'}
        if upload_type not in valid_types:
            print(f"Can't determine file type {upload_type}. "
                  f"Please use one of: 'all', 'jars', 'stages', 'whl', 'cluster-init'")
            return

        print(f'Uploading files of type: {upload_type} to bucket: {self.bucket_name}')

        project_path = os.path.abspath(os.path.join(os.getcwd()))
        batch_files_path = os.path.abspath(os.path.join(os.getcwd(), 'aws_batch_files'))
        script_path = os.path.join(batch_files_path, 'scripts')

        if upload_type == 'all' or upload_type == 'jars':
            self.upload_jars_to_bucket(batch_files_path)
        if upload_type == 'all' or upload_type == 'stages':
            self.upload_stages_main_to_bucket(batch_files_path)
        if upload_type == 'all' or upload_type == 'whl':
            self.upload_whl_to_bucket(batch_files_path)
        if upload_type == 'all' or upload_type == 'cluster-init':
            self.upload_cluster_init_to_bucket(script_path)
        if upload_type == 'all' or upload_type == 'requirements':
            self.upload_requirements_to_bucket(project_path)

    def upload_dag2(self):
        name = 'dag/dag.py'
        parent_path = os.path.abspath(os.path.join(os.getcwd(), 'aws_batch_files'))
        path_local = os.path.join(parent_path, name)
        bucket_blob_path = path_local[path_local.index(self.project_name) + len(self.project_name):].replace('\\','/')
        print(self.folder_path + bucket_blob_path)
        self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)

        print(f'uploaded dag successfully to: {self.folder_path}/{bucket_blob_path}')


if __name__ == "__main__":
    AWS_PROFILE = 'gaia_admin'
    s3_uploader = S3Uploader(AWS_PROFILE=AWS_PROFILE)

    # parent_path = os.path.abspath(os.path.join(os.getcwd(), 'aws_batch_files'))
    # script_path = os.path.join(parent_path, 'scripts')

    type = ''
    if sys.argv and len(sys.argv) > 1:
        type = sys.argv[1]
    if not type:
        raise Exception('type must be enter')

    s3_uploader.upload_files_to_bucket(type)
    # s3_uploader.upload_dag2()

    # Upload spark_script.py to the "scripts" folder
    # s3_uploader.upload_script('spark_script.py', 'scripts')

    # Upload your_airflow_dag.py to the "dags" folder
    # s3_uploader.upload_dag('dag.py', 'dags')

    # s3_uploader.start_paused_dag('emr_cluster_management')