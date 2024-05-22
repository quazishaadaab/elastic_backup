FROM registry.gitlab.int.bell.ca/tvsre-tools/lib/base-images/debian:bullseye-python-3.9-dev


LABEL authors="Quazi Shaadaab"
RUN export http_proxy=http://fastweb.int.bell.ca:8083
RUN export https_proxy=http://fastweb.int.bell.ca:8083
RUN export no_proxy=localhost,gitlab.int.bell.ca,registry.gitlab.int.bell.ca,int.bell.ca


# Installing elastic-backup-files requirements through pip3
# COPY requirements.txt /var/www/jane/
RUN pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --default-timeout=1000 install -r requirements.txt