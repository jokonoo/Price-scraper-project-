FROM ubuntu:latest

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 python3.8 python3-pip libapache2-mod-wsgi-py3

RUN pip3 install --upgrade pip

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD ./scraper_project.conf /etc/apache2/sites-available/scraper_project.conf
ADD . /var/www/html/public

WORKDIR /var/www/html/public

RUN chown -R :www-data .
RUN chmod -R 775 . 

EXPOSE 80

RUN a2ensite scraper_project
RUN a2dissite 000-default

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
