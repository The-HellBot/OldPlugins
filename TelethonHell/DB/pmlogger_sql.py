from sqlalchemy import Column, String
from TelethonHell.DB import BASE, SESSION


class PmLogger(BASE):
    __tablename__ = "pmlogger"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


PmLogger.__table__.create(checkfirst=True)


def add_nolog(chat_id: str):
    chatid = PmLogger(str(chat_id))
    SESSION.add(chatid)
    SESSION.commit()


def del_nolog(chat_id: str):
    chatid = SESSION.query(PmLogger).get(str(chat_id))
    if chatid:
        SESSION.delete(chatid)
        SESSION.commit()


def get_all_nolog():
    chatid = SESSION.query(PmLogger).all()
    SESSION.close()
    return chatid


def is_nolog(chat_id: str):
    try:
        chatid = SESSION.query(PmLogger).get(str(chat_id))
        if chatid:
            return str(chatid.chat_id)
    finally:
        SESSION.close()
