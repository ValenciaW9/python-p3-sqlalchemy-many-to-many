import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import User, Game, Review
from models import User, Game, Review, Base

# Create an in-memory SQLite database for testing
SQLITE_URL = "sqlite:///:memory:"

# Create the database engine and bind it to the session
engine = create_engine(SQLITE_URL)
Session = sessionmaker(bind=engine)

# Create the tables
Base.metadata.create_all(engine)


@pytest.fixture
def session():
    """Create a new database session for each test."""
    session = Session()
    yield session
    session.rollback()
    session.close()


class TestGame:
    """Game in models.py"""

    def test_has_attributes(self, session):
        """has attributes id, title, genre, platform, price, reviews, and users."""

        game = Game(title="Corbin Air Drive")
        session.add(game)
        session.commit()

        assert hasattr(game, "id")
        assert hasattr(game, "title")
        assert hasattr(game, "genre")
        assert hasattr(game, "platform")
        assert hasattr(game, "price")
        assert hasattr(game, "reviews")
        assert hasattr(game, "users")

        # Check if the relationships are defined correctly
        assert isinstance(game.reviews, list)
        assert isinstance(game.users, list)

    def test_has_many_reviews(self, session):
        """has an attribute 'reviews' that is a sequence of Review records."""

        review_1 = Review(score=8, comment="Good game!")
        review_2 = Review(score=6, comment="OK game.")
        session.add_all([review_1, review_2])
        session.commit()

        game = Game(title="Metric Prime Reverb")
        game.reviews.append(review_1)
        game.reviews.append(review_2)
        session.add(game)
        session.commit()

        assert game.reviews
        assert review_1 in game.reviews
        assert review_2 in game.reviews

    def test_has_many_users(self, session):
        """has an attribute 'users' that is a sequence of User records."""

        user_1 = User(name="Ben")
        user_2 = User(name="Prabhdip")
        session.add_all([user_1, user_2])
        session.commit()

        game = Game(title="Super Marvin 128")
        game.users.append(user_1)
        game.users.append(user_2)
        session.add(game)
        session.commit()