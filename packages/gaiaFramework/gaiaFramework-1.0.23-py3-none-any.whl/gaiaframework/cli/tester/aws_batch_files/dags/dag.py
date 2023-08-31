import json

from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import (
    EmrCreateJobFlowOperator,
    EmrTerminateJobFlowOperator,
    EmrAddStepsOperator
)
# from airflow.providers.amazon.aws.transfers.s3_to_local import S3ToLocalOperator
# from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='gaia-airflow-test',
    default_args=default_args,
    schedule_interval=None,  # Set to None to prevent automatic scheduling
    is_paused_upon_creation=True,  # Start the DAG in a paused state
    # schedule_interval=timedelta(days=1),
)

bucket_name = 'gaia-aws-airflow-try'

cluster_config = {
    "Name": "MyEMRCluster",
    "LogUri": f"s3://{bucket_name}/",
    "ReleaseLabel": "emr-6.3.0",  # EMR version
    "Applications": [{"Name": "Spark"}],  # Example application
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master nodes",
                "Market": "SPOT",
                "InstanceRole": "MASTER",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1,
            },
            {
                "Name": "Worker nodes",
                "Market": "SPOT",
                "InstanceRole": "CORE",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 2,
            },
        ],
        "KeepJobFlowAliveWhenNoSteps": False,
        "TerminationProtected": False,
    },
}

# Create EMR cluster
create_cluster = EmrCreateJobFlowOperator(
    task_id="create_cluster",
    job_flow_overrides=cluster_config,
    aws_conn_id="aws_default",
    dag=dag,
)

# Submit Spark job to EMR cluster
submit_spark_job = EmrAddStepsOperator(
    task_id="submit_spark_job",
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_cluster')['ResponseMetadata']['RequestId'] }}",
    aws_conn_id="aws_default",
    steps=[{
        "Name": "Run Spark Job",
        "ActionOnFailure": "CONTINUE",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": ["spark-submit", "--deploy-mode", "cluster", "--class", "org.apache.spark.deploy.SparkSubmit",
                     "--master", "yarn", "--conf", "spark.yarn.submit.waitAppCompletion=false",
                     f"s3://{bucket_name}/scripts/spark_script.py", json.dumps({}), "start_time", "end_time"]
        }
    }],
    dag=dag,
)

# Terminate EMR cluster
terminate_cluster = EmrTerminateJobFlowOperator(
    task_id="terminate_cluster",
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_cluster')['ResponseMetadata']['RequestId'] }}",
    aws_conn_id="aws_default",
    dag=dag,
)

# Define task dependencies
create_cluster >> submit_spark_job >> terminate_cluster
