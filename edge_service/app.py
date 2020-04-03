from flask import Flask, render_template
import requests
import random

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
   app.run(host="0.0.0.0", port=5000, debug=True)
