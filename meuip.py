#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
'''
classe: Scrapy
descrição: Exercicio para buscar todos os links de um site
autor: Clodonil Honorio Trigo
email: clodonil@nisled.org
data: 04 de julho de 2017
'''

import requests
import smtplib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys


class Scrapy:
      def __init__(self):
          # links
          self.domain = ""

      def get_page(self,url):    
          '''
             Metodo que conecta na pagina
          '''
          headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

          #conecta na pagina     
          fonte = requests.get(url,headers=headers)

          #Verifica se o status é de sucesso
          if fonte.status_code == 200:
              return  BeautifulSoup(fonte.text,"lxml")
          else:
              #Apresenta a mensagem de erro
              return(False)

      

      def run(self, site,TO,FROM,PASSWD):
          '''
             Metodo para iniciar acao da classe
          '''
          page = self.get_page(site)

          ip = page.find('div', attrs={'id':'div_ip'})


          ip_antigo = self.load_ip()
          if ip_antigo != ip.text:
             self.gravar_ip(ip.text)
             self.sendmail(TO,FROM,PASSWD,ip.text)
             
          return ip.text


      def load_ip(self):
          try:
             f_ip = open('ip.txt','r')
             ip = f_ip.read()
             f_ip.close()
          except:
             ip=""
          return ip

      def gravar_ip(self,ip):
          f_ip = open('ip.txt','w')
          f_ip.write(ip)
          f_ip.close()

      def sendmail(self,TO, FROM, passwd,ip):
          SUBJECT = 'HOME: Alteracao de IP'
          TEXT = 'NOVO IP:{0}'.format(ip)

          gmail_sender = FROM
          gmail_passwd = passwd

          server = smtplib.SMTP('smtp.gmail.com', 587)
          server.ehlo()
          server.starttls()
          server.login(gmail_sender, gmail_passwd)

          BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

          try:
              server.sendmail(gmail_sender, [TO], BODY)
          except:
              print ('error sending mail')

          server.quit()

if __name__ == "__main__":
     TO   = sys.argv[1]
     FROM = sys.argv[2]
     PASSWD = sys.argv[3]
     url="http://www.meuip.com.br"
     site_connect = Scrapy()
     ip = site_connect.run(url,TO,FROM,PASSWD)
     print(ip)

