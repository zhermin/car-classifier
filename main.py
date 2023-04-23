from fastapi import FastAPI, UploadFile
from contextlib import asynccontextmanager

import io
from PIL import Image

import pandas as pd
import numpy as np
import tensorflow as tf


MODEL_PARAMS = {
    "MODEL_NAME": "effnetv2b3-batch64-ep120",
    "IMG_SIZE": 300,
    "BATCH_SIZE": 64,
    "CLASS_NAMES": pd.read_csv(
        "Stanford Cars Dataset/annotations/class_names.csv", header=None
    )[0].tolist(),
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Lifespan context manager to load the ML model"""

    MODEL_PARAMS["MODEL"] = tf.keras.models.load_model(
        f"models/{MODEL_PARAMS['MODEL_NAME']}.h5"
    )
    yield
    MODEL_PARAMS.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home() -> dict:
    """App homepage."""
    return {"status": "The car classification service is running!"}


@app.get("/ping")
def ping() -> dict:
    """Ping endpoint to check if the service is running."""
    return {"message": "pong"}


@app.post("/infer")
def infer(image: UploadFile) -> dict:
    """POST endpoint to predict the class of a car image."""

    print(image.filename)

    # read the image bytes to a Pillow image object
    img = Image.open(io.BytesIO(image.file.read()))

    # preprocess the image
    img = img.resize((MODEL_PARAMS["IMG_SIZE"], MODEL_PARAMS["IMG_SIZE"]))
    img = np.array(img)
    img = tf.keras.applications.efficientnet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    # predict on the image
    prediction = MODEL_PARAMS["MODEL"].predict(img)
    prediction = np.argmax(prediction, axis=1)

    # return the class label as a JSON response
    return {"class": MODEL_PARAMS["CLASS_NAMES"][prediction[0]]}
