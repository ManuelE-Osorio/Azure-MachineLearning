## Build pipeline (have to crreate components .yaml file)

from azure.ai.ml import load_component
parent_dir = ""

prep_data = load_component(source=parent_dir + "./prep-data.yml")
train_decision_tree = load_component(source=parent_dir + "./train-model.yml")

from azure.ai.ml import Input
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.dsl import pipeline

@pipeline()
def diabetes_classification(pipeline_job_input):
    clean_data = prep_data(input_data=pipeline_job_input)
    train_model = train_decision_tree(training_data=clean_data.outputs.output_data)

    return {
        "pipeline_job_transformed_data": clean_data.outputs.output_data,
        "pipeline_job_trained_model": train_model.outputs.model_output,
    }

pipeline_job = diabetes_classification(Input(type=AssetTypes.URI_FILE, path="azureml:diabetes-data:1"))

print(pipeline_job)

# change the output mode
pipeline_job.outputs.pipeline_job_transformed_data.mode = "upload"
pipeline_job.outputs.pipeline_job_trained_model.mode = "upload"
# set pipeline level compute
pipeline_job.settings.default_compute = "aml-cluster"
# set pipeline level datastore
pipeline_job.settings.default_datastore = "workspaceblobstore"

# print the pipeline job again to review the changes
print(pipeline_job)



# submit job to workspace
pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="pipeline_diabetes"
)
pipeline_job
     
