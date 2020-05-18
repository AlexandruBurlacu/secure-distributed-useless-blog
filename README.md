# `I Ain't Gonna Need It` blog, a masters project

Below you can find the links that I used to learn how to do a distributed + secure application, and some idea-pads. Enjoy.

## DB Schema (not really)

There are `users` and there are `blogs`. Every user can have multiple blog posts. A blog has just one author/user. 1:n relation.

Use Case: Find all blogs that are written by someone Franklin:
```sql
SELECT * FROM blogs WHERE blogs.author_handle = (SELECT handle FROM users WHERE name MATCHES "% Franklin %");
-- kinda, what a shame my database is divided between microservices
```

## The API
```
GET /users (done)
GET /users/:handle (done)
GET /users/blogs?user_name=partial_name
POST /users
PUT /users/:handle
DELETE /users/:handle

GET /blogs (done)
GET /blogs/:slug (done)
GET /blogs?title=partial_title
POST /blogs
PUT /blogs/:slug
DELETE /blogs/:slug

POST /auth (via JWT)
```

## TODO
- Publish api as Swagger docs
- Validate inputs
- Implement controllers + rbac
- Make Vault PKI and integrate with Nginx

## What was done
- Microservices + API Gateway (kinda)
- NGINX load balancing and proxy-ing
- Network (micro-)segmentation
- HTTPS for outbound connections, self-signed, for now
- Postgres DBs with SQLAlchemy

## Used links

[Deprecated] RabbitMQ
- https://dev.to/usamaashraf/microservices--rabbitmq-on-docker-e2f
- https://www.rabbitmq.com/getstarted.html
- https://github.com/dmaze/docker-rabbitmq-example
- https://www.rabbitmq.com/ssl.html

OpenSSL
- https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

Vault
- https://www.vaultproject.io/api-docs/secret/pki
- https://www.hashicorp.com/blog/certificate-management-with-vault/
- https://www.nginx.com/blog/protecting-ssl-private-keys-nginx-hashicorp-vault/
- https://medium.com/@sufiyanghori/guide-using-hashicorp-vault-to-manage-pki-and-issue-certificates-e1981e7574e
- http://cuddletech.com/?p=959

Flask
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
- https://www.bogotobogo.com/python/Flask/Python_Flask_Blog_App_Tutorial_1.php
- https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/
- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

SQLAlchemy
- https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
- https://riptutorial.com/sqlalchemy

RBAC
- https://flask-user.readthedocs.io/en/latest/authorization.html
- https://subscription.packtpub.com/book/web_development/9781788995405/6/ch06lvl1sec41/role-based-access-control-rbac
- https://github.com/tonyseek/simple-rbac
- https://github.com/casbin/pycasbin

JWT and Auth in general
- https://realpython.com/token-based-authentication-with-flask/
- https://blog.tecladocode.com/simple-jwt-authentication-with-flask-jwt/
- https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask
- https://geekflare.com/securing-flask-api-with-jwt/
- https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb

Others:
- https://developer.okta.com/blog/2020/03/23/microservice-security-patterns
- https://pythonhosted.org/Flask-Security/features.html
- https://github.com/OWASP/Docker-Security/blob/master/D03%20-%20Network%20Segmentation%20and%20Firewalling.md
- https://success.docker.com/article/networking

