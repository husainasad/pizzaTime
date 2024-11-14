python -m venv .pizza_venv
.pizza_venv\Scripts\activate.bat
pip install fastapi uvicorn
python -m pip install --upgrade pip

alembic init alembic

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

uvicorn app.main:app --reload