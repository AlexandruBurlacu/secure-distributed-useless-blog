-- CREATE DATABASE users_prod;
CREATE DATABASE users_dev;

\connect users_dev

CREATE TYPE ROLE_T AS ENUM ('admin', 'user', 'notloged');

CREATE TABLE users (
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(128) NOT NULL,
    handle VARCHAR(32) NOT NULL UNIQUE,
    user_role ROLE_T NOT NULL DEFAULT 'user',
    PRIMARY KEY (id)
);

GRANT SELECT, UPDATE(name), INSERT(name, handle, user_role), DELETE ON users TO postgres;

-- CREATE TABLE users_prod.users (
--     id int,
--     name varchar(128),
--     handle varchar(32)
-- )

INSERT INTO users (name, handle) VALUES ('Kal-El', '@realsuperman'), ('Logan', '@wolverine'), ('Professor Xavier', '@profxavier');
