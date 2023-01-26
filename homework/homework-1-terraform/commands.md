## Refresh service-account's auth-token for this session
`gcloud auth application-default login`

## Initialize state file (.tfstate)
`terraform init`

## Check changes to new infra plan
`terraform plan -var="project=<your-gcp-project-id>"`


## Create new infra
`terraform apply -var="project=<your-gcp-project-id>"`

## Optional - Delete infra after your work, to avoid costs on any running services
`terraform destroy`