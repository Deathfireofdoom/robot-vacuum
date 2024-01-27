FROM python:3.11

WORKDIR /usr/src/app

COPY src/ ./src/
COPY app.py .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

RUN gcc -shared -fPIC ./src/c/bitmapmemory_performance.c -o ./src/c/bitmapmemory_performance.so

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["flask", "run"]