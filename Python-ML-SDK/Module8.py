## Configure a hyperparameter sweep job


from azure.ai.ml import command, Input
from azure.ai.ml.constants import AssetTypes

# configure job

job = command(
    code="./src",
    command="python train.py --training_data {{inputs.reg_rate}}",
    inputs={
        "diabetes_data": Input(
            type=AssetTypes.URI_FILE, 
            path="azureml:diabetes-data:1"
            ),
        "reg_rate": 0.01,
    },
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="diabetes-train-mlflow",
    experiment_name="diabetes-training", 
    tags={"model_type": "LogisticRegression"}
    )

# submit job (to test if it works, it will set reg_rate as 0.01)
returned_job = ml_client.create_or_update(job)
aml_url = returned_job.studio_url
print("Monitor your job at", aml_url)

## Defining search space

from azure.ai.ml.sweep import Choice

command_job_for_sweep = job(
    reg_rate=Choice(values=[0.01, 0.1, 1]),
)

## Configuring sweep job

# apply the sweep parameter to obtain the sweep_job
sweep_job = command_job_for_sweep.sweep(
    compute="aml-cluster",
    sampling_algorithm="grid",
    primary_metric="training_accuracy_score",  ## this is an mlflow.log_metric name
    goal="Maximize",
)

# set the name of the sweep job experiment
sweep_job.experiment_name="sweep-diabetes"

# define the limits for this sweep
sweep_job.set_limits(max_total_trials=4, max_concurrent_trials=2, timeout=7200)

returned_sweep_job = ml_client.create_or_update(sweep_job)
aml_url = returned_sweep_job.studio_url
print("Monitor your job at", aml_url)