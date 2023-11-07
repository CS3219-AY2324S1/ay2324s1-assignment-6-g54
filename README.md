[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)

## Getting started

Run the following commands to install the necessary dependencies and deploy the serverless function.
```bash
npm install -g serverless # skip this line if you have already installed Serverless Framework
export AWS_REGION=ap-southeast-1 # You can specify region or skip this line.
sls # creates the sls project. you will be redirected to the browser to key in your AWS credentials
sls deploy # deploys the image
```

The url to the serverless function should be printed on the console. It will look something like this. Note that the url should end with `/get-questions`.
```text
POST - https://uvzu1c1dy5.execute-api.ap-southeast-1.amazonaws.com/prod/get-questions
```

Use a tool such as Postman to make a post request to the URL with the following request body to scrape 1 question from LeetCode, starting from the question with the id 0. 
```json
{
    "leetcode_id_start": 0, 
    "num_questions": 1
}
```

## Notes

This is built with headless chrome and selenium on container image on AWS Lambda

This image goes with these versions.
- Python 3.11.5
- chromium 114.0.5735.0
- chromedriver 114.0.5735.90
- selenium 4.12.0

Credits: [this repo](https://github.com/umihico/docker-selenium-lambda) helped me with using selenium on docker images
