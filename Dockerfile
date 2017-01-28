FROM python

MAINTAINER Konstantin Malacnhev <hombit@gmail.com>

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /house
WORKDIR /house

COPY requirements.txt /house/
RUN pip install -r requirements.txt

COPY . /house
RUN python setup.py install

EXPOSE 15134

ENTRYPOINT ["python", "/house/bin/house_web"]
