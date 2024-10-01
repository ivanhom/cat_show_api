FROM python:3.11-slim

WORKDIR /app

RUN apt update && \
    apt install -y netcat-traditional curl && \
    apt clean autoclean && apt autoremove --yes

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x docker-entrypoint.bash

EXPOSE 8000

CMD ["./docker-entrypoint.bash"]
