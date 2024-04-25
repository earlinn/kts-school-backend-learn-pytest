import uuid
from blog_app.user.models import Session, User


class TestRegisterView:
    async def test_success(self, cli):
        data = {"username": "test", "password": "1234"}
        response = await cli.post("/user.register", json=data)
        assert response.status == 200
        user = await User.query.gino.first()
        assert await response.json() == {
            "username": user.username,
            "created": user.created.isoformat(),
            "id": user.id,
        }

    async def test_already_exists(self, cli, user: User):
        data = {"username": user.username, "password": "1234"}
        response = await cli.post("/user.register", json=data)
        assert response.status == 400
        assert await response.json() == {"code": "user_already_exists"}


class TestLoginView:
    async def test_success(self, cli, user: User, mocker):
        token = "0" * 32
        mock_uuid = mocker.patch.object(uuid, "uuid4", autospec=True)
        mock_uuid.return_value = uuid.UUID(hex=token)
        data = {"username": user.username, "password": "1234"}
        response = await cli.post("/user.login", json=data)
        assert response.status == 200
        session = await Session.query.where(Session.key == token).gino.first()
        assert session.user_id == user.id
        assert await response.json() == {"token": token}
