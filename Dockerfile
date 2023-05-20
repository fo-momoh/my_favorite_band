FROM python:3.10-slim-buster

WORKDIR /my_favorite_band

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${PORT}

ENV PYTHONBUFFERED=1

CMD [ "python3", "server.py", "--host=0.0.0.0", "--port=5000", "--debug"]