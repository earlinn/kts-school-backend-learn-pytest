from blog_app.user.models import User


class TestRegisterView:
    async def test_success(self, cli):
        data = {"username": "test2", "password": "1234"}
        response = await cli.post("/user.register", json=data)
        print("response=", await response.json())
        assert response.status == 200
        user = await User.query.gino.first()
        assert await response.json() == {
            "username": user.username,
            "created": user.created.isoformat(),
            "id": user.id,
        }
