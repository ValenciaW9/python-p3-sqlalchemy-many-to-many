import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Game, Review, Base
from lib.models import User, Game, Review



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


class TestUser:
    """User in models.py"""

    def test_has_attributes(self, session):
        """has attributes id, name, created_at, updated_at, reviews, and games."""

        user = User(name="Ben")
        session.add(user)
        session.commit()

        assert hasattr(user, "id")
        assert hasattr(user, "name")
        assert hasattr(user, "created_at")
        assert hasattr(user, "updated_at")
        assert hasattr(user, "reviews")
        assert hasattr(user, "games")

        session.query(User).delete()
        session.commit()

    def test_has_many_reviews(self, session):
        """has an attribute "reviews" that is a sequence of Review records."""

        review_1 = Review(score=8, comment="Good game!")
        review_2 = Review(score=6, comment="OK game.")
        session.add_all([review_1, review_2])
        session.commit()

        user = User(name="Ben")
        user.reviews.append(review_1)
        user.reviews.append(review_2)
        session.add(user)
        session.commit()

        assert user.reviews
        assert review_1 in user.reviews
        assert review_2 in user.reviews

        session.query(Review).delete()
        session.query(User).delete()
        session.commit()

    def test_has_many_games(self, session):
        """has an attribute "games" that is a sequence of Game records."""

        game_1 = Game(title="Super Marvin Sunscreen")
        game_2 = Game(title="The Legend of Zumba: Breath of the Indoors")
        session.add_all([game_1, game_2])
        session.commit()

        user = User(name="Ben")
        user.games.append(game_1)
        user.games.append(game_2)
        session.add(user)
        session.commit()

        assert user.games
        assert game_1 in user.games
        assert game_2 in user.games

        session.query(Game).delete()
        session.query(User).delete()
        session.commit()
