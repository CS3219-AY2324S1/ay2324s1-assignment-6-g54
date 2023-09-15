[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)
# ServerlessTemplate

# docker-selenium-lambda

This is minimum demo of headless chrome and selenium on container image on AWS Lambda

This image goes with these versions. [These are automatically updated and tested everyday.](https://github.com/umihico/docker-selenium-lambda/actions)

- Python 3.11.5
- chromium 114.0.5735.0
- chromedriver 114.0.5735.90
- selenium 4.12.0

## Running the demo

```bash
$ npm install -g serverless # skip this line if you have already installed Serverless Framework
$ export AWS_REGION=ap-southeast-1 # You can specify region or skip this line.
$ sls # creates the sls project. you will be redirected to the browser to key in your AWS credentials
$ sls deploy # deploys the image
$ sls invoke --function demo --data '{"completed_upto": 5, "num_questions": 3}' 
sls invoke --function demo --path input.json
```

## Public image is available

If you want your image simplier and updated automatically, rewrite the Dockerfile with the following commands:

```Dockerfile
FROM umihico/aws-lambda-selenium-python:latest

COPY main.py ./
CMD [ "main.handler" ]
```

Available tags are listed [here](https://hub.docker.com/r/umihico/aws-lambda-selenium-python/tags)
