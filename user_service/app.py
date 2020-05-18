from flask import Flask, jsonify

from model import get_db_connection, select, insert, get_users_table_handle

app = Flask(__name__)
CONNECTION = get_db_connection()

@app.route("/users")
def list_users():
    users_table = get_users_table_handle()
    res = CONNECTION.execute(select([users_table]))
    return jsonify({"user_list": [{"name": name, "handle": handle} for _id, name, handle in res.fetchall()]})


@app.route("/users/<handle>")
def get_user_by_handle(handle):
    if len(handle) > 32:
        return {"error": "invalid handle, must be < 32 characters long"}, 400
    
    if not handle.startswith("@"):
        return {"error": "invalid handle, must start with `@`"}, 400

    users_table = get_users_table_handle()
    res = CONNECTION.execute(select([users_table]).where(users_table.c.handle == handle))
    return jsonify({"user_list": [{"name": name, "handle": handle} for _id, name, handle in res.fetchall()]})


@app.route("/users", methods=["POST"])
def create_user(): # TODO: rewrite
    users_table = get_users_table_handle()
    res = CONNECTION.execute(select([users_table]))
    return jsonify({"user_list": [{"name": name, "handle": handle} for _id, name, handle in res.fetchall()]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
