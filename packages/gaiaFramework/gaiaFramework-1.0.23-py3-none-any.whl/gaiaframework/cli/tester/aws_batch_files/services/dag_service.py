import boto3
from boto3.s3.transfer import TransferConfig
from datetime import datetime, timezone
import sys
import requests
import os
import subprocess
from json import load as json_load
from airflow.models import DagBag, DagRun, DagModel
from airflow.api.common.trigger_dag import trigger_dag, _trigger_dag
from airflow.api.client.local_client import Client
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow import DAG


class DagService:
    def __init__(self, AWS_PROFILE=None):

        if AWS_PROFILE:
            boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.storage_client = boto3.resource('s3')
        self.mwaa_client = boto3.client('mwaa')

        file_path = sys.modules[self.__class__.__module__].__file__
        curr_path = file_path[:file_path.rfind("aws_batch_files")]
        self.project_folder_path = curr_path

        AIRFLOW_HOME = self.project_folder_path + '/aws_batch_files/'
        os.environ["AIRFLOW_HOME"] = AIRFLOW_HOME
        self.run_airflow_db_init(AIRFLOW_HOME)

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
        self.cluster_name = stage_config['cluster_conf']['managed_cluster']['cluster_name']
        self.cluster_duration = stage_config['cluster_duration_sec']
        self.managed_cluster = stage_config['cluster_conf']['managed_cluster']
        if self.unique_iteration_id:
            self.folder_path = 'dags/' + self.project_name + self.user_id + \
                               '/unique_iteration_id_' + self.unique_iteration_id
        else:
            self.folder_path = 'dags/' + self.project_name + self.user_id + '/main'

        self.bucket_path = f's3://{self.bucket_name}/{self.folder_path}'
        self.project_path = 'projects/{project_id}/regions/{region}'.format(project_id=self.project_id,
                                                                            region=self.region)

        self.bucket = self.storage_client.Bucket(self.bucket_name)

    def run_airflow_db_init(self, AIRFLOW_HOME):
        if not os.path.exists(os.path.join(AIRFLOW_HOME, 'airflow.db')):
            try:
                subprocess.run(["airflow", "db", "init"], check=True)
                print("airflow db init completed successfully.")
            except subprocess.CalledProcessError as e:
                print("Error running airflow db init:", e)
        else:
            self.get_dags_list()

    def get_dags_list(self):
        dag_ids = DagBag(include_examples=False).dag_ids
        for id in dag_ids:
            print('id', id)

    def instantiate_dag(self, dag_id):
        token = self.mwaa_client.create_cli_token(Name=self.config['environment'])
        url = f"https://{token['WebServerHostname']}/aws_mwaa/cli"
        body = 'dags trigger ' + dag_id
        headers = {
            'Authorization': 'Bearer ' + token['CliToken'],
            'Content-Type': 'text/plain'
        }
        requests.post(url, data=body, headers=headers)

    def start_paused_dag(self, dag_id):
        dag_bag = DagBag(dag_folder=self.project_folder_path + 'aws_batch_files/')
        print('dag_bag', dag_bag)
        if dag_id in dag_bag.dags:
            print('dag_id', dag_id)
            # dag_model = DagModel.get_current(dag_id)
            # print('dag_model', dag_model)
            dag = dag_bag.dags[dag_id]
            print('dag', dag)
            execution_date = datetime.now().replace(tzinfo=timezone.utc)
            run_id = f"manual__{execution_date.isoformat()}"
            conf = {}  # You can provide any additional configuration if needed
            execution_date_str = execution_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            trigger_dag(dag_id, run_id=run_id, execution_date=execution_date, conf=conf)
            # print(';execution_date', execution_date)
            # _trigger_dag(
            #     dag_id=dag_id,
            #     dag_bag=dag_bag,
            #     run_id=run_id,
            #     conf=conf,
            #     execution_date=execution_date,
            #     replace_microseconds=True,
            # )
            print(f"Started DAG run for {dag_id} manually with run_id: {run_id}")
        else:
            print(f"DAG {dag_id} not found in DAG bag.")

    def start_dag_by_id(self, dag_id):
        # Get the current time as the execution_date
        execution_date = datetime.now().replace(tzinfo=timezone.utc)

        # Load the DAG from the DagBag
        dag_bag = DagBag(dag_folder=self.project_folder_path + 'aws_batch_files')
        dag = dag_bag.get_dag(dag_id)

        if dag is None:
            print(f"DAG '{dag_id}' not found.")
            return

        # Instantiate a DagRun to trigger the DAG
        dag_run = DagRun.find(dag_id=dag_id, execution_date=execution_date)

        # If the DagRun doesn't exist, create it
        if dag_run is None:
            dag_run = DagRun(dag_id=dag_id, execution_date=execution_date)
            dag_run.run_id = f"manual__{execution_date.isoformat()}"
            dag_run.state = "manual"
            dag_run.create()

            print(f"DAG '{dag_id}' has been instantiated with execution_date {execution_date}.")
        else:
            with DAG(
                    dag_id="trigger_existing_dag_run",
                    start_date=execution_date,
                    schedule_interval=None,
                    catchup=False
            ) as dag:
                trigger_operator = TriggerDagRunOperator(
                    task_id="trigger_task",
                    trigger_dag_id=dag_id,
                    execution_date=execution_date
                )

            # Start the execution of the main DAG
            dag.run()
            print(f"DAG '{dag_id}' has been instantiated with execution_date {execution_date}.")

    def upload_dag(self):
        name = 'dag/dag.py'
        parent_path = os.path.abspath(os.path.join(os.getcwd(), 'aws_batch_files'))
        path_local = os.path.join(parent_path, name)
        bucket_blob_path = path_local[path_local.index(self.project_name) + len(self.project_name):].replace('\\','/')
        print(self.folder_path + bucket_blob_path)
        self.bucket.upload_file(path_local, self.folder_path + bucket_blob_path)

        print(f'uploaded dag successfully to: {self.folder_path}{bucket_blob_path}')

    def upload_dag2(self, local_path, remote_folder):
        remote_key = f"{remote_folder}/{local_path.split('/')[-1]}"
        remote_path = remote_key
        parent_path = os.path.abspath(os.path.join(os.getcwd(), 'aws_batch_files'))
        path_local = os.path.join(parent_path, local_path)
        print('remote_path',remote_path)
        self.bucket.upload_file(path_local, remote_path)
        print(f"Uploaded {path_local} to s3://{remote_path}")


if __name__ == "__main__":
    AWS_PROFILE = 'gaia_admin'
    s3_uploader = DagService(AWS_PROFILE=AWS_PROFILE)

    type = ''
    if sys.argv and len(sys.argv) > 1:
        type = sys.argv[1]
    if not type:
        raise Exception('type must be enter')
    if type == 'import':
        s3_uploader.upload_dag()
        # s3_uploader.upload_dag2('dag/dag.py', 'dags')
    if type == 'trigger':
        dag_id = ''
        if sys.argv and len(sys.argv) > 2:
            dag_id = sys.argv[2]
        if not dag_id:
            raise Exception('dag_id must be enter')
        # dag_id = 'emr_cluster_management'
        s3_uploader.instantiate_dag(dag_id)

# python aws_batch_files\services\dag_service.py trigger gaia-airflow-test