FROM python:3-alpine

RUN apk update && apk upgrade --no-cache

ENV APP /app
RUN mkdir $APP
WORKDIR $APP

COPY ./requirements.txt .
RUN apk add --no-cache postgresql-libs linux-headers && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
