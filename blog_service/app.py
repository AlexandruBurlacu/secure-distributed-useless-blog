from flask import Flask, jsonify

from model import get_db_connection, select, insert, get_blogs_table_handle

app = Flask(__name__)
CONNECTION = get_db_connection()


@app.route("/blogs")
def list_blogs():
    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(select([blogs_table]))
    return jsonify({"blog_list": [{"title": title, "author_handle": author_handle, "content": content}
                        for _id, title, _slug, content, author_handle in res.fetchall()]})


@app.route("/blogs/<slug>")
def get_blog_by_handle(slug):
    if len(slug) > 256:
        return {"error": "invalid slug, must be < 255 characters long"}, 400

    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(select([blogs_table]).where(blogs_table.c.slug == slug))
    return jsonify({"blog_list": [{"title": title, "author_handle": author_handle, "content": content}
                        for _id, title, _slug, content, author_handle in res.fetchall()]})


@app.route("/blogs", methods=["POST"])
def create_blog(): # TODO: rewrite
    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(select([blogs_table]))
    return jsonify({"blog_list": [{"title": title, "author_handle": author_handle, "content": content}
                        for _id, title, _slug, content, author_handle in res.fetchall()]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
