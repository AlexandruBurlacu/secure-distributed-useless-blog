from flask import Flask, jsonify

from model import get_db_connection, select, insert, get_blogs_table_handle

app = Flask(__name__)
CONNECTION = get_db_connection()

# basic route
@app.route("/")
def main():
    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(select([blogs_table]))
    return jsonify({"blog_list": [{"title": title, "author_handle": author_handle, "content": content}
                        for _id, title, _slug, content, author_handle in res.fetchall()]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
