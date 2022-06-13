FROM debian:11

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y gunicorn3 python3-pip libxrender1 libxrender-dev libsm6 libxext6

RUN mkdir /opt/molecules
WORKDIR /opt/molecules

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY molecule_admin molecule_admin
COPY molecule_project molecule_project
COPY manage.py manage.py
COPY data.csv data.csv
COPY entrypoint entrypoint
ENTRYPOINT ["./entrypoint"]

