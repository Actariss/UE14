-- # TRIGGERS
CREATE TRIGGER update_on_insert
    BEFORE INSERT ON stat_files
    WHEN(EXISTS(SELECT * FROM stat_files WHERE file_inode == new.file_inode))
BEGIN
    UPDATE stat_files
    SET parent_id = new.parent_id,
        file_name = new.file_name,
        file_type = new.file_type,
        file_mode = new.file_mode,
        file_nlink = new.file_nlink,
        file_uid = new.file_uid,
        file_gid = new.file_gid,
        file_size = new.file_size,
        file_atime = new.file_atime,
        file_mtime = new.file_mtime,
        file_ctime = new.file_ctime,
        file_md5 = new.file_md5,
        file_SHA1 = new.file_SHA1
    WHERE file_inode == new.file_inode;
    SELECT RAISE ( IGNORE ) WHERE EXISTS(SELECT * FROM stat_files WHERE file_inode == new.file_inode);
END;