#!/usr/bin/python3.11
import time
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

account_url = "https://robotfoursbxeuw.blob.core.windows.net"
default_credential = DefaultAzureCredential()
container_name = "stblc-robot-four-upload-sbx-euw-01"
download_dir = Path("/mnt/robotfoursbxeuw/stfss-robot-four-share-sbx-euw-01")

while True:
    with BlobServiceClient(account_url, credential=default_credential) as blob_client:
        with blob_client.get_container_client(container_name) as container_client:
            # container_client.upload_blob("test123", "empty")
            while not (blobs := list(container_client.list_blobs())):
                print("No blobs, waiting")
                time.sleep(10)
            for blob in blobs:
                new_file_path = download_dir / ("prep_" + blob.name)
                print(f"Pre-processing {blob.name} to {new_file_path}...")
                with new_file_path.open("wb") as new_file:
                    new_file.write(container_client.download_blob(blob.name).readall())
                container_client.delete_blob(blob.name)
    print("Preprocessing done, wait a little...")
    time.sleep(10)
