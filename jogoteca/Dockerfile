FROM python:latest
LABEL key="Uilan"
COPY . /var/www
WORKDIR /var/www
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT python jogoteca.py
CMD bash
EXPOSE 5000