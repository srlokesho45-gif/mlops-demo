
FROM python:3.12-slim

WORKDIR /app

COPY train.py .
COPY test_model.py .
COPY evaluate_model.py .
COPY test_evaluation.py .
COPY model_version.json .

CMD ["python3", "train.py"]
