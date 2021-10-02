from . import BASE, SESSION

from sqlalchemy import BigInteger, Column, Numeric, String, UnicodeText


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    client = Column(String(14), primary_key=True)
    previous_welcome = Column(BigInteger)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, previous_welcome, reply, f_mesg_id, client):
        self.chat_id = str(chat_id)
        self.previous_welcome = previous_welcome
        self.reply = reply
        self.f_mesg_id = f_mesg_id
        self.client = str(client)


Welcome.__table__.create(checkfirst=True)


def get_welcome(chat_id, client):
    try:
        return SESSION.query(Welcome).get(str(chat_id), str(client))
    finally:
        SESSION.close()


def get_current_welcome(chat_id, client):
    try:
        return SESSION.query(Welcome).filter(Welcome.chat_id == str(chat_id), str(client)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_welcome(chat_id, previous_welcome, reply, f_mesg_id, client):
    to_check = get_welcome(chat_id, client)
    if not to_check:
        adder = Welcome(chat_id, previous_welcome, reply, f_mesg_id, client)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Welcome).get(str(chat_id), str(client))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Welcome(chat_id, previous_welcome, reply, f_mesg_id, client)
    SESSION.commit()
    return False


def rm_welcome(chat_id, client):
    try:
        rem = SESSION.query(Welcome).get(str(chat_id), str(client))
        if rem:
            SESSION.delete(rem)
            SESSION.commit()
            return True
    except BaseException:
        return False


def update_welcome(chat_id, previous_welcome, client):
    row = SESSION.query(Welcome).get(str(chat_id), str(client))
    row.previous_welcome = previous_welcome
    SESSION.commit()
