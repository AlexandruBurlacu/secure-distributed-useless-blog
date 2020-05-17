from flask import Flask, render_template
import requests
import random

import time

app = Flask(__name__)


def make_catchphrase():
    return random.choice(["To be or not to be?", "Got milk?", "The dude abides"])


def make_full_user_stories(user_list):
    return [(idx, user_name, make_catchphrase()) for idx, user_name in enumerate(user_list)]


# basic route
@app.route("/")
def main():
    user_resp = requests.get("http://user_service_proxy")
    user_list = user_resp.json()

    blog_resp = requests.get("http://blog_service_proxy")
    blog_list = blog_resp.json()

    return render_template('index.html', users=make_full_user_stories(user_list['user_list']),
                                         blogs=[(idx, blog) for idx, blog in enumerate(blog_list["blog_list"])])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
