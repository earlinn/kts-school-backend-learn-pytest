from blog_app.user.models import User


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
