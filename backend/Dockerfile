FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.10-slim
COPY --from=builder /install /usr/local
WORKDIR /app
COPY . .
RUN useradd app
USER app
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]