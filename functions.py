#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, os

def loadFile(filename):
		f = open(filename,'r')
		r = f.read()
		f.close()
		return r

def saveFile(filename,data):
		f = open(filename,'w')
		f.write(data)
		f.close()

def createFileName(sufix):
		now = datetime.datetime.now()
		return  format(now.year,'02') + "." + \
                        format(now.month,'02') + "." + \
                        format(now.day,'02') + "_" + \
                        format(now.hour,'02')  + \
                        format(now.minute,'02') +  sufix
