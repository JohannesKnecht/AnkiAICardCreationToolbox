# AnkiAICardCreationToolbox
App to create Anki Cards using AI 

# Infrastructure
Infrastructure is handled using Terraform.


# Create Service Account
PROJECT_ID=ankiaicardcreationtoolbox
SA_NAME=ankiaicardcreationtoolboxsa
gcloud iam service-accounts create $SA_NAME \
  --display-name "ankiaicardcreationtoolboxbackend service account" \
  --project @$PROJECT_ID
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/editor"
gcloud iam service-accounts keys create cicd.json \
  --iam-account=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com


# Give cloud run access to secret. todo: add to iac
COMPUTE_SERVICE_ACCOUNT=<id>-compute@developer.gserviceaccount.com
gcloud secrets add-iam-policy-binding openai \
  --member="serviceAccount:$COMPUTE_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"