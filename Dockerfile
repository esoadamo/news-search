FROM python:3.11

WORKDIR /app
RUN pip install --no-cache-dir --upgrade waitress

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["waitress-serve", "--port=8000", "app:app"]
