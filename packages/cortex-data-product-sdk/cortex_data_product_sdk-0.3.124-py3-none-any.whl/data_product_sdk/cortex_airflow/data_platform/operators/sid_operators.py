import io
import collections
import logging
import posixpath
import pandas as pd
import time
import csv
from airflow.operators.python import PythonOperator

from data_product_sdk.cortex_airflow.data_platform.utils.sid_utils import process_date_columns, reorder_df_to_sid, upload_file, get_sid_token
from data_product_sdk.cortex_databricks.data_platform.aws_utils import S3

SID_MAX_ROWS = 10000000
log = logging.getLogger(__name__)


class SidOperator(PythonOperator):
    def __init__(self, task_id, cube_id, platform_url: str, username: str, password: str, python_callable, op_kwargs=None, ignore_empty_dataframe=False, sleep_between_chunks=30,
                 sid_chunksize=SID_MAX_ROWS, date_columns: list = None, pandas_kwargs: dict = None, retries=2, replicate_to_s3=None, **kwargs) -> None:
        """
        Operator that expects a python_callable that returns or yields a pandas Dataframe to process and insert the corresponding Dataframe into a csv to SID

        :param task_id: id of the this task
        :param retries: number of times to retry this task in case of failure
        :param cube_id: id of the cube to be stored the data
        :param platform_url: id of the platform to be stored the data
        :param username: platform login username
        :param password: platform login password
        :param python_callable: it is expected a Callable that returns a pandas DataFrame or else a TypeError will be raised
        :param op_kwargs: python_callable kwargs
        :param ignore_empty_dataframe: will consider a empty dataframe returned from python_callable as a success
        :param sleep_between_chunks: number in seconds to wait before sending another chunk of dataframe to SID
        :param sid_chunksize: max number of rows per chunk to send to SID
        :param date_columns: list of columns containing the name of the columns that are date type to be pre-processed (SID have specific requirements for date types)
        :param pandas_kwargs: dictionary containing the parameters to be forwarded to pandas 'to_csv' method
        :param replicate_to_s3: s3 path to replicate the dataframe to be uploaded to SID
        :param kwargs: all kwargs will be forwarded to the PythonOperator as parameters
        """
        if op_kwargs is None:
            op_kwargs = dict()
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        if date_columns is None:
            date_columns = list()

        super().__init__(task_id=task_id, python_callable=python_callable, op_kwargs=op_kwargs, retries=retries, **kwargs)
        self.cube_id = cube_id
        self.platform_url = platform_url
        self.username = username
        self.password = password
        self.ignore_empty_dataframe = ignore_empty_dataframe
        self.pandas_kwargs = pandas_kwargs
        self.sleep_between_chunks = sleep_between_chunks
        self.date_columns = date_columns
        self.sid_chunksize = sid_chunksize
        self.replicate_to_s3 = replicate_to_s3

    def process_date_columns(self, df):
        process_date_columns(df, date_columns=self.date_columns)
        return df

    def get_sid_token(self):
        url = f'https://{self.platform_url}/service/integration-authorization-service.login'
        token = get_sid_token(auth_endpoint=url, sid_user=self.username, user_password=self.password)

        return token

    def __upload_df_to_sid(self, df, sid_token, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        df = reorder_df_to_sid(df)
        df = self.process_date_columns(df)
        string_buffer = io.StringIO()
        df.to_csv(string_buffer, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, **pandas_kwargs)
        string_buffer.seek(0)

        log.info(f'UPLOADING DATAFRAME TO SID - SHAPE: {df.shape}')
        execution_id = upload_file(token=sid_token,
                                   cube_id=self.cube_id,
                                   file_like_object=string_buffer
                                   )

        if self.replicate_to_s3:
            string_buffer.seek(0)
            s3_bucket, s3_key = S3.get_bucket_key_from_s3_url(s3_url=self.replicate_to_s3)
            s3_key = posixpath.join(s3_key, f'{execution_id}.csv')
            s3_client = S3(bucket_name=s3_bucket)
            s3_client.put_object(data=string_buffer, s3_key=s3_key)

        return execution_id

    def __upload_pandas_df_to_sid(self, df, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        rows = df.shape[0]
        execution_ids = list()

        sid_token = self.get_sid_token()
        if rows <= self.sid_chunksize:
            execution_id = self.__upload_df_to_sid(df=df, pandas_kwargs=pandas_kwargs, sid_token=sid_token)
            execution_ids.append(execution_id)
        else:
            list_df = [df[i:i + self.sid_chunksize] for i in range(0, df.shape[0], self.sid_chunksize)]
            for i, df_element in enumerate(list_df):
                execution_id = self.__upload_df_to_sid(df=df_element, pandas_kwargs=pandas_kwargs, sid_token=sid_token)
                execution_ids.append(execution_id)
                time.sleep(self.sleep_between_chunks)

        return execution_ids

    def upload_df_to_sid(self, df, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        if isinstance(df, pd.DataFrame):
            return self.__upload_pandas_df_to_sid(df=df, pandas_kwargs=pandas_kwargs)
        else:
            raise TypeError(f'df must be a pandas DataFrame object, it is type: {type(df)}')

    def __execute_df(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f'The callable must return a pandas DataFrame object, it returned: {type(df)}')

        if self.ignore_empty_dataframe and df.shape[0] == 0:
            return []
        elif not self.ignore_empty_dataframe and df.shape[0] == 0:
            raise ValueError(f'The dataframe passed is empty {df.shape}, please use a valid dataframe')

        execution_ids = self.upload_df_to_sid(df, pandas_kwargs=self.pandas_kwargs)

        return execution_ids

    def execute(self, context):
        df = super().execute(context)
        execution_ids = list()
        if isinstance(df, collections.Iterator):
            for df_part in df:
                execution_id = self.__execute_df(df=df_part)
                execution_ids.extend(execution_id)
        else:
            execution_id = self.__execute_df(df=df)
            execution_ids.extend(execution_id)
        if not self.ignore_empty_dataframe and not execution_ids:
            raise ValueError('There were no dataframes written to SID. Please check if your dataframes are empty')
        log.info(execution_ids)

        context['task_instance'].xcom_push(key='execution_ids', value=execution_ids)
        context['task_instance'].xcom_push(key='platform_url', value=self.platform_url)
        context['task_instance'].xcom_push(key='credentials', value={'username': self.username, 'password': self.password})

