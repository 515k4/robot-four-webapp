# Robot Dreams Azure Lesson 4

## Virtual Machines

There are 2 VMs crated via Azure Portal with this settings:

- *OS:* Linux (opensuse-leap 15.6)
- *Size:* Standard B2s (2 vcpus, 4 GiB memory)
- *Disk:* Premium SSD LRS 32GiB
- Enabled system assigned managed identity
- Public IP
- Login via SSH private key
- Backup policy: TBD

## Storage account

There is 1 Storage Account with this settings:
- Container for *upload* data
- Container for *processed* data
- File Share for *sharing* files between two VMs [using statically mounted SMB](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-linux?tabs=SLES%2Csmb311).
- Access Control: Storage Blob Data Contributor for both VMs and Web App
- Access Control: Storage File Data SMB Share Contributor for both VMs (is it needed?)
- Lifecycle: TBD
- Optimalization: Hot, Cold, Archive TBD

## Web App

This is a fork of sample FastAPI application for the Azure Quickstart [Deploy a
Python (Django, Flask or FastAPI) web app to Azure App
Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python).
For instructions on how to create the Azure resources and deploy the application
to Azure, refer to the Quickstart article.

Application is deployed from local Git using Azure CLI.

If Storage networking is enabled from selected virtual networks and IP addresses
only, you need to allow outbound public IP addresses or make the virtual network
integration and add subnet to allowed subnets.

## Backend Custom Scripts

[Azure Blob Storage client library for Python](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli&pivots=blob-storage-quickstart-scratch)

There are two Python script, each one running as systemd service on its own VM.

See `backend` directory.

## How to test it

Open Web App url, create a file. Wait few minutes and reload the page to see file in processed table.

## Next Steps

- Login to VMs using [AADSSHLogin on openSUSE](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-linux)
