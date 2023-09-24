[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)

# docker-selenium-lambda

This is built with headless chrome and selenium on container image on AWS Lambda

This image goes with these versions.
- Python 3.11.5
- chromium 114.0.5735.0
- chromedriver 114.0.5735.90
- selenium 4.12.0

## Running the question-scraping function

```bash
$ npm install -g serverless # skip this line if you have already installed Serverless Framework
$ export AWS_REGION=ap-southeast-1 # You can specify region or skip this line.
$ sls # creates the sls project. you will be redirected to the browser to key in your AWS credentials
$ sls deploy # deploys the image
$ sls invoke --function demo --data '{"leetcode_id_start": 5, "num_questions": 3}' # first way to run the function
sls invoke --function demo --path input.json # alternative way to run the function
```

Credits: [this repo](https://github.com/umihico/docker-selenium-lambda) helped me with using selenium on docker images
