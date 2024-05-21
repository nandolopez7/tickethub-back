FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements/ /app/requirements/
RUN pip install -r requirements/local.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . /app

ENTRYPOINT ["/entrypoint"]
