FROM python:3.8

WORKDIR /app

COPY . /app

ENV FLASK_APP=main.py

ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5555

RUN chmod -R 555 /app

USER nobody

CMD ["flask", "run", "-p", "5555"]
