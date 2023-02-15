"""
Main.py
"""
import argparse
from functools import wraps
import asyncio
import json
import logging
from flask import Flask, request
import requests

import utils
from chatbot import Chatbot


logging.basicConfig(filename="logs.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("cookies_U", help="The cookie for authentication.")
args = parser.parse_args()

logging.info(args.cookies_U)

# The function to wrap the flask api into async
def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

app = Flask(__name__)


@app.route("/create_conversation", methods=['POST'])
def create_conversation():
    request_body = json.loads(request.data)
    userId = request_body["userId"]
    if userId not in utils.get_whitelist_users():
        return "You are not allowed to use this feature."

    logging.info(f"User {userId} is creating conversation.")
    cookies = {"_U": args.cookies_U}
    url = "https://www.bing.com/turing/conversation/create"
    # Send GET request
    response = requests.get(
        url,
        cookies=cookies,
        timeout=30,
    )
    if response.status_code != 200:
        raise Exception("Authentication failed")
    try:
        ConversationAPIResponseBody = response.json()
        response = {
            "conversationId": ConversationAPIResponseBody["conversationId"],
            "clientId": ConversationAPIResponseBody["clientId"],
            "conversationSignature": ConversationAPIResponseBody["conversationSignature"],
            "invocationId": 0
        }
        logging.info(response)
        return response
    except json.decoder.JSONDecodeError as exc:
        raise Exception(
            "Authentication failed. You have not been accepted into the beta.",
        ) from exc

@app.route("/chatgpt", methods=['POST'])
@async_action
async def chatgpt_reply():
    # initialize the chatbot and connect to the websocket each time.
    bot = Chatbot()
    await bot.chat_hub.connect()
    request_body = json.loads(request.data)
    prompt = request_body["prompt"]
    conversationId = request_body["conversationId"]
    clientId = request_body["clientId"]
    conversationSignature = request_body["conversationSignature"]
    invocationId = request_body["invocationId"]

    response = await bot.ask(
        prompt=prompt,
        conversationId=conversationId,
        clientId=clientId,
        conversationSignature=conversationSignature,
        invocationId=invocationId)
    conversation_id = response["item"]["conversationId"]
    conversation_message = response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
    logging.info(f"ConversationId: {conversation_id}\nInvocationId: {invocationId}\nPrompt: {prompt}\nMessage: {conversation_message}")
    return {"conversationId": conversation_id, "message": conversation_message, "invocationId": invocationId+1}

app.run(debug=True, host="0.0.0.0")