from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone, timedelta
from database import Base

class FileInfo(Base):
    __tablename__ = "uploaded_file_info"
    __table_args__ = {'schema': 'cool_bot_data'}

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
