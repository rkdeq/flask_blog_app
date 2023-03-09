-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;

-- Create table user (
--     id uuid primary key default generate_uuid(),
--     username text unique not null,
--     password text unique not null
-- );

-- Create table post (
--     id uuid primary key default generate_uuid(),
--     author_id uuid not null,
--     title text not null,
--     body text,
--     created_at timestamp not null default current_timestamp,
--     Foreign key (author_id) references user (id)
-- );

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);