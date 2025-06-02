from sqlalchemy.orm import Session
from models import FileInfo
from schemas import FileInfoCreate

def create_file_info(db: Session, file_info: FileInfoCreate):
    db_file = FileInfo(file_name=file_info.file_name)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def fetch_all_files(db: Session):
    return db.query(FileInfo).all()

