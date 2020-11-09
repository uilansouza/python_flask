FROM Python:3.8.6-buster
LABEL Uilan Souza
COPY . /var/www
WORKDIR /var/www
EXPOSE 5000
