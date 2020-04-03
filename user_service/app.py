from flask import Flask, jsonify

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
   app.run(port=5000, debug=True)
