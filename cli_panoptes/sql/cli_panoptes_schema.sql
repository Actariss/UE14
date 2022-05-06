-- create table fim_rules
CREATE TABLE fim_rules
(
    fim_rule_id INTEGER PRIMARY KEY,
    fim_rule_name VARCHAR(255),
    path        VARCHAR(255),
    start_inode INTEGER,
    inode       BOOLEAN,
    parent      BOOLEAN,
    name        BOOLEAN,
    type        BOOLEAN,
    mode        BOOLEAN,
    nlink       BOOLEAN,
    uid         BOOLEAN,
    gid         BOOLEAN,
    size        BOOLEAN,
    atime       BOOLEAN,
    mtime       BOOLEAN,
    md5         BOOLEAN,
    sha1        BOOLEAN,
    ctime       BOOLEAN
);

-- create table stat_files
CREATE TABLE stat_files
(
    file_inode INTEGER PRIMARY KEY,
    parent_id  INTEGER,
    file_name  VARCHAR,
    file_type  TEXT,
    file_mode  VARCHAR,
    file_nlink  INTEGER,
    file_uid   INTEGER,
    file_gid   INTEGER,
    file_size  INTEGER,
    file_atime TIMESTAMP,
    file_mtime TIMESTAMP,
    file_ctime TIMESTAMP,
    file_md5   VARCHAR,
    file_SHA1  VARCHAR
);

-- create table ref_images
CREATE TABLE ref_images
(
    image_id       INTEGER PRIMARY KEY,
    file_inode     INTEGER,
    datetime_image TIMESTAMP,
    parent_id      INTEGER,
    file_name      VARCHAR,
    file_type      TEXT,
    file_mode      VARCHAR,
    file_nlink     INTEGER,
    file_uid       INTEGER,
    file_gid       INTEGER,
    file_size      INTEGER,
    file_atime     TIMESTAMP,
    file_mtime     TIMESTAMP,
    file_ctime     TIMESTAMP,
    file_md5       VARCHAR,
    file_SHA1      VARCHAR
);

-- create table fim_sets
CREATE TABLE fim_sets
(
    fim_set_id   INTEGER PRIMARY KEY,
    fim_rule_id  INTEGER,
    fim_set_name VARCHAR,
    schedule     INTEGER,
    FOREIGN KEY (fim_rule_id) REFERENCES fim_rules (fim_rule_id)
);

-- create table fim_events
CREATE TABLE fim_events
(
    fim_event_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    fim_set_id     INTEGER,
    fim_rule_id    INTEGER,
    image_id       INTEGER,
    file_inode     INTEGER,
    datetime_event TIMESTAMP,
    except_msg     VARCHAR,
    except_active  BOOLEAN,
    FOREIGN KEY (fim_set_id) REFERENCES fim_sets (fim_set_id),
    FOREIGN KEY (fim_rule_id) REFERENCES fim_rules (fim_rule_id),
    FOREIGN KEY (image_id) REFERENCES ref_images (image_id),
    FOREIGN KEY (file_inode) REFERENCES stat_files (file_inode)
);

-- create table sa_jobs
CREATE TABLE sa_jobs
(
    sa_job_id       INTEGER PRIMARY KEY,
    sa_job_name     VARCHAR,
    script          BOOLEAN,
    command_script  VARCHAR,
    expected_result VARCHAR,
    alert_message   VARCHAR
);

-- create table sa_sets
CREATE TABLE sa_sets
(
    sa_set_id   INTEGER PRIMARY KEY,
    sa_job_id   INTEGER,
    sa_set_name VARCHAR,
    schedule    INTEGER,
    FOREIGN KEY (sa_job_id) REFERENCES sa_jobs (sa_job_id)
);

--create table sa_events
CREATE TABLE sa_events
(
    sa_event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    sa_set_id      INTEGER,
    sa_job_id      INTEGER,
    datetime_event TIMESTAMP,
    except_active  BOOLEAN,
    FOREIGN KEY (sa_set_id) REFERENCES sa_sets (sa_set_id),
    FOREIGN KEY (sa_job_id) REFERENCES sa_jobs (sa_job_id)
);

INSERT INTO fim_rules (fim_rule_id, fim_rule_name, path, start_inode, inode, parent, name, type, mode, nlink, uid, gid, size, atime, mtime, md5, sha1, ctime) VALUES (1, 'regle oui', '/home/q210079/Desktop/**', 576191, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1);


INSERT INTO sa_sets (sa_set_id, sa_job_id, sa_set_name, schedule) VALUES (1, 1, 'every 5 seconds', 5);
INSERT INTO sa_sets (sa_set_id, sa_job_id, sa_set_name, schedule) VALUES (2, 2, 'every 7 seconds', 7);

INSERT INTO fim_sets (fim_set_id, fim_rule_id, fim_set_name, schedule) VALUES (1, 1, 'Coucou', 10);

INSERT INTO sa_jobs (sa_job_id, sa_job_name, script, command_script, expected_result, alert_message) VALUES (1, 'Syslog-ng', 1, 'systemctl is-active syslog-ng
', 'active', 'Syslog-ng est désacitvé');
INSERT INTO sa_jobs (sa_job_id, sa_job_name, script, command_script, expected_result, alert_message) VALUES (2, 'Ssh.service', 1, 'systemctl is-active ssh.service
', 'active', 'Ssh.service est désctivé');







