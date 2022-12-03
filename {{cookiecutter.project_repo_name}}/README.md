# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Runbook

### 1. Setup Service Account:

1. Create a Google Cloud Project. See [Getting started with Google Cloud API](https://cloud.google.com/apis/docs/getting-started).
2. Enable Google Sheets API for the project
3. Create Service Account Credentials
4. Generate and Download JSON key for the Service Account
5. Share the Google sheet with the Service Account's email

### 2. Save Service Account Key and Sheet ID and range:

1. Store downloaded service account key either in:
- Variable `SERVICE_ACCOUNT_INFO` in `.streamlit/secrets.toml` as a string, or
- in the filename specified in `config/default.yml`
2. Set google sheet id and range in `config/default.yml`

### 3. Install packages

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run dashboard:
```
streamlit run app.py
```
