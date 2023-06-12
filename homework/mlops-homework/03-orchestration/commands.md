# Homework

### Create conda env
    conda create -n prefect-ops python==3.9.12

    conda activate prefect-ops

    pip install -r requirements.txt

### Local prefect server
    prefect server start

    prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api


### cron job scheduling
    prefect deploy 3.4/orchestrate.py:main_flow -n taxi2 -p zoompool --cron "0 9 3 * *"

### project
    prefect project init

    prefect deploy --help

    prefect deploy 3.4/orchestrate.py:main_flow -n taxi_rmse_markdown_artifact -p zoompool

    prefect worker start -p zoompool -t process

    ### email notifications
    prefect version

    pip install prefect-email

    prefect profile ls

    prefect profile inspect

    prefect block register -m prefect_email

    python 3.4/create_email_bucket_block.py


### prefect cloud server
    prefect profile create cloud

    prefect profile ls

    prefect profile use cloud

    prefect cloud login

    prefect worker start -p zoompool -t process

    python 3.4/create_email_bucket_block.py

    prefect deploy 3.4/orchestrate.py:main_flow -n taxi_cloud_email_artifact -p zoompool

### Use automation on cloud server - e. g. e-mail notification using sendgrid e-mail block
