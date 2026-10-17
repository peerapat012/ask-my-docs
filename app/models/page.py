import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Index, Text, func,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Pages(Base):
    __tablename__ = "pages"
    __table_args__ = (Index("ix_pages_doc_id_number", "doc_id", "number"),)
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("docs.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column()
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    
    doc: Mapped["Docs"] = relationship(back_populates="pages")