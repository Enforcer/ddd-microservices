FROM python:3.11.0

WORKDIR /usr/src/app
COPY requirements/app.txt .
COPY requirements/dev.txt .
RUN pip install -r app.txt -r dev.txt && rm app.txt dev.txt

CMD echo "Hello, world!"
