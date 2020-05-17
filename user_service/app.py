from flask import Flask, jsonify

from model import get_db_connection, select, insert, get_users_table_handle

app = Flask(__name__)
CONNECTION = get_db_connection()

# basic route
@app.route("/")
def main():
    users_table = get_users_table_handle()
    res = CONNECTION.execute(select([users_table]))
    return jsonify({"user_list": [{"name": name, "handle": handle} for _id, name, handle in res.fetchall()]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
