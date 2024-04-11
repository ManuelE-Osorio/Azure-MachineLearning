## Connecting to workspace

from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient

try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()

# Get a handle to workspace
ml_client = MLClient.from_config(credential=credential)

## Listing datastores

stores = ml_client.datastores.list()
for ds_name in stores:
    print(ds_name.name)

## Create a datastore

from azure.ai.ml.entities import AzureBlobDatastore
from azure.ai.ml.entities import AccountKeyConfiguration

store = AzureBlobDatastore(
    name="blob_training_data",
    description="Blob Storage for training data",
    account_name="YOUR-STORAGE-ACCOUNT-NAME",
    container_name="training-data", 
    credentials=AccountKeyConfiguration(
        account_key="XXXX-XXXX"
    ),
)

ml_client.create_or_update(store)

## Create dataset
#Create URI File

from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

my_path = './data/diabetes.csv'

my_data = Data(
    path=my_path,
    type=AssetTypes.URI_FILE,
    description="Data asset pointing to a local file, automatically uploaded to the default datastore",
    name="diabetes-local"
)

ml_client.data.create_or_update(my_data)

# Create URI Folder

from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

datastore_path = 'azureml://datastores/blob_training_data/paths/data-asset-path/'

my_data = Data(
    path=datastore_path,
    type=AssetTypes.URI_FOLDER,
    description="Data asset pointing to data-asset-path folder in datastore",
    name="diabetes-datastore-path"
)

ml_client.data.create_or_update(my_data)

# Create ML Table

from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

local_path = 'data/'

my_data = Data(
    path=local_path,
    type=AssetTypes.MLTABLE,
    description="MLTable pointing to diabetes.csv in data folder",
    name="diabetes-table"
)

ml_client.data.create_or_update(my_data)

## Reading Data

# Reading ML Table

import mltable

registered_data_asset = ml_client.data.get(name='diabetes-table', version=1)
tbl = mltable.load(f"azureml:/{registered_data_asset.id}")
df = tbl.to_pandas_dataframe()
df.head(5)

## using data in a JOB

from azure.ai.ml import Input, Output
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml import command

# configure input and output
my_job_inputs = {
    "local_data": Input(type=AssetTypes.URI_FILE, path="azureml:diabetes-local:1")
}

my_job_outputs = {
    "datastore_data": Output(type=AssetTypes.URI_FOLDER, path="azureml://datastores/blob_training_data/paths/datastore-path")
}

# configure job
job = command(
    code="./src",
    command="python move-data.py --input_data ${{inputs.local_data}} --output_datastore ${{outputs.datastore_data}}",
    inputs=my_job_inputs,
    outputs=my_job_outputs,
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="move-diabetes-data",
    experiment_name="move-diabetes-data"
)

# submit job
returned_job = ml_client.create_or_update(job)
aml_url = returned_job.studio_url
print("Monitor your job at", aml_url)