FROM python:3.10-alpine

WORKDIR /
COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]