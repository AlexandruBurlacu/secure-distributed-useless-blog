-- CREATE DATABASE blogs_prod;
CREATE DATABASE blogs_dev;

\connect blogs_dev

CREATE TABLE blogs (
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(128) NOT NULL,
    slug VARCHAR(256) NOT NULL,
    content TEXT NOT NULL,
    author_handle VARCHAR(32) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- CREATE TABLE blogs_prod.blogs (
--     id int,
--     title varchar(128),
--     handle varchar(32)
-- )

INSERT INTO blogs (title, slug, content, author_handle) VALUES
    ('Why Kripton fell', 'why-krypton-fell-7124', 'It fell because deatata. And the only survivior was The Superman.', '@realsuperman'),
    ('How I got metal skeleton', 'how-i-got-meta-skeleton-5312', 'It happened during an experiment. And that''s how I met your mother.', '@wolverine'),
    ('Disability is not the end', 'disability-is-not-the-end-5765', 'I lost my legs, but I still got brainzz', '@profxavier');
