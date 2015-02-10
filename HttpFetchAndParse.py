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
    url = baseUrl + '/top-artistas/'
    data = urllib.request.urlopen(url).read()
    tree = html.fromstring(data)
    artistasLinks = tree.xpath('//div[@class="cnt_listas g-960"]//a/@href')
    outputFile = 'artistas.dat'
    f = open(outputFile,'w')
    for line in artistasLinks:
        print(line, file = f)
    f.close() 

def getArtistLetrasLink():
    directory = createDirectory('artistas')
    artistasLinks = openAndRead('artistas.dat')
    for artistLink in artistasLinks:
        url = baseUrl + artistLink;
        data = urllib.request.urlopen(url).read().decode('UTF8')
        tree = html.fromstring(data)
        letrasLinks = tree.xpath('//div[@class="cnt_listas"]//a/@href')
        filename = artistLink.replace('/', '')
        filename = filename[:-1]
        artistFile = directory + filename + '.dat'
        saveToFile(artistFile, letrasLinks)

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
                url = baseUrl + link;
                data = urllib.request.urlopen(url).read().decode('UTF8')
                tree = html.fromstring(data)
                letra = tree.xpath('//div[@id="div_letra"]//text()')
                
                letraName = str(i)
                letraFile = directory + letraName + '.txt'
                saveToFile(letraFile, letra)
                i += 1
            os.rename('artistas/' + fileName, rootDownloaded + fileName)
            print(" ---- >he bajado las letras en : " + str(time() - t0) + " seg.")




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
