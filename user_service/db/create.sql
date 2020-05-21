-- CREATE DATABASE users_prod;
CREATE DATABASE users_dev;

\connect users_dev

CREATE TYPE ROLE_T AS ENUM ('admin', 'user', 'notloged');

CREATE TABLE users (
    name VARCHAR(128) NOT NULL,
    handle VARCHAR(32) NOT NULL UNIQUE,
    user_role ROLE_T NOT NULL DEFAULT 'user',
    password CHAR(60) NOT NULL,
    PRIMARY KEY (handle)
);

GRANT SELECT, UPDATE(name), INSERT(name, handle, user_role, password), DELETE ON users TO postgres;

INSERT INTO users (name, handle, password) VALUES
    ('Kal-El', '@realsuperman', '$2b$12$0UrimppLS9kNfSS5X.Mp0eLxdSvuHNq9cMqeW0LCe7XbQ45Hn3BSe'),
    ('Logan', '@wolverine', '$2b$12$0UrimppLS9kNfSS5X.Mp0eLxdSvuHNq9cMqeW0LCe7XbQ45Hn3BSe'),
    ('Professor Xavier', '@profxavier', '$2b$12$0UrimppLS9kNfSS5X.Mp0eLxdSvuHNq9cMqeW0LCe7XbQ45Hn3BSe');

INSERT INTO users (name, handle, user_role, password) VALUES
    ('The Almighty', '@admin', 'admin', '$2b$12$KeKLW5ri.iLu7LWTrcOABuZDBPJ9lR/jGOMOM75mdX6If2MPehbZ2');
