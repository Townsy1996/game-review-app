FROM python:3.10-slim AS builder
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.10-slim
# COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /install /usr/local
# ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
RUN useradd app
USER app
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]