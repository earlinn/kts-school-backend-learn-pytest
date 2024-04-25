alembic-init:
	alembic init --template async alembic

makemig:
	alembic revision --autogenerate -m "<name of migration>"

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

coverage-html:
	pytest --cov=blog_app --cov-report=html tests

coverage-console:
	pytest --cov=blog_app tests

# Будет падать, если покрытие меньше %, указанного в <%>, например, --cov-fail-under=90
coverage-min:
	pytest --cov=blog_app --cov-fail-under=<%> tests
