#!/usr/bin/env python
# author: mariano barraco <marianobarraco@gmail.com>

from __future__ import print_function
import urllib.request
from lxml import html
import requests
import re, os, sys
from time import time

baseUrl = 'http://letras.com'

def getArtistsLink():
    saveToFile('artistas.dat', getHtml(baseUrl + '/top-artistas/', '//div[@class="cnt_listas g-960"]//a/@href' ))

def getArtistLetrasLink():
    directory = createDirectory('artistas')
    artistasLinks = openAndRead('artistas.dat')
    for artistLink in artistasLinks:
        filename = artistLink.replace('/', '')
        filename = filename[:-1]
        saveToFile(directory + filename + '.dat', getHtml(baseUrl + artistLink, '//div[@class="cnt_listas"]//a/@href'))

def getArtistsLetras():
    rootLetras = createDirectory('letras')
    rootDownloaded = createDirectory('artistas-ya-descargados')
    for dirpath, dnames, fnames in os.walk('artistas'):
        for fileName in fnames:
            t0 = time()
            letrasLinks = openAndRead('artistas/' + fileName)
            directory = createDirectory(rootLetras + fileName[:-4])
            i = 0;
            for link in letrasLinks:
                saveToFile(directory + str(i) + '.txt', getHtml(baseUrl + link, '//div[@id="div_letra"]//text()'))
                i += 1
            os.rename('artistas/' + fileName, rootDownloaded + fileName)
            print(" ---- >he bajado las letras en : " + str(time() - t0) + " seg.")

def getHtml(url, xpathSelector):
    tree = html.fromstring(urllib.request.urlopen(url).read())
    return tree.xpath(xpathSelector)


def createDirectory(name):
    directory = name + '/'
    if not os.path.exists(directory):
        print("Creando directorio: " + directory)
        os.makedirs(directory)
    return directory

def openAndRead(name):
    source = open(name, 'r')
    return source.readlines()

def saveToFile(filename, listTosave):
    f = open(filename,'w')
    for line in listTosave:
        print(line, file = f)
    f.close()

t0 = time()
getArtistsLink()
print("tiempo de bajado de artistas: " + str(time() - t0))
t1 = time()
getArtistLetrasLink()
print("tiempo de bajado de indice de letras: " + str(time() - t1))
getArtistsLetras()
print("tiempo de ejecucion total: " + str(time() - t0))