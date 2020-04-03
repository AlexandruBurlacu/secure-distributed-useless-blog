from flask import Flask, jsonify

import time
import pika

app = Flask(__name__)

# basic route
@app.route("/")
def main():
    return jsonify({"user_list": [
       {"name": "user1"},
       {"name": "user2"},
       {"name": "user3"}
    ]})

if __name__ == "__main__":
    time.sleep(5)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()
    app.run(host="0.0.0.0", port=5000, debug=True)
