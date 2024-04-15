## Using MLFlow to track jobs


import mlflow
experiments = mlflow.search_experiments()
for exp in experiments:
    print(exp.name)

experiment_name = "diabetes-training"
exp = mlflow.get_experiment_by_name(experiment_name)
print(exp)

query = "metrics.AUC > 0.8 and tags.model_type = 'LogisticRegression'"
mlflow.search_runs(exp.experiment_id, filter_string=query)