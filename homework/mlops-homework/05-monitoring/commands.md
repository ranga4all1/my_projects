# Setup environment

conda create -n py11 python=3.11

conda activate py11

pip install -r requirements.txt 

mkdir config

mkdir models

mkdir data

mkdir dashboards

prefect server start

docker-compose up --build

docker-compose down

docker-compose up --detach

docker-compose ls

docker-compose ps

docker images

docker-compose down

### ------------------

## tree structure

tree
.
├── baseline_model_nyc_taxi_data.ipynb

├── config

│   ├── grafana_dashboards.yaml

│   └── grafana_datasources.yaml

├── dashboards

│   └── nyc_green_taxi_metrics.json

├── data

│   ├── green_tripdata_2023-03.parquet

│   └── reference.parquet

├── docker-compose.yml

├── evidently_metrics_calculation.py

├── homework.md

├── models

│   └── lin_reg.bin

└── requirements.txt