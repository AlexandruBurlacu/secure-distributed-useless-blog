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
GET /users
GET /users/:handle
GET /users/:handle/_login (internal/private)
GET /users/blogs?user_name=partial_name
POST /users
PUT /users/:handle
DELETE /users/:handle

GET /blogs
GET /blogs/:slug
GET /blogs?title=partial_title
POST /blogs
PUT /blogs/:slug
DELETE /blogs/:slug

POST /auth
```

## TODO
- 2 more routes `GET /users/blogs?user_name=partial_name` and `GET /blogs?title=partial_title`
- Make Vault PKI and integrate with Nginx


## What was done
- Microservices + API Gateway (kinda)
- JWT Auth
- RBAC
- NGINX load balancing and proxy-ing
- Network (micro-)segmentation
- HTTPS for outbound connections, self-signed, for now
- Postgres DBs with SQLAlchemy
- Validate inputs
- Publish api as Swagger (not, just in this markdown) docs
- Minor chores (Mem/CPU/PID limits, droped docker capabilities, strict DB access control)


### Current issues
- It is possible to create a blog by an unexistent user


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


## Docker Security Checks audit (relevant parts)

```

# ------------------------------------------------------------------------------
# Docker Bench for Security v1.3.4
#
# Docker, Inc. (c) 2015-
#
# Checks for dozens of common best-practices around deploying Docker containers in production.
# Inspired by the CIS Docker Community Edition Benchmark v1.1.0.
# ------------------------------------------------------------------------------

Initializing Tue May 19 21:28:51 UTC 2020

[INFO] 4 - Container Images and Build File
[WARN] 4.1  - Ensure a user for the container has been created
[WARN]      * Running as root: useless-blog_blog_service_proxy_1
[WARN]      * Running as root: useless-blog_user_service_proxy_1
[WARN]      * Running as root: secrets

[WARN] 4.6  - Ensure HEALTHCHECK instructions have been added to the container image
[WARN]      * No Healthcheck found: [useless-blog_blog_service:latest]
[WARN]      * No Healthcheck found: [useless-blog_user_service:latest]
[WARN]      * No Healthcheck found: [useless-blog_edge_service:latest]
[WARN]      * No Healthcheck found: [useless-blog_user_service_db:latest]
[WARN]      * No Healthcheck found: [useless-blog_blog_service_db:latest]

[INFO] 4.7  - Ensure update instructions are not use alone in the Dockerfile
[INFO]      * Update instruction found: [useless-blog_blog_service:latest]
[INFO]      * Update instruction found: [useless-blog_user_service:latest]
[INFO]      * Update instruction found: [useless-blog_edge_service:latest]

[INFO] 5 - Container Runtime
[PASS] 5.1  - Ensure AppArmor Profile is Enabled
[WARN] 5.2  - Ensure SELinux security options are set, if applicable
[WARN]      * No SecurityOptions Found: useless-blog_edge_service_1
[WARN]      * No SecurityOptions Found: useless-blog_blog_service_proxy_1
[WARN]      * No SecurityOptions Found: useless-blog_user_service_proxy_1
[WARN]      * No SecurityOptions Found: useless-blog_blog_service_1
[WARN]      * No SecurityOptions Found: useless-blog_user_service_1
[WARN]      * No SecurityOptions Found: secrets
[WARN]      * No SecurityOptions Found: useless-blog_blog_service_db_1
[WARN]      * No SecurityOptions Found: useless-blog_user_service_db_1
[WARN] 5.3  - Ensure Linux Kernel Capabilities are restricted within containers
[WARN]      * Capabilities added: CapAdd=[IPC_LOCK] to secrets
[PASS] 5.4  - Ensure privileged containers are not used
[PASS] 5.5  - Ensure sensitive host system directories are not mounted on containers
[PASS] 5.6  - Ensure ssh is not run within containers
[PASS] 5.7  - Ensure privileged ports are not mapped within containers

