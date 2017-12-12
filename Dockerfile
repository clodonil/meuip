FROM centos:latest
MAINTAINER Clodonil Trigo <clodonil@nisled.org>

#Pre-requisito
RUN yum update -y 
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm

RUN yum install -y python36u python36u-pip

#variavel
ENV EMAIL_TO  mail_to
ENV EMAIL_FROM  mail_from
ENV PASSWD   password



#Criando diretorio
RUN mkdir /app

#Copiando o script
COPY meuip.py /app
COPY entrypoint.sh /app
COPY requirements /app/
RUN  pip3.6 install --requirement /app/requirements
RUN  chmod +x /app/meuip.py /app/entrypoint.sh
RUN  chmod +x /app/entrypoint.sh

CMD [ "/app/entrypoint.sh" ]
