import os
import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import BytesIO

class GoldLayerReader:
    def __init__(self):
        # We'll set this environment variable in the next step
        self.storage_account = "tapflow"
        self.storage_key = os.getenv("AZURE_STORAGE_KEY")
        
        if not self.storage_key:
            raise ValueError("AZURE_STORAGE_KEY environment variable is not set!")

        self.connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.storage_account};AccountKey={self.storage_key};EndpointSuffix=core.windows.net"
        self.blob_service = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_name = "gold"
        self.container_client = self.blob_service.get_container_client(self.container_name)

    def read_table(self, table_name):
        """
        Reads all parquet files from a specific directory (table) in the Gold container.
        Example: read_table('daily_sales')
        """
        print(f"Reading table: {table_name}...")
        
        # List all blobs that match the folder name
        # Note: We add a trailing slash to ensure we look inside the folder
        blob_list = self.container_client.list_blobs(name_starts_with=f"{table_name}/")
        
        dfs = []
        found_files = False

        for blob in blob_list:
            # We only want the .parquet files (ignoring _SUCCESS or other metadata)
            if blob.name.endswith(".parquet"):
                found_files = True
                print(f"  - Downloading {blob.name}...")
                blob_client = self.container_client.get_blob_client(blob.name)
                
                # Download blob data into memory
                stream = BytesIO()
                blob_client.download_blob().readinto(stream)
                stream.seek(0)
                
                # Read into Pandas
                df = pd.read_parquet(stream)
                dfs.append(df)
        
        if not found_files:
            print(f"Warning: No parquet files found for table '{table_name}'")
            return pd.DataFrame() # Return empty DF if nothing found

        # Combine all parts into one big DataFrame
        return pd.concat(dfs, ignore_index=True)