[PASS] 5.9  - Ensure the host's network namespace is not shared
[PASS] 5.10  - Ensure memory usage for container is limited
[PASS] 5.11  - Ensure CPU priority is set appropriately on the container
[WARN] 5.12  - Ensure the container's root filesystem is mounted as read only
[WARN]      * Container running with root FS mounted R/W: useless-blog_edge_service_1
[WARN]      * Container running with root FS mounted R/W: useless-blog_blog_service_proxy_1
[WARN]      * Container running with root FS mounted R/W: useless-blog_user_service_proxy_1
[WARN]      * Container running with root FS mounted R/W: useless-blog_blog_service_1
[WARN]      * Container running with root FS mounted R/W: useless-blog_user_service_1
[WARN]      * Container running with root FS mounted R/W: secrets
[WARN]      * Container running with root FS mounted R/W: useless-blog_blog_service_db_1
[WARN]      * Container running with root FS mounted R/W: useless-blog_user_service_db_1
[WARN] 5.13  - Ensure incoming container traffic is binded to a specific host interface
[WARN]      * Port being bound to wildcard IP: 0.0.0.0 in useless-blog_edge_service_1
[WARN]      * Port being bound to wildcard IP: 0.0.0.0 in secrets
[WARN] 5.14  - Ensure 'on-failure' container restart policy is set to '5'
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_edge_service_1
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_blog_service_proxy_1
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_user_service_proxy_1
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_blog_service_1
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_user_service_1
[WARN]      * MaximumRetryCount is not set to 5: secrets
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_blog_service_db_1
[WARN]      * MaximumRetryCount is not set to 5: useless-blog_user_service_db_1
[PASS] 5.15  - Ensure the host's process namespace is not shared
[PASS] 5.16  - Ensure the host's IPC namespace is not shared
[PASS] 5.17  - Ensure host devices are not directly exposed to containers
[INFO] 5.18  - Ensure the default ulimit is overwritten at runtime, only if needed
[INFO]      * Container no default ulimit override: useless-blog_edge_service_1
[INFO]      * Container no default ulimit override: useless-blog_blog_service_proxy_1
[INFO]      * Container no default ulimit override: useless-blog_user_service_proxy_1
[INFO]      * Container no default ulimit override: useless-blog_blog_service_1
[INFO]      * Container no default ulimit override: useless-blog_user_service_1
[INFO]      * Container no default ulimit override: secrets
[INFO]      * Container no default ulimit override: useless-blog_blog_service_db_1
[INFO]      * Container no default ulimit override: useless-blog_user_service_db_1
[PASS] 5.19  - Ensure mount propagation mode is not set to shared
[PASS] 5.20  - Ensure the host's UTS namespace is not shared
[PASS] 5.21  - Ensure the default seccomp profile is not Disabled
[NOTE] 5.22  - Ensure docker exec commands are not used with privileged option
[NOTE] 5.23  - Ensure docker exec commands are not used with user option
[PASS] 5.24  - Ensure cgroup usage is confirmed
[WARN] 5.25  - Ensure the container is restricted from acquiring additional privileges
[WARN]      * Privileges not restricted: useless-blog_edge_service_1
[WARN]      * Privileges not restricted: useless-blog_blog_service_proxy_1
[WARN]      * Privileges not restricted: useless-blog_user_service_proxy_1
[WARN]      * Privileges not restricted: useless-blog_blog_service_1
[WARN]      * Privileges not restricted: useless-blog_user_service_1
[WARN]      * Privileges not restricted: secrets
[WARN]      * Privileges not restricted: useless-blog_blog_service_db_1
[WARN]      * Privileges not restricted: useless-blog_user_service_db_1
[WARN] 5.26  - Ensure container health is checked at runtime
[WARN]      * Health check not set: useless-blog_edge_service_1
[WARN]      * Health check not set: useless-blog_blog_service_proxy_1
[WARN]      * Health check not set: useless-blog_user_service_proxy_1
[WARN]      * Health check not set: useless-blog_blog_service_1
[WARN]      * Health check not set: useless-blog_user_service_1
[WARN]      * Health check not set: secrets
[WARN]      * Health check not set: useless-blog_blog_service_db_1
[WARN]      * Health check not set: useless-blog_user_service_db_1
[INFO] 5.27  - Ensure docker commands always get the latest version of the image
[PASS] 5.28  - Ensure PIDs cgroup limit is used
[PASS] 5.29  - Ensure Docker's default bridge docker0 is not used
[PASS] 5.30  - Ensure the host's user namespaces is not shared
[PASS] 5.31  - Ensure the Docker socket is not mounted inside any containers

```
