import json
import time
import boto3

# BUCKET = 's3://gaia-data-room-v1'
# DATABASE_NAME = "athena_tutorial"
# RESULT_OUTPUT_LOCATION = f"{BUCKET}/queries/"

class AthenaDb:
    debug = False,
    AWS_PROFILE = None
    session = None

    bucket_name = None
    bucket = None
    db_name = None
    result_output_queries = None

    def __init__(self, AWS_PROFILE, debug, bucket_name, db_name, result_output_queries):
        self.AWS_PROFILE = AWS_PROFILE
        self.debug = debug
        if self.AWS_PROFILE:
            boto3.setup_default_session(profile_name=self.AWS_PROFILE)
        self.s3_client = boto3.client('s3')
        self.athena_client = boto3.client("athena")
        # try:
        #     self.session = boto3.Session(profile_name=AWS_PROFILE)
        # except:
        #     raise
        self.bucket_name = bucket_name
        self.bucket = f's3://{bucket_name}'
        self.db_name = db_name
        self.result_output_queries = f'{self.bucket}/{result_output_queries}'
        self.create_bucket()

    def create_bucket(self):
        # s3 = self.session.resource('s3')
        # Create the bucket with the desired settings
        try:
            bucket = self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                ACL='private',
                ObjectLockEnabledForBucket=True
            )

            # s3_client = self.session.client('s3')
            response = self.s3_client.put_public_access_block(
                Bucket=self.bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            if self.debug:
                print(f'successfully created bucket {self.bucket_name}')
            return True
        except Exception as e:
            if self.debug:
                print(f'failed to create bucket {self.bucket_name}, ERROR - {str(e)}')
            return False

    def create_database(self):
        query = f"create database {self.db_name}"
        return self.run_query(query)

    # TABLE_DDL = "funding_data.ddl"

    def create_table(self, table_name):
        query = self.get_ddl(table_name)
        return self.run_query(query)
        # with open(file) as f:
        # response = self.athena_client.start_query_execution(
        #     QueryString=f.read(),
        #     ResultConfiguration={"OutputLocation": self.result_output_queries}
        # )
        #
        # return response["QueryExecutionId"]

    def repair_partition(self, table_name):
        query = f'MSCK REPAIR TABLE {self.db_name}.{table_name}'
        return self.run_query(query)

    def drop_table(self, table_name):
        query = f'DROP TABLE {self.db_name}.{table_name}'
        return self.run_query(query)

    def get_ddl(self, table_name):
        ddl = f'''
            CREATE EXTERNAL TABLE IF NOT EXISTS
            {self.db_name}.{table_name} (
              Permalink string,
              Company string,
              NumEmps string,
              Category string,
              City string,
              State string,
              FundedDate string,
              RaisedAmt string,
              RaisedCurrency string,
              Round string
            )
            PARTITIONED BY(year int)
            ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
            STORED AS TEXTFILE
            LOCATION 's3://gaia-data-room-v1/athena/db/gaia_db/'
            TBLPROPERTIES (
                "skip.header.line.count"="1"
            );
        '''
        return ddl

    def get_num_rows(self, table_name):
        query = f"SELECT COUNT(*) from {self.db_name}.{table_name}"
        return self.run_query(query)

    def get_rows(self, table_name, limit, offset=0):
        query = f"SELECT * from {self.db_name}.{table_name} OFFSET {offset} LIMIT {limit}"
        return self.run_query(query)

    def run_query(self, query):
        results = None
        try:
            self.log('start running query', query)
            response = self.athena_client.start_query_execution(
                QueryString=query,
                ResultConfiguration={"OutputLocation": self.result_output_queries}
            )
            exec_id = response["QueryExecutionId"]
            status = 'RUNNING'
            while status in ['RUNNING', 'QUEUED']:
                response = self.athena_client.get_query_execution(QueryExecutionId=exec_id)
                status = response['QueryExecution']['Status']['State']
                if status in ['RUNNING', 'QUEUED']:
                    print("Query still running...")
                    time.sleep(1)  # Wait for 1 seconds before polling again

            self.log('end running query', query)
            if status == 'SUCCEEDED':
                results = self.get_query_results(exec_id)
            else:
                print(f"Query execution failed with status: {status}")
            results = self.get_query_results(exec_id)
        except Exception as e:
            if self.debug:
                print(f'something was wrong with your query {query}', str(e))
        return results

    def get_query_results(self, execution_id):
        response = self.athena_client.get_query_results(
            QueryExecutionId=execution_id
        )

        results = response
        if 'ResultSet' in results and 'Rows' in response['ResultSet']:
            results = self.results_to_df(response)
        return results

    def results_to_df(self, results):

        result_set = results['ResultSet']
        columns = result_set['ResultSetMetadata']['ColumnInfo']
        rows = result_set['Rows']
        column_names = [column['Name'] for column in columns]

        listed_results = []
        for row in rows[1:]:  # Skip the header row
            data = row['Data']
            r = {}
            for i in range(len(data)):
                r[column_names[i]] = data[i]['VarCharValue']
            listed_results.append(r)

        return listed_results

    def has_query_succeeded(self, execution_id):
        response = self.athena_client.get_query_execution(QueryExecutionId=execution_id)
        if (
                "QueryExecution" in response
                and "Status" in response["QueryExecution"]
                and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED" or state == 'FAILED':
                return True
            else:
                return False

    def get_now(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    def log(self, message, data):
        if self.debug:
            print(self.get_now(), message, data)

athenaDb = AthenaDb(
    AWS_PROFILE='gaia_admin',
    debug=True,
    bucket_name='gaia-data-room-v1',
    db_name='gaia_db',
    result_output_queries='queries'
)
table_name = 'gaia_table'
# res = athenaDb.drop_table(table_name)
# print('drop_table', res)
# res = athenaDb.create_database()
# print('create_database', res)

# res = athenaDb.create_table(table_name)
# print('create_table', res)
# res = athenaDb.repair_partition(table_name)
# print('repair_partition', res)
res = athenaDb.get_num_rows(table_name)
print('get_num_rows', res)
# res = athenaDb.get_rows(table_name, 5, 5)
# print('get_rows', json.dumps(res, indent=2))