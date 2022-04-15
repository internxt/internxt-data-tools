from google.oauth2 import service_account
from google.cloud import bigquery


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