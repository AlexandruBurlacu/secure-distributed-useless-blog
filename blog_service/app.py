from flask import Flask, jsonify

app = Flask(__name__)

# basic route
@app.route("/")
def main():
    return jsonify({"blog_list": [
       {"title": "blog1", "author": "user1"},
       {"title": "blog2", "author": "user1"},
       {"title": "blog3", "author": "user2"}
    ]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
