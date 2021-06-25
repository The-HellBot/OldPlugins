from . import SESSION, BASE
from sqlalchemy import Column, String


class Fsub(BASE):
    __tablename__ = "fsub"
    chat_id = Column(String(14), primary_key=True)
    target = Column(String(127))

    def __init__(self, chat_id, target=""):
        self.chat_id = chat_id
        self.target = target


Fsub.__table__.create(checkfirst=True)


def is_fsub(chat_id):
    try:
        return SESSION.query(Fsub).filter(Fsub.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_fsub(chat_id, target):
    adder = Fsub(str(chat_id), str(target))
    SESSION.add(adder)
    SESSION.commit()


def rem_fsub(chat_id):
    rem = SESSION.query(Fsub).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def all_fsub():
    rem = SESSION.query(Fsub).all()
    SESSION.close()
    return rem
