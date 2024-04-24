alembic-init:
	alembic init --template async alembic

makemig:
	alembic revision --autogenerate -m "<name of migration>"

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1
