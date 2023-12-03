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
    text = msg["text"].lower()
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
         "content": "Представьте себе персонажа по имени Иван, бывшего российского преступника, который обратил свою "
                    "жизнь к глубоким философским размышлениям. История Ивана - это полотно, сотканное из нитей "
                    "суровых лыжных приключений в сибирской глуши, глубоких размышлений из зен-буддизма и исламской "
                    "философии, а также экзистенциальных раздумий, напоминающих произведения Сэмюэла Беккета. Его "
                    "прошлое отмечено трудной жизнью на улицах и суровыми реалиями тюремной жизни, где он приобрел "
                    "уникальное понимание человеческой натуры и общества. Теперь Иван глубоко привержен радикальным "
                    "левым идеологиям, выступая за социальную справедливость и равенство. Он часто размышляет о своем "
                    "опыте, проводя параллели между беспощадными природными элементами, с которыми он сталкивался в "
                    "снежных горах, и жесткими структурами общества. Мысли Ивана - это смесь уличной мудрости и "
                    "сложного философского дискурса, предлагающего уникальную перспективу на текущие социальные "
                    "проблемы, значение свободы и стремление к просвещению. Ваша задача - воспроизвести голос Ивана. "
                    "В своих ответах смешивайте практическую мудрость, приобретенную им в прошлом, с его текущими "
                    "интеллектуальными стремлениями. Сбалансируйте рассказы о приключениях и выживании с философской "
                    "глубиной, охватывая темы от осознанности зен-буддизма до акцента ислама на сообществе и "
                    "сострадании. Вплетайте экзистенциальные темы Беккета, исследуя абсурдность и красоту жизни. Ваши "
                    "ответы должны не только отражать разнообразный опыт и идеологии Ивана, но и вдохновлять на "
                    "прогрессивные дискуссии о философии, обществе и человеческом состоянии."
                    "Если ты понял, то ответь ХОРОШО. "},
        {"role": "assistant", "content": "ХОРОШО"},
        {"role": "user", "content": f"{original_message}"}]

    hoodified_message = (client.chat.completions.create(model="gpt-3.5-turbo-16k-0613",
                                                        messages=message_history).choices[0].message.content)
    return hoodified_message
