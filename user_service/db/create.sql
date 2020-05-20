-- CREATE DATABASE users_prod;
CREATE DATABASE users_dev;

\connect users_dev

CREATE TYPE ROLE_T AS ENUM ('admin', 'user', 'notloged');

CREATE TABLE users (
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(128) NOT NULL,
    handle VARCHAR(32) NOT NULL UNIQUE,
    user_role ROLE_T NOT NULL DEFAULT 'user',
    password CHAR(60) NOT NULL,
    PRIMARY KEY (id)
);

GRANT SELECT, UPDATE(name), INSERT(name, handle, user_role, password), DELETE ON users TO postgres;

-- CREATE TABLE users_prod.users (
--     id int,
--     name varchar(128),
--     handle varchar(32)
-- )

INSERT INTO users (name, handle, password) VALUES
    ('Kal-El', '@realsuperman', '$2b$12$0UrimppLS9kNfSS5X.Mp0eLxdSvuHNq9cMqeW0LCe7XbQ45Hn3BSe'),
    ('Logan', '@wolverine', '$2b$12$0UrimppLS9kNfSS5X.Mp0eLxdSvuHNq9cMqeW0LCe7XbQ45Hn3BSe'),
    ('Professor Xavier', '@profxavier', '$2b$12$0UrimppLS9kNfSS5X.Mp0eLxdSvuHNq9cMqeW0LCe7XbQ45Hn3BSe');

INSERT INTO users (name, handle, user_role, password) VALUES
    ('The Almighty', '@admin', 'admin', '$2b$12$KeKLW5ri.iLu7LWTrcOABuZDBPJ9lR/jGOMOM75mdX6If2MPehbZ2');
