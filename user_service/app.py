from flask import Flask, request, Response

import json

from model import get_db_connection, get_users_table_handle

app = Flask(__name__)
CONNECTION = get_db_connection()

def make_response(payload, status=200, headers=dict()):
    headers.update({"Content-Type": "application/json"})
    return Response(json.dumps(payload), status=status, headers=headers)


@app.route("/users")
def list_users():
    users_table = get_users_table_handle()
    res = CONNECTION.execute(users_table.select())
    return make_response({"user_list": [{"name": name, "handle": handle} for _id, name, handle, _role, _psswd in res.fetchall()]})


@app.route("/users/<handle>")
def get_user_by_handle(handle):
    if len(handle) > 32:
        return make_response({"msg": "invalid handle, must be < 32 characters long"}, status=400)
    
    if not handle.startswith("@"):
        return make_response({"msg": "invalid handle, must start with `@`"}, status=400)

    users_table = get_users_table_handle()
    res = CONNECTION.execute(users_table.select().where(users_table.c.handle == handle))
    return make_response({"user_list": [{"name": name, "handle": handle} for _id, name, handle, _role, _psswd in res.fetchall()]})


@app.route("/users/<handle>/_login")
def __login(handle):
    if len(handle) > 32:
        return make_response({"msg": "invalid handle, must be < 32 characters long"}, status=400)
    
    if not handle.startswith("@"):
        return make_response({"msg": "invalid handle, must start with `@`"}, status=400)

    users_table = get_users_table_handle()
    res = CONNECTION.execute(users_table.select().where(users_table.c.handle == handle))
    user_tuple = res.fetchone()
    _id, _name, handle, role, psswd = user_tuple
    return make_response({"password": psswd, "handle": handle, "role": role})


@app.route("/users/<handle>", methods=["PUT"])
def update_user_by_handle(handle):
    data = request.get_json(force=True)
    name = data['name']

    if len(handle) > 32:
        return make_response({"msg": "invalid handle, must be < 32 characters long"}, status=400)
    
    if not handle.startswith("@"):
        return make_response({"msg": "invalid handle, must start with `@`"}, status=400)

    users_table = get_users_table_handle()
    res = CONNECTION.execute(users_table.update().where(users_table.c.handle == handle).values(name=name))
    return make_response(data, status=201)


@app.route("/users/<handle>", methods=["DELETE"])
def delete_user_by_handle(handle):
    if len(handle) > 32:
        return make_response({"msg": "invalid handle, must be < 32 characters long"}, status=400)
    
    if not handle.startswith("@"):
        return make_response({"msg": "invalid handle, must start with `@`"}, status=400)


    users_table = get_users_table_handle()
    res = CONNECTION.execute(users_table.delete().where(users_table.c.handle == handle))
    return make_response({"status": "deleted"}, status=200)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    handle = data['handle']
    name = data['name']

    if len(handle) > 32:
        return make_response({"msg": "invalid handle, must be < 32 characters long"}, status=400)
    
    if not handle.startswith("@"):
        return make_response({"msg": "invalid handle, must start with `@`"}, status=400)

    users_table = get_users_table_handle()
    CONNECTION.execute(users_table.insert().values([{
        "name": name,
        "handle": handle
    }]))
    return make_response(data, status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
