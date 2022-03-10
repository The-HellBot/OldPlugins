from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from . import BASE, SESSION


class Husbando(BASE):
    __tablename__ = "husbando"
    chat_id = Column(String(14), primary_key=True)
    
    def __init__(self, chat_id):
        self.chat_id = chat_id


Husbando.__table__.create(checkfirst=True)


def add_hus_grp(chat_id: str):
    husba = Husbando(str(chat_id))
    SESSION.add(husba)
    SESSION.commit()


def rm_hus_grp(chat_id: str):
    husba = SESSION.query(Husbando).get(str(chat_id))
    if husba:
        SESSION.delete(husba)
        SESSION.commit()


def get_all_hus_grp():
    husba = SESSION.query(Husbando).all()
    SESSION.close()
    return husba


def is_husb(chat_id: str):
    try:
        husba = SESSION.query(Husbando).get(str(chat_id))
        if husba:
            return str(husba.chat_id)
    finally:
        SESSION.close()
