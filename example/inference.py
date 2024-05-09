import glob
import json
import torch
from tqdm import tqdm
from transformers import pipeline

device = 0 if torch.cuda.is_available() else -1
pipe = pipeline(task="image-classification", model="dima806/facial_emotions_image_detection", device=device)

predictions = {}

for img_path in tqdm(glob.glob("images/*.jpg")):
    predictions[img_path] = pipe(img_path)

json.dump(predictions, open("predictions.json", "w"))
