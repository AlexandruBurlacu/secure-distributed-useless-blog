from flask import Flask, jsonify, Response, request

from model import get_db_connection, get_blogs_table_handle

import json

import random

app = Flask(__name__)
CONNECTION = get_db_connection()


def to_slug(title):
    return f"{'-'.join(title.lower().split())}-{random.randint(2 ** 4, 2 ** 12)}"


def make_response(payload, status=200, headers=dict()):
    headers.update({"Content-Type": "application/json"})
    return Response(json.dumps(payload), status=status, headers=headers)


@app.route("/blogs")
def list_blogs():
    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(blogs_table.select())
    return make_response({"blog_list": [{"title": title, "author_handle": author_handle, "content": content, "slug": slug}
                        for title, slug, content, author_handle in res.fetchall()]})


@app.route("/blogs/<slug>")
def get_blog_by_handle(slug):
    if len(slug) > 256:
        return make_response({"msg": "invalid slug, must be < 255 characters long"}, status=400)

    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(blogs_table.select().where(blogs_table.c.slug == slug))
    return make_response({"blog_list": [{"title": title, "author_handle": author_handle, "content": content, "slug": slug}
                        for title, slug, content, author_handle in res.fetchall()]})


@app.route("/blogs/<slug>", methods=["PUT"])
def update_blog_by_handle(slug):
    if len(slug) > 256:
        return make_response({"msg": "invalid slug, must be < 255 characters long"}, status=400)

    data = request.get_json(force=True)
    title = data.get('title')
    content = data.get('content')

    if not (title or content):
        return make_response({"msg": "at least one of `title` or `content` must be updated"}, status=400)

    values = dict()
    if title:
        values.update(title=title)
    if content:
        values.update(content=content)

    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(blogs_table.update().where(blogs_table.c.slug == slug).values(**values))
    return make_response(data, status=201)


@app.route("/blogs/<slug>", methods=["DELETE"])
def delete_blog_by_handle(slug):
    if len(slug) > 256:
        return make_response({"msg": "invalid slug, must be < 255 characters long"}, status=400)

    blogs_table = get_blogs_table_handle()
    res = CONNECTION.execute(blogs_table.delete().where(blogs_table.c.slug == slug))
    return make_response({"status": "deleted"}, status=200)


@app.route("/blogs", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    title = data['title']
    content = data['content']
    author_handle = data['author_handle']

    if len(author_handle) > 32:
        return make_response({"msg": "invalid author_handle, must be < 32 characters long"}, status=400)
    
    if not author_handle.startswith("@"):
        return make_response({"msg": "invalid author_handle, must start with `@`"}, status=400)

    blogs_table = get_blogs_table_handle()

    slug = to_slug(title)

    CONNECTION.execute(blogs_table.insert().values([{
        "content": content,
        "title": title,
        "author_handle": author_handle,
        "slug": slug
    }]))
    return make_response({
        "content": content,
        "title": title,
        "author_handle": author_handle,
        "slug": slug
    }, status=201)


@app.route("/blogs/search", methods=["GET"])
def search_blog_by_title_or_author():
    title = request.args.get("title", None)
    author = request.args.get("author", None)

    blogs_table = get_blogs_table_handle()
    if title:
        res = CONNECTION.execute(blogs_table.select().where(blogs_table.c.title.ilike(f"%{title}%")))
    else:
        res = CONNECTION.execute(blogs_table.select().where(blogs_table.c.author_handle.ilike(f"%{author}%")))

    return make_response({"results": [{"title": title, "author_handle": author_handle, "content": content, "slug": slug}
                        for title, slug, content, author_handle in res.fetchall()]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
