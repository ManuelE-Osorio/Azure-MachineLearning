az extension add -n ml -y  # install azure ml extension
az group create --name "rg-dp100-labs" --location "eastus"  # azure group creation
az ml workspace create --name "mlw-dp100-labs" -g "rg-dp100-labs" # azure ml workspace creation

# Create compute instance 

# Compute name: Name of compute instance. Has to be unique and fewer than 24 characters.
# Virtual machine size: STANDARD_DS11_V2
# Compute type (instance or cluster): ComputeInstance
# Azure Machine Learning workspace name: mlw-dp100-labs
# Resource group: rg-dp100-labs

az ml compute create --name "ci4321" --size STANDARD_DS11_V2 --type ComputeInstance -w mlw-dp100-labs -g rg-dp100-labs

# Create compute cluster


# Compute name: aml-cluster
# Virtual machine size: STANDARD_DS11_V2
# Compute type: AmlCompute (Creates a compute cluster)
# Maximum instances: Maximum number of nodes
# Azure Machine Learning workspace name: mlw-dp100-labs
# Resource group: rg-dp100-labs

az ml compute create --name "aml-cluster" --size STANDARD_DS11_V2 --max-instances 2 --type AmlCompute -w mlw-dp100-labs -g rg-dp100-labs


