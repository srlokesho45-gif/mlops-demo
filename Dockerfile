FROM python:3.12-slim

WORKDIR /app

COPY train.py .
COPY test_model.py .

CMD ["python3", "train.py"]
