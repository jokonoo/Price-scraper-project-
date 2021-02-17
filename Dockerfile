FROM ubuntu
RUN apt-get update && apt-get upgrade -y
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
RUN apt-get install -y apache2
RUN apt-get -y install python3-pip apache2 libapache2-mod-wsgi-py3
RUN pip3 install --upgrade pip
RUN pip install djangorestframework
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD ./scraper_project.conf /etc/apache2/sites-available/scraper-project.conf
ADD . /var/www/html/public
RUN chmod 664 /var/www/html/public/db.sqlite3
RUN chmod 775 /var/www/html/public/
RUN chown :www-data /var/www/html/public/db.sqlite3
RUN chown :www-data /var/www/html/public/
EXPOSE 80
RUN a2ensite scraper-project
CMD ["apachectl", "restart"]
#CMD ["service", "apache2", "restart"]
#CMD ["systemctl","reload","apache2"]
