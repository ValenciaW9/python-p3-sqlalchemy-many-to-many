
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table

Base = declarative_base()

game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    extend_existing=True,
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    reviews = relationship('Review', backref='user')
    games = relationship('Game', secondary=game_user, back_populates='users')

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    platform = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', backref='game')
    users = relationship('User', secondary=game_user, back_populates='games')

    def __repr__(self):
        return f'Game(id={self.id}, title={self.title}, platform={self.platform})'


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)

    game_id = Column(Integer, ForeignKey('games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'Review(id={self.id}, score={self.score}, game_id={self.game_id})'


if __name__ == "__main__":
    engine = create_engine("sqlite:///your_database_file.db")
    Base.metadata.create_all(engine)