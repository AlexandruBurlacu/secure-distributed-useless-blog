from flask import Flask, render_template, request
import requests
import random

import time

app = Flask(__name__)
# https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask

def make_catchphrase():
    return random.choice(["To be or not to be?", "Got milk?", "The dude abides"])


def make_full_user_stories(user_list):
    return [(idx, user_name, make_catchphrase()) for idx, user_name in enumerate(user_list)]


# basic route
@app.route("/")
def main():
    user_resp = requests.get("http://user_service_proxy/users")
    user_list = user_resp.json()

    blog_resp = requests.get("http://blog_service_proxy/blogs")
    blog_list = blog_resp.json()

    return render_template('index.html', users=make_full_user_stories(user_list['user_list']),
                                         blogs=[(idx, blog) for idx, blog in enumerate(blog_list["blog_list"])])


@app.route("/users")
def list_users():
    user_resp = requests.get("http://user_service_proxy/users")
    return user_resp.json(), user_resp.status_code


@app.route("/blogs")
def list_blogs():
    blog_resp = requests.get("http://blog_service_proxy/blogs")
    return blog_resp.json(), blog_resp.status_code


@app.route("/users", methods=["POST"])
def create_users():
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    user_resp = requests.post("http://user_service_proxy/users", data=data, headers=headers)
    return user_resp.json(), user_resp.status_code


@app.route("/blogs", methods=["POST"])
def create_blogs():
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    blog_resp = requests.post("http://blog_service_proxy/blogs", data=data, headers=headers)
    return blog_resp.json(), blog_resp.status_code


@app.route("/users/<handle>")
def get_user_by_handle(handle):
    user_resp = requests.get(f"http://user_service_proxy/users/{handle}")
    return user_resp.json(), user_resp.status_code


@app.route("/blogs/<slug>")
def get_blog_by_slug(slug):
    blog_resp = requests.get(f"http://blog_service_proxy/blogs/{slug}")
    return blog_resp.json(), blog_resp.status_code


@app.route("/users/<handle>", methods=["PUT"])
def update_user_by_handle(handle):
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    user_resp = requests.put(f"http://user_service_proxy/users/{handle}", data=data, headers=headers)
    return user_resp.json(), user_resp.status_code


@app.route("/blogs/<slug>", methods=["PUT"])
def update_blog_by_slug(slug):
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    blog_resp = requests.put(f"http://blog_service_proxy/blogs/{slug}", data=data, headers=headers)
    return blog_resp.json(), blog_resp.status_code


@app.route("/users/<handle>", methods=["DELETE"])
def delete_user_by_handle(handle):
    user_resp = requests.delete(f"http://user_service_proxy/users/{handle}")
    return user_resp.json(), user_resp.status_code


@app.route("/blogs/<slug>", methods=["DELETE"])
def delete_blog_by_slug(slug):
    blog_resp = requests.delete(f"http://blog_service_proxy/blogs/{slug}")
    return blog_resp.json(), blog_resp.status_code


@app.route("/test") # NICEEEEEE! ^_^
def test_selects():
    user_resp = requests.get("http://user_service_proxy/users/@profxavier")
    user_list = user_resp.json()

    blog_resp = requests.get("http://blog_service_proxy/blogs/disability-is-not-the-end-5765")
    blog_list = blog_resp.json()

    return {"user": user_list, "blog": blog_list}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
