import os
from glob import iglob
from hashlib import md5, sha1
from stat import *
from time import time

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
    print(f'Got compare : {rules} -> {stat_files} and {ref_images}')
    pass
    # lister = []
    # db_conn = data.connect_db()
    # donnes_ref_image = data.select_db(db_conn, 'select max(datetime_image), * from ref_images group by file_inode', ())
    # # boucle sur tuple ou l'inode stat files et ref image sont les memes
    # for tuple_fichier_scanne in donnes_ref_image:
    #     donne_inode_scanne = data.select_db(db_conn, f'select * from stat_files where file_inode = ? ',
    #                                         (tuple_fichier_scanne[1],))
    #     donne_inode_image = data.select_db(db_conn, f'select * from ref_images where file_inode = ? ',
    #                                        (tuple_fichier_scanne[1],))
    #     # exemple d'un check uniquement sur name :
    #     regles_a_check = data.select_db(db_conn,
    #                                     f"Select * from fim_rules ", ())
    #     erreur = ""
    #     # where start_inode={tuple_fichier_scanne[1]}")
    #     try:
    #         if regles_a_check[0][6] == 1 and donne_inode_scanne[0][2] != donne_inode_image[0][4]:
    #             erreur += f"{donne_inode_image[0][4]} a changé de nom en {donne_inode_scanne[0][2]} "
    #         # pour faire effet, il faut arrete de remplacer les anciennes images par des nouvelles dans le main
    #         if regles_a_check[0][5] == 1 and donne_inode_scanne[0][1] != donne_inode_image[0][3]:
    #             erreur += f"Le fichier parent de {donne_inode_image[0][4]} a changé "
    #         # check du parent
    #         if regles_a_check[0][7] == 1 and donne_inode_scanne[0][3] != donne_inode_image[0][5]:
    #             erreur += f"Le type de {donne_inode_image[0][4]} a changé "
    #         # check type
    #         if regles_a_check[0][8] == 1 and donne_inode_scanne[0][4] != donne_inode_image[0][6]:
    #             erreur += f"Le mode de {donne_inode_image[0][4]} a changé "
    #         # check mode
    #         if regles_a_check[0][9] == 1 and donne_inode_scanne[0][5] != donne_inode_image[0][7]:
    #             erreur += f"Le nlink de {donne_inode_image[0][4]} a changé "
    #         # check nlink
    #         if regles_a_check[0][10] == 1 and donne_inode_scanne[0][6] != donne_inode_image[0][8]:
    #             erreur += f"Le uid de {donne_inode_image[0][4]} a changé "
    #         # check uid
    #         if regles_a_check[0][11] == 1 and donne_inode_scanne[0][7] != donne_inode_image[0][9]:
    #             erreur += f"Le gid de {donne_inode_image[0][4]} a changé "
    #         # check gid
    #         if regles_a_check[0][12] == 1 and donne_inode_scanne[0][8] != donne_inode_image[0][10]:
    #             erreur += f"La taille de {donne_inode_image[0][4]} a changé "
    #         # check size
    #         if regles_a_check[0][13] == 1 and donne_inode_scanne[0][9] != donne_inode_image[0][11]:
    #             erreur += f"Le atime de {donne_inode_image[0][4]} a changé "
    #         # check atime
    #         if regles_a_check[0][14] == 1 and donne_inode_scanne[0][10] != donne_inode_image[0][12]:
    #             erreur += f"Le mtime de {donne_inode_image[0][4]} a changé "
    #         # check mtime
    #
    #         # check ctime !!!!! a ajouter à la bd !!!!!!!!!!!!!!!!!!!!!!!!!!!
    #         if regles_a_check[0][15] == 1 and donne_inode_scanne[0][12] != donne_inode_image[0][14]:
    #             erreur += f"Le hash md5 de {donne_inode_image[0][4]} a changé "
    #         # check md5
    #         if regles_a_check[0][16] == 1 and donne_inode_scanne[0][13] != donne_inode_image[0][15]:
    #             erreur += f"Le hash sha de {donne_inode_image[0][4]} a changé "
    #         # check sha
    #         if regles_a_check[0][17] == 1 and donne_inode_scanne[0][11] != donne_inode_image[0][13]:
    #             erreur += f"Le ctime de {donne_inode_image[0][4]} a changé "
    #         if len(erreur) > 0:
    #             lister.append(erreur)
    #
    #     except IndexError as e:
    #         pass
    #         """
    #         ça veut dire qu'il y a pas de règles ou qu'un truc est vide jcrois
    #         vu que c'est un index out of range il msemble
    #         """
    #
    # if len(lister) > 0:
    #     return lister

