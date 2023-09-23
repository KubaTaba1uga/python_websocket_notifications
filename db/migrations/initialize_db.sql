CREATE TABLE app_user (
 id SERIAL PRIMARY KEY,
 username TEXT NOT NULL
);

-- GRANT select, insert, update, delete on app_user to username ;

CREATE TABLE message (
     id SERIAL PRIMARY KEY,
     content TEXT NOT NULL,
     from_ INT NOT NULL,
     to_ INT NOT NULL,
     CONSTRAINT fk_from FOREIGN KEY(from_) REFERENCES app_user(id),
     CONSTRAINT fk_to FOREIGN KEY(to_) REFERENCES app_user(id)
);

INSERT INTO app_user (username) VALUES
       ('Jakub'), ('Maciek'), ('Magda'), ('Kuba'), ('Daniel');


INSERT INTO message (content, from_, to_) VALUES
       ('Czesc Kuba', 1, 2),
       ('Czesc Maciek', 2, 1),
       ('Lubie wszystko', 4, 3),
       ('Nie lubie nic', 3, 4),
       ('Kocham kotki', 5, 3),
       ('Kocham foki', 1, 5);

