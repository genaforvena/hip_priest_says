# Hip Priest Says Telegram Bot

This is a quick and dirty implementation of a Telegram bot backend, hosted on AWS Lambda using the Serverless Application Model (SAM). The bot is designed to interact with a group chat.

## Overview

The bot is triggered by certain keywords in the chat and responds with a message generated by OpenAI's GPT-3 model. The bot's behavior is defined in the `hello_world/app.py` file.

## Setup and Deployment

To deploy this bot, you need to have the AWS SAM CLI and Docker installed on your machine. If you haven't installed them yet, you can find the instructions in the following links:

- [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Install Docker](https://docs.docker.com/get-docker/)

Once you have SAM CLI and Docker installed, you can build and deploy the bot using the following commands:

```bash
sam build --use-container
sam deploy --guided
```

During the guided deployment, SAM CLI will prompt you to enter the necessary parameters such as the stack name and AWS region.  

## Usage

Once the bot is deployed, you can add it to your Telegram group chat. The bot will start listening to the chat and respond whenever a trigger word is used in a message.  

## Note

This bot is a quick and dirty implementation. It's not intended for production use and may not handle all edge cases. Use it as a starting point for your own Telegram bot projects.  