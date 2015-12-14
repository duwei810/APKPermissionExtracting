#!usr/bin/python
#coding:utf8
import os
import numpy as np
from xml.parsers.expat import ParserCreate
class PermissionExtraction(object):
	def __init__(self):
		self.path = "/Users/duwei/Desktop/apk"
		self.permission = []
		self.dict = {}
		self.dicts = {}
	def start_element(self,name,attrs):
		if name == "uses-permission":
			str = attrs["android:name"].split(".")
			n = len(str)
			self.permission.append(str[n-1])
	def getFiledict(self,path):
		for dirname in os.listdir(path):
			pathname1 = os.path.join(path,dirname)
			for appname in os.listdir(pathname1):
				pathname2 = os.path.join(pathname1,appname)
				if os.path.exists(os.path.join(pathname2,"AndroidManifest.xml")):
					self.dict[appname] = os.path.join(pathname2,"AndroidManifest.xml")
	def getPermissiondict(self):
		for appname,xmlpath in self.dict.items():
			self.permission = []
			parser = ParserCreate()
			parser.StartElementHandler = self.start_element
			f1 = open(xmlpath,"rb")
			parser.ParseFile(f1)
			self.dict[appname] = self.permission
			f1.close()
	def getCountdict(self):
		for appname,pername in self.dict.items():
			for i in pername:
				if i in self.dicts:
					self.dicts[i] = self.dicts[i]+1
				else:
					self.dicts[i] = 1
	def getMaxtrix(self):
		tran = []
		for appname,pername in self.dict.items():
			tmp = []
			for keyper in self.dicts:
				if keyper in pername:
					tmp.append("1")
				else:
					tmp.append("0")
			tran.append(tmp)
		return tran
	def getFiletxt(self):
		f2 = open("pernum.txt","w")
		for pername,number in self.dicts.items():
			f2.write(pername+":"+str(number)+"\n")
		f2.close()
		f3 = open("out.txt","w")
		trans = np.array(self.getMaxtrix())
		np.savetxt("out.txt",trans,fmt=["%s"]*trans.shape[1],newline='\n')
		f3.close()
	def start(self):
		self.getFiledict(self.path)
		self.getPermissiondict()
		self.getCountdict()
		self.getFiletxt()

pe = PermissionExtraction()
pe.start()



