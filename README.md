# gallery-app
Gallery app
Gallery is an open source application for managing something. It provides basic mechanisms for adding, updating and deleting items.
Technology stack: Python 3, Flask, Flask RESTful, DynamoDB, SQS, SNS, AWS Lambda, S3

## Requirements
- MySQL Server 5.7
- Python at least 3.7.5 version

## How to install
1) Correct rds.py file with your credentials and address to database server
2) Install all requirements through pip module
3) Export environmental variable FLASK_APP with point where your application placed.
export FLASK_APP=main.py
4) Run application through command 'flask run'. It runs on localhost 5000 port.