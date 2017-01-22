FROM python

MAINTAINER Konstantin Malacnhev <hombit@gmail.com>

RUN mkdir -p /house
WORKDIR /house

COPY requirements.txt /house/
RUN pip install -r requirements.txt

COPY . /house
RUN python setup.py install

EXPOSE 15134

ENTRYPOINT ["python", "/house/bin/house_web"]