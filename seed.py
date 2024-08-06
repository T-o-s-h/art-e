from app import create_app, db
from app.models import User, Artwork, ArtistProfile, Comment

app = create_app()

# Sample data
users = [
    {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123', 'is_artist': True},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password123', 'is_artist': False},
    {'username': 'alice_jones', 'email': 'alice@example.com', 'password': 'password123', 'is_artist': True},
    {'username': 'bob_brown', 'email': 'bob@example.com', 'password': 'password123', 'is_artist': False},
    {'username': 'carol_white', 'email': 'carol@example.com', 'password': 'password123', 'is_artist': True},
]

artworks = [
    {'title': 'Sunset Bliss', 'description': 'A beautiful sunset painting.', 'price': 200.0, 'artist_id': 1},
    {'title': 'Mountain Escape', 'description': 'A serene mountain landscape.', 'price': 150.0, 'artist_id': 3},
]

artist_profiles = [
    {'user_id': 1, 'bio': 'John Doe is a contemporary artist.', 'portfolio': 'http://johnsportfolio.com'},
    {'user_id': 3, 'bio': 'Alice Jones specializes in landscape art.', 'portfolio': 'http://alicesportfolio.com'},
]

comments = [
    {'content': 'Amazing artwork!', 'user_id': 2},
    {'content': 'I love the colors!', 'user_id': 4},
]

def seed_data():
    with app.app_context():
        # Add users
        for user_data in users:
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            user.is_artist = user_data['is_artist']
            db.session.add(user)

        db.session.commit()

        # Add artworks
        for artwork_data in artworks:
            artwork = Artwork(title=artwork_data['title'], description=artwork_data['description'],
                              price=artwork_data['price'], artist_id=artwork_data['artist_id'])
            db.session.add(artwork)

        db.session.commit()

        # Add artist profiles
        for profile_data in artist_profiles:
            profile = ArtistProfile(user_id=profile_data['user_id'], bio=profile_data['bio'],
                                    portfolio=profile_data['portfolio'])
            db.session.add(profile)

        db.session.commit()

        # Add comments
        for comment_data in comments:
            comment = Comment(content=comment_data['content'], user_id=comment_data['user_id'])
            db.session.add(comment)

        db.session.commit()

if __name__ == '__main__':
    seed_data()
