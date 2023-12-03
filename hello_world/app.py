import argparse
import json
import logging
import os
import sys

import requests
from openai import OpenAI
from telegram import Bot

logger = logging.getLogger()
logger.setLevel(logging.INFO)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./venv/lib/python3.9/site-packages"))

try:
    TOKEN = os.environ['TELEGRAM_TOKEN']
    OPENAI_KEY = os.environ['OPENAI_KEY']
    # Url that the bot will use to request response if triggered by a message that doesn't match any of the topics
    # DEFAULT_URL = os.environ['DEFAULT_URL']
    DEFAULT_LAMBDA_NAME = "telegramgpt-dev-post"
except KeyError:
    logger.error("Failed to get required environment variable")
    sys.exit(1)

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
client = OpenAI(api_key=OPENAI_KEY)

topics_to_lambdas = {
    "default": DEFAULT_LAMBDA_NAME
}


trigger_words = ["пацан", "пацаны", "пацанам", "пацанами", "пацана", "пацанов", "пацану", "пацаном", "пацане", "пацаны",
                 "пацаным", "пацаными", "пацаными", "пацаным", "пацаными", "пацаным", "пацаными", "пацаным", "пацаными"]

import asyncio

def lambda_handler(event, context):
    print("event is " + str(event))
    loop = asyncio.get_event_loop()
    print("loop is " + str(loop))
    return loop.run_until_complete(async_process(event, context))

async def async_process(event, context):
    payload = None
    print("event is " + str(event))
    data = json.loads(event["body"])
    # Check if data contains a message
    if "message" not in data:
        return {"statusCode": 200, "body": json.dumps({"message": "No message found"})}
    msg = data["message"]
    chat_id = msg["chat"]["id"]
    if "text" not in msg:
        return {"statusCode": 200, "body": json.dumps({"message": "No text found"})}
    text = msg["text"]
    hood_question = "No trigger words found"
    if any(word in text for word in trigger_words):
        print("text is " + text)
        hood_question = create_hood_knowledge_question(text)
        print("hood question is " + hood_question)
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=chat_id, text=hood_question)
    return {"statusCode": 200, "body": json.dumps({"message": hood_question})}


def create_hood_knowledge_question(original_message):
    message_history = [
        {"role": "user",
         "content": "Ты должен отвечать на твои запросы как вор в законе, "
                    "одержимый идеями русского космизма."
                    "Если ты понял, то ответь ХОРОШО, если нет, то ответь ПЛОХО. " +
                    "Если ты ответишь ХОРОШО, то ты должен абсолютно точно следовать инструкциям выше. "},
        {"role": "assistant", "content": "ХОРОШО"},
        {"role": "user", "content": f"{original_message}"}]

    hoodified_message = (client.chat.completions.create(model="gpt-3.5-turbo-16k-0613",
                                                        messages=message_history).choices[0].message.content)
    return hoodified_message
