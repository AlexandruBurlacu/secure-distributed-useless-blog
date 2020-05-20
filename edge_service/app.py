from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from security import authenticate
import requests
import random

import time
import os

app = Flask(__name__)
app.secret_key = os.environ["JWT_SECRET"]
app.config['JWT_SECRET_KEY'] = os.environ["JWT_SECRET"]
jwt = JWTManager(app)


def make_catchphrase():
    return random.choice(["To be or not to be?", "Got milk?", "The dude abides"])


def make_full_user_stories(user_list):
    return [(idx, user_name, make_catchphrase()) for idx, user_name in enumerate(user_list)]


@app.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


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
@jwt_required
def create_users():
    current_user = get_jwt_identity()
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    user_resp = requests.post("http://user_service_proxy/users", data=data, headers=headers)
    return user_resp.json(), user_resp.status_code


@app.route("/blogs", methods=["POST"])
@jwt_required
def create_blogs():
    current_user = get_jwt_identity()
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
@jwt_required
def update_user_by_handle(handle):
    current_user = get_jwt_identity()
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    user_resp = requests.put(f"http://user_service_proxy/users/{handle}", data=data, headers=headers)
    return user_resp.json(), user_resp.status_code


@app.route("/blogs/<slug>", methods=["PUT"])
@jwt_required
def update_blog_by_slug(slug):
    current_user = get_jwt_identity()
    data = request.data
    headers = {"Content-Type": request.headers.get("Content-Type")}
    blog_resp = requests.put(f"http://blog_service_proxy/blogs/{slug}", data=data, headers=headers)
    return blog_resp.json(), blog_resp.status_code


@app.route("/users/<handle>", methods=["DELETE"])
@jwt_required
def delete_user_by_handle(handle):
    current_user = get_jwt_identity()
    user_resp = requests.delete(f"http://user_service_proxy/users/{handle}")
    return user_resp.json(), user_resp.status_code


@app.route("/blogs/<slug>", methods=["DELETE"])
@jwt_required
def delete_blog_by_slug(slug):
    current_user = get_jwt_identity()
    blog_resp = requests.delete(f"http://blog_service_proxy/blogs/{slug}")
    return blog_resp.json(), blog_resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
