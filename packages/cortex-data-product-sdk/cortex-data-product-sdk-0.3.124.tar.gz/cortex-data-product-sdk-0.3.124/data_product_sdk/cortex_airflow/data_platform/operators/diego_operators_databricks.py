import logging
import pandas as pd
import requests
from datetime import datetime
import json

DIEGO_MAX_ROWS = 10000000
log = logging.getLogger(__name__)


class DiegoOperatorDatabricks():
    def __init__(self, task_id, cube_id: str=None, platform_url: str=None, ignore_empty_dataframe=False, full_load=False, multiple_addresses:list(dict())=list(dict()),**kwargs) -> None:
        """
        Operator that expects a python_callable that returns or yields a pandas Dataframe to process and insert the corresponding Dataframe into a csv to Diego

        :param task_id: id of the this task
        :param cube_id: id of the cube to be stored the data
        :param platform_url: id of the platform to be stored the data
        :param ignore_empty_dataframe: will consider a empty dataframe returned from python_callable as a success
        :param full_load: wheter or not the destiny cube will have its data erased before inserting new data. Values True or False (default)
        :param multiple_addresses: list of dicts. Ex.: [{'platform_url':'https://xpto.com', 'cube_id':'123456789101112'}]
        """
        self.cube_id = cube_id
        self.platform_url = platform_url
        self.ignore_empty_dataframe = ignore_empty_dataframe
        self.task_id = task_id
        self.full_load = full_load
        self.multiple_addresses = multiple_addresses

    def send_file_path_to_diego(self, cube_id, file_path, platform_url):
        data_format = json.dumps({
            "destinationId": cube_id,
            "file": file_path,
            "pattern": ".*.parquet",
            "fullLoad": self.full_load
            })

        endpoint = f"{platform_url}/controller/dataloader/cube-load/s3"
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            endpoint,
            data=data_format,
            headers=headers
        )

        print(f"File sent to Diego to path {file_path}")
        print(f"Diego response {response.text}")

        return response


    def __upload_pandas_df_to_diego(self, df: pd.DataFrame, path, part_number):

        df.write.parquet(f"{path}/{part_number}.parquet")

        return True


    def execute(self, df):
        temp_file_path = f"cortex-data-lakehouse-metastore-development/temp-files-diego/{self.task_id}/{self.cube_id}/{str(hash(datetime.utcnow().isoformat()))}"

        if df.first() == None:
            print("Empty dataframe")
            return False

        self.__upload_pandas_df_to_diego(df=df, path=f"s3://{temp_file_path}", part_number=1,)

        response = self.send_file_path_to_diego(self.cube_id, temp_file_path, self.platform_url)

        if not self.ignore_empty_dataframe and not response.json().get("replyId"):
            raise ValueError('There were no dataframes written to Diego. Please check if your dataframes are empty')

        return True

    def execute_multiples(self, df):

        if df.first() == None:
                print("Empty dataframe")
                return False

        for address in self.multiple_addresses:
            temp_file_path = f"cortex-data-lakehouse-metastore-development/temp-files-diego/{self.task_id}/{address.get('cube_id')}/{str(hash(datetime.utcnow().isoformat()))}"

            self.__upload_pandas_df_to_diego(df=df, path=f"s3://{temp_file_path}", part_number=1)

            response = self.send_file_path_to_diego(address.get('cube_id'), temp_file_path, address.get('platform_url'))

            if not response.json().get("replyId"):
                raise ValueError(f"There were no dataframes written to Diego.\nPlease check if your dataframes are empty\nPlatform: {address.get('platform_url')}\nCube: {address.get('cube_id')}")

        return True
