#!/usr/bin/env python
# author: mariano barraco <marianobarraco@gmail.com>
# 02 Aug 2014

from __future__ import print_function
import urllib.request
from lxml import html
import requests
import re, os

baseUrl = 'http://letras.com'

def getArtistsLink():
    url = baseUrl + '/top-artistas/'
    print url;
    # data = urllib.request.urlopen(url).read()
    # tree = html.fromstring(data)
    # artistasLinks = tree.xpath('//div[@class="cnt_listas g-960"]//a/@href')
    # outputFile = 'artistas.dat'
    # f = open(outputFile,'w')
    # for line in artistasLinks:
    #     print(line, file = f)
    # f.close() 

def getLetrasLink():
    # xpath : cnt_listas
    directory = 'artistas/'
    if not os.path.exists(directory):
        print("Creando directorio: artistas/")
        os.makedirs(directory)
    
    source = open('artistas.dat', 'r')
    artistasLinks = source.readlines()
    for link in artistasLinks[1]:
        url = baseUrl + link;
        data = urllib.request.urlopen(url).read()
        tree = html.fromstring(data)
        letrasLinks = tree.xpath('//div[@class="cnt_listas"]//a/@href')
        outputFile = 'artistas/' + link.replace('/', '') + 'Links.dat'
        f = open(outputFile,'w')
        for line in letrasLinks:
            print(line, file = f)
        f.close() 
    

getArtistsLink()
getLetrasLink()

# url = 'http://letras.com' + '/thalia/478664/'
# data = urllib.request.urlopen(url).read()
# data = data.decode('UTF8')
# tree = html.fromstring(data)
# letra = tree.xpath('//div[@id="div_letra"]//text()')

# metaLineDelimiters = ["[", "("]

# f = open('thalia.letra','w')
# for line in letra:
#     line = re.sub('\(.*?\)','', line)
#     line = re.sub('\[.*?\]','', line)
#     print(line, file=f)
# # letra = letra.replace("\n", "")
# # print(letra)
# f.close() # you can omit in most cases as the destructor will call if
