FROM python:3.11

WORKDIR /usr/src/app

COPY src/ ./src/
COPY app.py .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["flask", "run"]