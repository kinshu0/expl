DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS tracker;
DROP TABLE IF EXISTS email_log;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE tracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_name TEXT UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)

);

CREATE TABLE email_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    accessed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tracker_id INTEGER NOT NULL,
    FOREIGN KEY (tracker_id) REFERENCES tracker (id)
);


-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );