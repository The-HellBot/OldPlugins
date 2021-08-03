from sqlalchemy import Column, String
from . import SESSION, BASE


class harem(BASE):
    __tablename__ = "channels"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


harem.__table__.create(checkfirst=True)


def in_grp(chat_id):
    try:
        return SESSION.query(harem).filter(harem.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_grp(chat_id):
    adder = harem(str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def rm_grp(chat_id):
    rem = SESSION.query(harem).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_grp():
    rem = SESSION.query(harem).all()
    SESSION.close()
    return rem
