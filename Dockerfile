FROM python

MAINTAINER Konstantin Malacnhev <hombit@gmail.com>

COPY . /house
WORKDIR /house

RUN pip install -r requirements.txt &&\
    python setup.py install

EXPOSE 15134

ENTRYPOINT ["python", "/house/bin/house_web"]