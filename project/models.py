from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# --> deze lijn wordt gebruikt als je meerdere tables hebt en ze een relatie wilt geven

from database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    mmr = Column(Integer)
    level = Column(Integer)
