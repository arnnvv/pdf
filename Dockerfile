FROM python:3.9 AS builder
WORKDIR /app
RUN pip install --no-cache-dir flask markdown_pdf gunicorn
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/
COPY main.py ./
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
