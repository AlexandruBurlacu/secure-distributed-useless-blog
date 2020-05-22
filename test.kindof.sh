curl -vk https://localhost:5000/users
curl -vk https://localhost:5000/blogs

curl -vk -X POST -H 'Content-Type: application/json' \
            --data '{"handle": "@ab", "password": "1234", "name": "Alex Burlacu"}' \
            https://localhost:5000/users

curl -vk https://localhost:5000/users/@ab

curl -vk -X POST -H 'Content-Type: application/json' --data '{"username": "@ab", "password": "1234"}' https://localhost:5000/auth

TOKEN="Example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTAxNjY4MTAsIm5iZiI6MTU5MDE2NjgxMCwianRpIjoiOWM0Y2Q3ZjUtZWU4ZC00YWU3LTg3ZDEtZThkMzZkNWIxZTEwIiwiZXhwIjoxNTkwMTY3NzEwLCJpZGVudGl0eSI6IkBhYiIsImZyZXNoIjp0cnVlLCJ0eXBlIjoiYWNjZXNzIiwidXNlcl9jbGFpbXMiOnsicm9sZSI6InVzZXIifX0.P4Uak8eXPBPxW7SUUb_Vh4aN6bgXqHYmWMJXe-yuk_c"

curl -vk -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer $TOKEN' \
            --data '{"title": "How I was debuging this", "content": "via curl"}' https://localhost:5000/blogs

curl -vk https://localhost:5000/blogs/how-i-was-debuging-this-1370

curl -vk https://localhost:5000/blogs/search\?title\=How 

curl -vk https://localhost:5000/blogs/search\?author\=@wol

curl -vk https://localhost:5000/users/blogs\?user_name\=Log

curl -vk -X PUT -H 'Content-Type: application/json' -H 'Authorization: Bearer $TOKEN' \
        --data '{"content": "via curl and zsh", "author_handle": "@ab"}' https://localhost:5000/blogs/how-i-was-debuging-this-1370

curl -vk -X PUT -H 'Content-Type: application/json' -H 'Authorization: Bearer $TOKEN' \
        --data '{"content": "via curl and zsh and from a laptop", "title": "How I solved it", "author_handle": "@ab"}' \
        https://localhost:5000/blogs/how-i-was-debuging-this-1370

curl -vk -X DELETE -H 'Authorization: Bearer $TOKEN' https://localhost:5000/blogs/how-i-was-debuging-this-1370
curl -vk -X DELETE -H 'Authorization: Bearer $TOKEN' https://localhost:5000/users/@ab
