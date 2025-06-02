from pydantic import BaseModel
from datetime import datetime

# All schemas
class FileInfoCreate(BaseModel):
    file_name: str

class FileInfoResponse(FileInfoCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
