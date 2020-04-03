from flask import Flask, render_template
import requests
import random

import ssl

import time

import pika

app = Flask(__name__)


def make_catchphrase():
    return random.choice(["To be or not to be?", "Got milk?", "The dude abides"])


def make_full_user_stories(user_list):
    return [(idx, user_name, make_catchphrase()) for idx, user_name in enumerate(user_list)]


# basic route
@app.route("/")
def main():
    resp = requests.get("http://user_service:5000")
    user_list = resp.json()
    return render_template('index.html', users=make_full_user_stories(user_list['user_list']))

if __name__ == "__main__":
    # time.sleep(5)
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='rabbitmq'))
    # channel = connection.channel()

    # channel.queue_declare(queue='hello')


    # def callback(ch, method, properties, body):
    #     print(" [x] Received %r" % body)


    # channel.basic_consume(
    #     queue='hello', on_message_callback=callback, auto_ack=True)

    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()

    app.run(host="0.0.0.0", port=5000, debug=True)
