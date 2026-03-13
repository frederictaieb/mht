#from sqlalchemy.orm import Session
#from app.models.telepai import Actress
#from app.schemas.telepai import CharacterCreate


#def create_actress(db: Session, actress: CharacterCreate):
#    db_actress = Actress(name=actress.name)
#    db.add(db_actress)
#    db.commit()
#    db.refresh(db_actress)
#    return db_actress


#def get_actress(db: Session, actress_id: int):
#    return db.query(Actress).filter(Actress.id == actress_id).first()


#def get_all_actresses(db: Session):
#    return db.query(Actress).all()


#def delete_actress(db: Session, actress_id: int):
#    db_actress = db.query(Actress).filter(Actress.id == actress_id).first()

#    if db_actress is None:
#        return None

#    db.delete(db_actress)
#    db.commit()
#    return db_actress