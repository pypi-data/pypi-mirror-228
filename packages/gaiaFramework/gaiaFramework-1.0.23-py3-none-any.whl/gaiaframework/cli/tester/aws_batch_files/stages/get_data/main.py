# from gaiaframework.base.batch.stage_base import DS_Stage
# from pyspark.sql import SparkSession
# from json import loads as json_loads
# import sys
# import platform
#
#
# if __name__ == "__main__":
#
#     print('platform.python_version()', platform.python_version())
#     spark = SparkSession.builder.appName("ParameterPrint").getOrCreate()
#     if sys.argv and len(sys.argv) > 1:
#         config = json_loads(sys.argv[1])
#         try:
#             start_date = sys.argv[2]
#             end_date = sys.argv[3]
#             params = sys.argv[4]
#         except Exception as e:
#             raise Exception(f" Stage failed with error: {e}")
#     else:
#         raise Exception(f"Stage configuration not provided, Can't run stage")
#
#     print('config', config)
#     print('start_date', start_date)
#     print('end_date', end_date)
#     print('params', params)
#
#     spark.stop()



"""! @brief Get Data stage, for obtaining data from a generic source, such as a database."""
import sys
from typing import Any
from json import loads as json_loads
from pyspark.sql import SparkSession
from pyspark import __version__ as pyspark_version
import platform

from gaiaframework.base.batch.stage_base import DS_Stage

print('platform.python_version()', platform.python_version())
print('pyspark_version', pyspark_version)


##
# @file
# @brief Stage main class, implements ZIDS_Stage base class.
class GetDataStage(DS_Stage):
    """! Stage class

    Implement a stage that will later be converted to an executable job in a specific workflow.
    """

    def __init__(self, stage_config):
        """! The Stage class (generatedStageName) initializer.
        Base class will load basic configuration parameters, additional fields should be added here

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.
        """

        ##
        # @hidecallgraph @hidecallergraph
        print(f"Initializing Stage: {self.get_name()}")
        super().__init__(stage_config)
        self.bucket_path = f's3://{self.bucket_name}/{self.project_name}'
        print('self.bucket_path', self.bucket_path)

    def get_name(self):
        """! Get the stage name
        """
        return self.__class__.__name__

    def load_spark(self) -> SparkSession:   # TODO: Generalize this in order to receive config options.
        """! Basic loading of a spark session.

            Returns:
                A basic spark session
        """
        spark = SparkSession.builder \
            .appName(self.project_name) \
            .config('spark.ui.showConsoleProgress', True) \
            .config("spark.sql.parquet.compression.codec", "gzip") \
            .getOrCreate()

        print(f"Spark ID: {spark.sparkContext.applicationId}")
        return spark

    def main(self, **kwargs: Any):
        """! Executes the main functionality of the stage.

            Args:
                **kwargs : Whatever is needed for the stage to run properly.
        """
        spark_session = self.load_spark()
        df = spark_session.read. \
            options(header='true', inferSchema='true').csv(f"s3://{self.bucket_name}/example_data/retail_day.csv")

        df.printSchema()
        df.createOrReplaceTempView("sales")
        highest_price_unit_df = spark_session.sql("select * from sales where UnitPrice >= 3.0")
        # highestPriceUnitDF.write.parquet("s3://us-east1-test-4ba22677-bucket/data/highest_prices.parquet")
        highest_price_unit_df.write.mode("overwrite").parquet(f"{self.bucket_path}"
                                                              f"/example_data/highest_prices_{self.project_id}.parquet")


if __name__ == "__main__":
    """! Executes the stage by instantiating it and calling the main function.
    Set up argument condition according to the usage of the written stage

        Args:
            System argument 1 - Configuration file
            System argument 2 - Start date
    """
    if sys.argv and len(sys.argv) > 1:
        config = json_loads(sys.argv[1])
        stage = GetDataStage(config)
        try:
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            params = sys.argv[4]
            print('config', config)
            print('start_date', start_date)
            print('end_date', end_date)
            print('params', params)
            stage.update_stage_params(start_date, end_date, params)
            stage.main()
        except Exception as e:
            raise Exception(f" Stage failed with error: {e}")
    else:
        raise Exception(f"Stage configuration not provided, Can't run stage")


