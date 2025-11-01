FROM python:3.9-slim
LABEL maintainer="Axanet"
LABEL description="Sistema de Gestión de Clientes"
LABEL version="1.0"
WORKDIR /app
COPY . /app/
RUN mkdir -p /app/axanet_clients_data
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]