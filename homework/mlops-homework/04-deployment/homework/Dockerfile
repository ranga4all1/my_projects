FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "score.py", "./" ]

RUN chmod +x /app/score.py

ENTRYPOINT [ "/app/score.py" ]

CMD ["python", "score.py", "2022", "10"]

COPY [ "/app/*.parquet", "output/yellow" ]
