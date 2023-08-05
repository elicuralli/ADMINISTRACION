FROM python:3-alpine
RUN apk update \
&& apk upgrade --no-cache

# Set an environment variable with the directory
# where we’ll be running the app
ENV APP /app
# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP
# Copy the requirements file in order to install
# Python dependencies
COPY ./requirements.txt .
# Install Python dependencies
RUN \
 apk add --no-cache postgresql-libs linux-headers && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# We copy the rest of the codebase into the image
COPY . .
# Finally, we run uWSGI with the ini file we
# created earlier
CMD ["uwsgi","src/app.ini"]