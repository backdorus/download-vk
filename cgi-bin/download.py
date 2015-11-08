#!/usr/bin/env python3
#__author__ = 'ilya khramtsov'


import re
from os import system, mkdir, chdir, path, walk
from zipfile import ZipFile
from urllib import request
import cgi
#import cgitb; cgitb.enable()

form = cgi.FieldStorage()
input_url = form.getfirst("url_album")
inputurl2 = input_url.find('https')
if inputurl2 == -1:
    url_album = input_url.replace("http://vk.com/album","").split("_")
else:
    url_album = input_url.replace("https://vk.com/album","").split("_")

f = open('static', 'w')
static = int(f.read())
id_groups = url_album[0]
id_albums = url_album[1]
file_name = id_albums+'.txt'
directory = id_albums

url = str(request.urlopen('https://api.vk.com/method/photos.get?owner_id='+id_groups+'&album_id='+id_albums+'&rev=1&extended=0&count=400').read())
search = re.compile(r'"src_big":"([^"]+)"')
findall = str(re.findall(search, url)).replace('\\', '').replace('\'', '').replace('[', '').replace(']', '').replace(', ', '\n')

chdir('/home/www/download-vk.ru/tmp/')
mkdir(directory)
chdir(directory)

f = open(file_name, 'w')
for line in findall:
        f.write(line)
f.close()

system('wget -i'+file_name)
system('sh down')
chdir('..')

zip=ZipFile(directory+'.zip',mode='w')
for root, dirs, files in walk(directory):
   for file in files:
        zip.write(path.join(root,file))
zip.close()

system('rm -R ./'+directory)

#####################################################
print("Content-type: text/html\n")
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Загрузка альбомов вконтакте</title>
    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <link rel="stylesheet" href="..//css/bootstrap-theme.min.css">
""")
print("""</head>
    <div class="container">
    </br>
   <div class="row-fluid">
   <div class="span12">

<div class="panel panel-default">
  <div class="panel-body">
  <nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
    </div>

    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="/">Главная <span class="sr-only">(current)</span></a></li>
          <li><a href="#">Обновления</a></li>
        <li><a href="http://бэкдор.рф">Портфолио</a></li>
          <li><a href="#">Статистика</a></li>
          <li><a href="http://бэкдор.рф/контакты/">Контакты</a></li>
    </div>
  </nav>
      <center>
  <h1>Загрузка завершена!</h1>
  <p>Архив будет хранится на сервере 30 минут.</p>
    <p><a class="btn btn-success" href=http://download-vk.ru/tmp/"""+directory+""".zip role="button">Скачать</a></p>
          </center>""")
print("""</div>
<div class="panel-footer">Copyright © <a href="http://бэкдор.рф">Бэкдор</a> | Powered by <a href="https://www.python.org/">Python</a> </div>
</div>
   </div>
   </div>
   </div>
    <script src="../js/jquery.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
</body>
</html>""")
#####################################################
static = static + 1
f.write(static)
f.close()