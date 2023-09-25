from shared import db_models
from shared import schemas


def test_get_message(db, message):
    msg_obj = db_models.get_message(db, message.id)

    assert isinstance(msg_obj, db_models.Message)
    assert message.from_ == msg_obj.from_
    assert message.to == msg_obj.to
    assert message.content == msg_obj.content
    assert message.id == msg_obj.id


def test_create_msg(db):
    msg_schema = schemas.MessageUserSchema(from_=1, to=2, content="Hi")

    saved_msg = db_models.create_messge(db, msg_schema)
    db_models.save_obj(db, saved_msg)

    msg_obj = db_models.get_message(db, saved_msg.id)

    assert msg_schema.from_ == msg_obj.from_
    assert msg_schema.to == msg_obj.to
    assert msg_schema.content == msg_obj.content
    assert isinstance(msg_obj.id, int)
