#!/usr/bin/python3.11
import time
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

account_url = "https://robotfoursbxeuw.blob.core.windows.net"
default_credential = DefaultAzureCredential()
container_name = "stblc-robot-four-processed-sbx-euw-01"
preprocessed_dir = Path("/mnt/robotfoursbxeuw/stfss-robot-four-share-sbx-euw-01")

while True:
    with BlobServiceClient(account_url, credential=default_credential) as blob_client:
        with blob_client.get_container_client(container_name) as container_client:
            while not (preprocessed_files := list(preprocessed_dir.iterdir())):
                print("No files, waiting")
                time.sleep(10)
            for preprocessed_file in preprocessed_files:
                if not preprocessed_file.name.startswith("prep_"):
                    continue
                blob_name = "post_" + preprocessed_file.name[5:]
                print(f"Post-processing {preprocessed_file} to {blob_name}...")
                with preprocessed_file.open("rb") as stream:
                    container_client.upload_blob(
                        blob_name, stream.read(), overwrite=True
                    )
                preprocessed_file.unlink()
    print("Preprocessing done, wait a little...")
    time.sleep(10)
