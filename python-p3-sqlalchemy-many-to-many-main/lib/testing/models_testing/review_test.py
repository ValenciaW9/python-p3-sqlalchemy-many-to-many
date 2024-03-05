import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Game, Review, Base

# Create an in-memory SQLite database for testing
SQLITE_URL = "sqlite:///:memory:"

# Create the database engine and bind it to the session
engine = create_engine(SQLITE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@pytest.fixture
def session():
    """Create a new database session for each test."""
    session = Session()
    yield session
    session.rollback()
    session.close()


class TestReview:
    """Review in models.py"""

    def test_has_attributes(self, session):
        """has attributes id, score, comment, game_id, and user_id."""

        review = Review(score=2, comment="Very bad!")
        session.add(review)
        session.commit()

        assert hasattr(review, "id")
        assert hasattr(review, "score")
        assert hasattr(review, "comment")
        assert hasattr(review, "game_id")
        assert hasattr(review, "user_id")

        session.query(Review).delete()
        session.commit()

    def test_has_one_user_id(self, session):
        """has an attribute "user_id", an int that is a foreign key to the users table."""

        user = User(name="Ben")
        session.add(user)
        session.commit()

        review = Review(score=4, comment="Fairly bad!")
        review.user_id = user.id
        session.add(review)
        session.commit()

        assert type(review.user_id) == int
        assert review.user_id == user.id

        session.query(User).delete()
        session.query(Review).delete()
        session.commit()

    def test_has_one_user(self, session):
        """has an attribute "user" in the ORM that is a record from the users table."""

        user = User(name="Ben")
        session.add(user)
        session.commit()

        review = Review(score=4, comment="Fairly bad!")
        review.user = user
        session.add(review)
        session.commit()

        assert review.user
        assert review.user_id == user.id
        assert review.user == user

        session.query(User).delete()
        session.query(Review).delete()
        session.commit()

    def test_has_one_game_id(self, session):
        """has an attribute "game_id", an int that is a foreign key to the games table."""

        game = Game(title="Javelinna")
        session.add(game)
        session.commit()

        review = Review(score=9, comment="Iconic.")
        review.game_id = game.id
        session.add(review)
        session.commit()

        assert type(review.game_id) == int
        assert review.game_id == game.id

        session.query(Game).delete()
        session.query(Review).delete()
        session.commit()

    def test_has_one_game(self, session):
        """has an attribute "game" in the ORM that is a record from the games table."""

        game = Game(title="Shady Spirits")
        session.add(game)
        session.commit()

        review = Review(score=10, comment="GGOAT")
        review.game = game
        session.add(review)
        session.commit()

        assert review.game
        assert review.game_id == game.id
        assert review.game == game

        session.query(Game).delete()
        session.query(Review).delete()
        session.commit()