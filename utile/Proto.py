import hashlib
import pickle
from enum import Enum


class Proto(Enum):
    SA_EVENT = 0,
    FIM_EVENT = 1,
    IMG = 2,
    STAT = 3,
    # NEW
    LD_FIM = 4,
    LD_SA = 5,
    LD_IMG = 6


def pickler(data: any):
    """Permet d'encapsuler les objets sous forme de pickel ,collection d'octets"""
    data_pickled = pickle.dumps(data)
    length = len(data_pickled).to_bytes(4, 'big')
    md5 = hashlib.md5(data_pickled).digest()

    header = length + md5 + data_pickled

    return header


def verify(data: any):
    """Permet de vérifier le contenu d'une trame en calculant les CRC et en comparant la taille"""
    header = data[0:20]
    length = header[0:4]
    crc = header[4:]

    new_data = data[20:]

    match_size = len(new_data).to_bytes(4, 'big') == length
    match_hash = hashlib.md5(new_data).digest() == crc

    return match_size and match_hash