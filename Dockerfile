FROM python:3.8-alpine      

# options
ENV PYTHONUNBUFFERED 1

RUN addgroup -S app && adduser -S app -G app

# Set working directoryad
RUN mkdir praxsa_manager
# set the working directory
WORKDIR /praxsa_manager/

ENV HOME=/praxsa_manager/

COPY praxsa_manager/ ./praxsa_manager
COPY product/ ./product
# COPY .env-prod ./.env
COPY requirements-3.8.10.txt .
COPY manage.py ./

# update docker-iamage packages
RUN apk update 
RUN apk upgrade --available
RUN apk add netcat-openbsd gcc libc-dev gpgme-dev 
RUN apk add postgresql-dev

# update pip 
RUN pip install --upgrade pip
# install psycopg for connect to pgsql
RUN pip install psycopg2-binary
# install python packages 
RUN pip install -r requirements-3.8.10.txt
# create static directory
RUN mkdir staticfiles
RUN mkdir static
RUN chown app:app staticfiles
RUN chown -R app:app $HOME

# USER app

# CMD ["python", "manage.py", "collectstatic"]
# WORKDIR /web_app/praxsa_manager

EXPOSE 5000
CMD ["gunicorn","--bind", "0.0.0.0:5000", "praxsa_manager.wsgi:application"]