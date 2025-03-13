FROM python:3.10-slim

WORKDIR /
COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]