from app.domain.subscriber.entity import Subscriber


def test_can_create_subscriber():
    Subscriber.create(id="test", first_name="User", last_name="Name")
