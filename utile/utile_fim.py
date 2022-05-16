import os
from glob import iglob
from hashlib import md5, sha1
from stat import *
from time import time
import re

from utile import utile_data as data


def get_file_infos(filename):
    file_infos = {}
    stat_info = os.stat(filename)
    file_infos['file_inode'] = stat_info.st_ino
    file_infos['parent_id'] = os.stat(os.path.abspath(os.path.join(filename, os.pardir))).st_ino
    file_infos['file_name'] = filename
    file_infos['file_type'] = type_file(stat_info.st_mode)
    file_infos['file_mode'] = filemode(stat_info.st_mode)
    file_infos['file_nlink'] = stat_info.st_nlink
    file_infos['file_uid'] = stat_info.st_uid
    file_infos['file_gid'] = stat_info.st_gid
    file_infos['file_size'] = stat_info.st_size
    file_infos['file_atime'] = int(stat_info.st_atime)
    file_infos['file_mtime'] = int(stat_info.st_mtime)
    file_infos['file_ctime'] = int(stat_info.st_ctime)
    file_infos['file_md5'] = md5_file(filename)
    file_infos['file_SHA1'] = sha1_file(filename)
    return file_infos





def type_file(mode):
    """
    :param mode: 'D' --> Directory, R --> Regular file, B --> Block file, C --> Character file, L --> Link file
    :return:
    """
    if S_ISDIR(mode):
        return 'D'
    if S_ISREG(mode):
        return 'R'
    if S_ISBLK(mode):
        return 'B'
    if S_ISCHR(mode):
        return 'C'
    if S_ISLNK(mode):
        return 'L'


def md5_file(filename=''):
    if os.path.isfile(filename):
        hash_md5 = md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    return None


def sha1_file(filename=''):
    if os.path.isfile(filename):
        hash_sha1 = sha1()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()
    return None


def capture_image_de_reference(pattern):
    files_infos = {}
    for i in iglob(pattern, recursive=True):
        file_infos = get_file_infos(i)
        file_infos['datetime_image'] = int(time())
        files_infos[str(file_infos["file_inode"])] = file_infos
    return files_infos


def capture_image_stat_files(pattern):
    files_infos = {}
    for i in iglob(pattern, recursive=True):
        # print(f'Extracting file infos from {i}')
        file_infos = get_file_infos(i)
        files_infos[str(file_infos["file_inode"])] = file_infos
    return files_infos


def compare_image(stat_files, ref_images, rules):
    if rules[2]:
        print(f'Got compare : {rules} -> {stat_files} and {ref_images}')
    lister = []
    # boucle sur tuple ou l'inode stat files et ref image sont les memes
    try:
        for inode in stat_files.keys():
            if inode in ref_images.keys():
                erreur = ""
    # where start_inode={tuple_fichier_scanne[1]}")
                if rules[2] and re.match('/([^/]+)/?$', stat_files[inode]["file_name"]).group(1) != re.match('/([^/]+)/?$', ref_images[inode]["file_name"]).group(1):
                    erreur += f"{ref_images[inode]['file_name']} a changé de nom en {stat_files[inode]['file_name']} "
                # pour faire effet, il faut arrete de remplacer les anciennes images par des nouvelles dans le main
                if rules[1] and stat_files[inode]["parent_id"] != ref_images[inode]["parent_id"]:
                    erreur += f"Le fichier parent de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['parent_id']}"
                # # check du parent
                if rules[3] and stat_files[inode]['file_type'] != ref_images[inode]["file_type"]:
                    erreur += f"Le type de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_type']}"
                # # check type
                if rules[4] and stat_files[inode]['file_mode'] != ref_images[inode]["file_mode"]:
                    erreur += f"Le mode de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_mode']}"
                # # check mode
                if rules[5] and stat_files[inode]['file_nlink'] != ref_images[inode]["file_nlink"]:
                    erreur += f"Le nlink de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_nlink']}"
                # # check nlink
                if rules[6] and stat_files[inode]['file_uid'] != ref_images[inode]["file_uid"]:
                    erreur += f"Le uid de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_uid']}"
                # # check uid
                if rules[7] and stat_files[inode]['file_gid'] != ref_images[inode]["file_gid"]:
                    erreur += f"Le gid de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_gid']}"
                # # check gid
                if rules[8] and stat_files[inode]['file_size'] != ref_images[inode]["file_size"]:
                    erreur += f"La taille de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_size']}"
                # # check size
                if rules[9] and stat_files[inode]['file_atime'] != ref_images[inode]["file_atime"]:
                    erreur += f"Le atime de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_atime']}"
                # # check atime
                if rules[10] and stat_files[inode]['file_mtime'] != ref_images[inode]["file_mtime"]:
                    erreur += f"Le mtime de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_mtime']}"
                # # check mtime
                #
                # # check ctime !!!!! a ajouter à la bd !!!!!!!!!!!!!!!!!!!!!!!!!!!
                if rules[11] and stat_files[inode]['file_md5'] != ref_images[inode]["file_md5"]:
                    erreur += f"Le hash md5 de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_md5']}"
                # # check md5
                if rules[12] and stat_files[inode]['file_SHA1'] != ref_images[inode]["file_SHA1"]:
                    erreur += f"Le hash sha de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_SHA1']}"
                # # check sha
                if rules[13] and stat_files[inode]['file_ctime'] != ref_images[inode]["file_ctime"]:
                    erreur += f"Le ctime de {stat_files[inode]['file_name']} a changé en {stat_files[inode]['file_ctime']}"
                if len(erreur) > 0:
                    lister.append(erreur)

    except IndexError as e:
        pass
        """
        ça veut dire qu'il y a pas de règles ou qu'un truc est vide jcrois
        vu que c'est un index out of range il msemble
        """

    if len(lister) > 0:
        return lister

