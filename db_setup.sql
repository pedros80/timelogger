/*
 Run as root, creates user and grants privileges as stored in config.php
 Why can't use function NOW() (or indeed any function!) as DEFAULT
 value for start? sure it is in the standards...
*/

CREATE DATABASE logger;

CREATE USER 'logger_u'@'localhost' IDENTIFIED BY 'this is a dummy pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON 'logger' TO 'logger_u'@'localhost';

CREATE TABLE tasks (
            tid INT NOT NULL AUTO_INCREMENT,
            descript VARCHAR(200),
            PRIMARY KEY (tid)
);


CREATE TABLE logs (
        tid INT NOT NULL,
        start DATETIME,
        stop DATETIME,
        PRIMARY KEY (tid, start)
);

