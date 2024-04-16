## Model Registering (From MLFlow)

from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

model_name = 'diabetes-mlflow'
model = ml_client.models.create_or_update(
    Model(name=model_name, path='./model', type=AssetTypes.MLFLOW_MODEL)
)

## Creating a batch endpoint

from azure.ai.ml.entities import BatchEndpoint

# create a batch endpoint
endpoint = BatchEndpoint(
    name=endpoint_name,
    description="A batch endpoint for classifying diabetes in patients",
)

ml_client.batch_endpoints.begin_create_or_update(endpoint)


## Create deployment for the endpoint


from azure.ai.ml.entities import BatchDeployment, BatchRetrySettings
from azure.ai.ml.constants import BatchDeploymentOutputAction

deployment = BatchDeployment(
    name="classifier-diabetes-mlflow",
    description="A diabetes classifier",
    endpoint_name=endpoint.name,
    model=model,
    compute="aml-cluster",
    instance_count=2,
    max_concurrency_per_instance=2,
    mini_batch_size=2,
    output_action=BatchDeploymentOutputAction.APPEND_ROW,
    output_file_name="predictions.csv",
    retry_settings=BatchRetrySettings(max_retries=3, timeout=300),
    logging_level="info",
)
ml_client.batch_deployments.begin_create_or_update(deployment)

endpoint.defaults = {}

endpoint.defaults["deployment_name"] = deployment.name

ml_client.batch_endpoints.begin_create_or_update(endpoint)

## Getting data for batch job


from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

data_path = "./data"
dataset_name = "patient-data-unlabeled"

patient_dataset_unlabeled = Data(
    path=data_path,
    type=AssetTypes.URI_FOLDER,
    description="An unlabeled dataset for diabetes classification",
    name=dataset_name,
)
ml_client.data.create_or_update(patient_dataset_unlabeled)

patient_dataset_unlabeled = ml_client.data.get(
    name="patient-data-unlabeled", label="latest"
)

## Submit the job to a pipeline

from azure.ai.ml import Input
from azure.ai.ml.constants import AssetTypes

input = Input(type=AssetTypes.URI_FOLDER, path=patient_dataset_unlabeled.id)
job = ml_client.batch_endpoints.invoke(
    endpoint_name=endpoint.name, 
    input=input)

ml_client.jobs.get(job.name)