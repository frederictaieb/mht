from sqlalchemy.orm import Session
from app.models.telepai.line import Line
from app.models.telepai.speech import Speech
from app.models.telepai.profile import Profile
from app.schemas.telepai.line import LineCreate


def create_line(line: LineCreate, db: Session):
    db_speech = db.query(Speech).filter(Speech.id == line.speech_id).first()
    if db_speech is None:
        return None, "speech_not_found"

    db_profile = db.query(Profile).filter(Profile.id == line.profile_id).first()
    if db_profile is None:
        return None, "profile_not_found"

    existing_line = db.query(Line).filter(
        Line.speech_id == line.speech_id,
        Line.line_order == line.line_order
    ).first()

    if existing_line is not None:
        return None, "line_order_exists"

    db_line = Line(
        speech_id=line.speech_id,
        profile_id=line.profile_id,
        line_order=line.line_order,
        text=line.text
    )

    db.add(db_line)
    db.commit()
    db.refresh(db_line)

    return db_line, None


def get_all_lines(db: Session):
    return db.query(Line).order_by(Line.speech_id, Line.line_order).all()


def get_line(line_id: int, db: Session):
    return db.query(Line).filter(Line.id == line_id).first()


def delete_line(line_id: int, db: Session):
    db_line = db.query(Line).filter(Line.id == line_id).first()

    if db_line is None:
        return None

    db.delete(db_line)
    db.commit()

    return db_line