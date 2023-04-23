# Car Type CNN Classifier

This is a classic computer vision task to classify 196 car models using deep learning convolutional neural networks. The full details can be found in the [PDF document](%5BAIML%5D%20Assessment%201A%20-%20Image%20Classification%20model.pdf).

It is a complete, end-to-end MLE exercise going from data exploration and cleaning, to research and modeling, to local inference, and finally to containerization and deployment.

The dataset can be downloaded [here](https://hometeamsnt-my.sharepoint.com/personal/benjamin_cham_hometeamsnt_onmicrosoft_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fbenjamin%5Fcham%5Fhometeamsnt%5Fonmicrosoft%5Fcom%2FDocuments%2FStanford%20Cars%20Dataset%2Ezip&parent=%2Fpersonal%2Fbenjamin%5Fcham%5Fhometeamsnt%5Fonmicrosoft%5Fcom%2FDocuments&ga=1) or from [Kaggle](https://www.kaggle.com/datasets/jessicali9530/stanford-cars-dataset?resource=download).

## Overview

The detailed approaches and thought processes are described clearly in the [Jupyter Notebook](modelling.ipynb) and the CNN model selected was the pretrained [EfficientNetV2 B3](https://keras.io/api/applications/efficientnet_v2/#efficientnetv2b3-function) with the `imagenet` weights.

The best model achieved a macro accuracy of **94.2%** on the combined train and validation sets.

After training a few models, the best model is then containerized using Docker and served through a POST endpoint in a FastAPI app. You can setup your local machine to run the docker container using the steps below.

Unfortunately there was little time to further optimize the model due to personal reasons but ideally, here are some ways to improve the model performance:

- Data Augmentation: Scaling, flipping, cropping, rotation/brightness/contrast changes, etc. can increase the generalizability of the model
- More Powerful Models: Although a bigger model might not always be better, it might still give a performance boost
- More Data: For this task, other data sources are disallowed but for real-world use-cases, more data is often paramount to robust models especially for car types, which have an abundance of possibilities
- Unclassified Class: Since the model might face unknown images or never-before-seen car types, an unclassified class can be trained up, although it might be hard to prepare the data for this since "unclassified" can be anything

## Setup

The car-classifier FastAPI app is dockerized and can be started be following these steps:

1. Install Docker on your local machine if not yet installed
2. Clone this repository to your local machine and navigate to it

```bash
git clone https://github.com/zhermin/car-classifier.git
cd car-classifier
```

3. Build the Docker image with tag name `car-classifier`

```bash
docker build -t car-classifier .
```

4. Run the container on port 4000

```bash
docker run -p 4000:4000 car-classifier
```

5. Try out the app at [localhost:4000](localhost:4000)

## Endpoints

### `[GET] /`

Home route with a simple status JSON message:

```json
{ "status":"The car classification service is running!" }
```

### `[GET] /ping`

Polls the service to check if it is alive and running.

The response should be in JSON serialised format with `key = "message"` and `value = "pong"`:

```json
{ "message":"pong" }
```

### `[POST] /infer`

Uploads an image for inference to receive the inference result.

You may test this endpoint using FastAPI's auto-generated docs at [localhost:4000/docs](localhost:4000/docs). First click `Try it out` and upload an image by clicking `Choose File`.

Then click `Execute` to receive the predicted car type in a JSON serialised format with `key = "class"` and `value = "Make, Model, Year"`, for example:

```json
{ "class":"Bentley Continental GT Coupe 2007" }
```

## Conclusion

It was really interesting setting up the entire ML pipeline in such a short time (1-2 days). Hopefully this showcases a decent understanding and expertise in these technologies. These are exciting challenges that I would love to work on especially when it comes to productionizing machine learning products since models should not just live in notebooks but instead be scaled up and served to real-world users to deliver business impacts and value propositions.
