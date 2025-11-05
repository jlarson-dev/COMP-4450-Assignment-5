# COMP-4450-Assignment-5

This application contains two microservices: a monitoring dashboard which can detect data drift, and a lightweight FastAPI backend that logs predictions based on posted reviews. There is also an evaluation script in the root directory that can ingest test data, utilizing the API to make predictions.

## Architecture

The folder/file structure of the project is the following.
```
C:.
│   evaluate.py
│   Makefile
│   README.md
│   test.json
│
├───api
│   │   Dockerfile
│   │   main.py
│   │   Makefile
│   │   requirements.txt
│   │   sentiment_model.pkl
│   │
│   └───__pycache__
│           main.cpython-311.pyc
│
├───logs
│       prediction_logs.json
│
└───monitoring
        app.py
        Dockerfile
        IMDB Dataset.csv
        Makefile
        prediction_logs.json
        requirements.txt
```

## How to Use Each Service

There is a container for each of the microservices, each with its respective Dockerfile. The root directory contains a Makefile which manages both of the containers. Here are the steps to run the application.
1. Clone the repository `git clone https://github.com/jlarson-dev/COMP-4450-Assignment-5.git`
2. Navigate to the root directory `cd ./COMP-4450-Assignment-5.git`
3. Build the images `make build`
3. Run the images `make run`

You are now ready to use the application! Here are specific steps for each service.

### Evaluation Script

From the root directory of the app, run `python3 evaluate.py`. This will run the script which iterates over the test.json file in the same directory, logging predictions of the sentiment for each review using the predict endpoint from the API service.

### API

The API documentation can be found at http://127.0.0.1:8000/docs

#### Endpoints
http://127.0.0.1:8000/health: GET endpoint confirming whether the API is running or not. 

**Example:** `curl http://127.0.0.1:8000/health`

http://127.0.0.1:8000/predict: POST endpoint that takes an input movie review and the true sentiment of the reviewer and returns the predicted sentiment of the review (positive or negative). It then logs the predicted sentiment, true sentiment, length of the review, and the time stamp.

**Example:** 
curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"text": "The movie was amazing and full of heart.", "true_sentiment": "positive"}'

### Monitoring Dashboard

Visit the dashboard at http://localhost:8501/

The dashboard posts the accuracy of the model according to the test data from the evaluation script, it shows the distributions of review lengths between the IMDB dataset and the logged reviews, and the distribution of positive and negative reviews from each dataset.

There is a warning banner that will appear at the top of the dashboard as well when the accuracy drops below 80%.