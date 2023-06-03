
python preprocess_data.py \
  --wandb_project WANDB-NYC-TAXI \
  --wandb_entity ranga4all1 \
  --raw_data_path '../data' \
  --dest_path ./output


python train.py \
  --wandb_project WANDB-NYC-TAXI \
  --wandb_entity ranga4all1 \
  --data_artifact "ranga4all1/WANDB-NYC-TAXI/NYC-Taxi:v0"


python sweep.py \
  --wandb_project WANDB-NYC-TAXI \
  --wandb_entity ranga4all1 \
  --data_artifact "ranga4all1/WANDB-NYC-TAXI/NYC-Taxi:v0"