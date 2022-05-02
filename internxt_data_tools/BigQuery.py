from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd


class BigQuery:
  def __init__(self, key_path):
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    self.client = bigquery.Client(credentials=credentials,
                                  project=credentials.project_id)

  def store_dataframe(self, df, table_name):
    job = self.client.load_table_from_dataframe(df, table_name)
    return job

  def download_table(self, query):
    dataframe = (
        self.client.query(query)
        .result()
        .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
            create_bqstorage_client=True,
        )
    )
    return dataframe

  def latest_metadata(self, table_name, metadata_table='inxt-analytics.metadata.load_history'):
    query = f"""SELECT * FROM `{metadata_table}` WHERE table_name like '{table_name}' ORDER BY timestamp DESC LIMIT 1"""
    df = self.download_table(query)
    return df.iloc[0]

  def store_extraction_metadata(self,table_name,  init_date, end_date, extraction_status, metadata_table='metadata.load_history'):
    d = {'table_name': [table_name], 'timestamp': [end_date], 'timestamp_init': [init_date], 'status': [extraction_status]}
    df = pd.DataFrame(data=d)
    job = self.store_dataframe(df,metadata_table)
    return job

