FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ /app/

CMD alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 5000