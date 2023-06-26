#!/usr/bin/env python
# coding: utf-8

# import libraries
import os
import sys
import pickle

from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd


def get_paths(run_date):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    taxi_type = "yellow"
    input_file = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    # output_file = f"output/{taxi_type}/{year:04d}-{month:02d}.parquet"
    # for docker, save in /app
    output_file = f"{year:04d}-{month:02d}.parquet"

    return input_file, output_file


def read_data(filename: str):
    df = pd.read_parquet(filename)

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    return df


def prepare_dictionaries(df: pd.DataFrame):
    # preprocess data
    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    dicts = df[categorical].to_dict(orient="records")

    return dicts


def load_model():
    # load pickeled model
    with open("model.bin", "rb") as f_in:
        dv, model = pickle.load(f_in)
    return dv, model


def save_results(run_date, df, y_pred, output_file):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    # let's create an artificial ride_id column
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    # create empty results df
    df_result = pd.DataFrame()

    #  add columns
    df_result["ride_id"] = df["ride_id"]
    df_result["predictions"] = y_pred

    # Save as parquet
    df_result.to_parquet(output_file, engine="pyarrow", compression=None, index=False)


def apply_model(run_date, input_file, output_file):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    print(f"reading data from {input_file}...")
    df = read_data(input_file)

    print(f"loading model...")
    dv, model = load_model()
    dicts = prepare_dictionaries(df)

    print(f"applying model...")
    # y_pred = model.predict(dv, dicts)
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    # save above y_pred array to pandas dataframe
    y_pred = pd.DataFrame(data=y_pred, columns=["predicted"])

    # What's the standard deviation of the predicted duration for this df?
    print("std dev of predicted duration:", y_pred["predicted"].std())

    # What's the mean of the predicted duration for this df?
    print("Mean of predicted duration:", y_pred["predicted"].mean())

    print(f"writing score results to {output_file}...")
    save_results(run_date, df, y_pred, output_file)

    return output_file


def ride_duration_prediction(run_date: datetime = None):
    input_file, output_file = get_paths(run_date)

    apply_model(run_date, input_file=input_file, output_file=output_file)


def run():
    year = int(sys.argv[1])  # 2022
    month = int(sys.argv[2])  # 3
    # taxi_type = sys.argv[3]  # "yellow"

    ride_duration_prediction(run_date=datetime(year=year, month=month, day=1))


if __name__ == "__main__":
    run()
