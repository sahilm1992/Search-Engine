import os,glob,re
from bs4 import BeautifulSoup
import linecache
import sys

class Text:

	def __init__(self, string):
		self.text = string
	def extractTags(self,tag):
		soup =BeautifulSoup(self.text, 'html.parser')
		for x in soup.findAll(tag):
			x.extract()
			self.text= str(soup)
	def removeSymbols(self):
		#stopWordRegex='( a )+|( an )+|( and )+|( are )+|( as )+|( at )+|( be )+|( by )+|( for )+|( from )+|( has )+|( he )+|( in )+|( is )+|( its )+|( of )+|( on )+|( that )+|( the )+|( to )+|( was )+|( were )+|( will )+|( with )+'
		
		#for x in stopWordRegex:
		#	reg =  re.compile(x,re.IGNORECASE)#print (str(soup))
		#	self.text = re.sub(reg,' ',self.text)
		
		#reg =  re.compile('[;]+|[,]+|[.]+|[\']+|[&]+|[\"]+|[-]+|[+]+')#print (str(soup))
		reg =  re.compile('[\W]+')#print (str(soup))
		self.text = re.sub(reg,' ',self.text)
		
		#reg =  re.compile(stopWordRegex,re.IGNORECASE)#print (str(soup))
		#self.text = re.sub(reg,' ',self.text)
		
		
		reg =  re.compile('[ ]+')#print (str(soup))
		self.text = re.sub(reg,' ',self.text)
		
		#reg =  re.compile('[\n]|[\t]|[\r]')#print (str(soup))
		#self.text = re.sub(reg,'',self.text)
		
		
		self.text = self.text.strip()
		
	def removeHTML(self):			
		reg =  re.compile('<[^<]+?>|&nbsp|&amp|<!--*?-->')#print (str(soup))
		self.text = re.sub(reg,'',self.text)
		self.printMe()
		self.removeSymbols(	)
		
		

		
	def printMe(self):
		None
		print("\n " + str(self.text))
	
def getFileContents(path):
	#dirList = os.listdir(path)
	for file in glob.glob(path):
		
		file = open(file, "r", encoding="latin-1")
		readData= file.read(90000)
		readData = readData.replace("\n",'')
		
		readData =str(readData.encode("utf-8"))
		#print( "ead String is : ", readData)
	file.close()
	return readData
	

class Entry:
	
	def __init__(self, docId,pos):
		self.docId = docId
		self.count = 1
		self.posiList =[pos]  #position array
		
	def insertNumInEntry(self,pos):
		posInsert=0
		self.posiList.append(pos)
		self.count= self.count +1
		self.posiList.sort()
	
	def printEntry(self):
		print(" ID: " + str(self.docId) +   " C: "  + str(self.count) +" POS: <" + str(self.posiList) + " >")
		#	for iter in self.posiList:
		#		print(iter)
		#print(" >")
	def getEntryString(self):
		
		string = str(self.docId)+"	+"
		for iter in self.posiList:
			string = string+str(iter)+","
		#string=string+"" +str(self.count)
		return string
	
	
class Dict:
	#index={} #posting List within each index[i]
	def __init__(self,path,dict1,dict2 ):
		self.index = {}
		self.dict1=path+dict1
		self.dict2=path+dict2
	def insertEntry(self,key,docId,pos):
		if(key in self.index ):
				list = self.index[key]
				flag=0
				index =0 
				for iter in list :
					if(iter.docId>docId):
						entry = Entry(docId,pos)
						list.insert(index,iteentry)
						
					elif(iter.docId == docId):
						entry = iter	
						flag=1
						entry.insertNumInEntry(pos)
						break
					
					index+=1
				
				if (flag==0):
					entry = Entry(docId,pos)
					list.append(entry)
					
		else:
				entry =Entry(docId,pos)
				self.index[key] = []
				self.index[key].append(entry)
				#print (self.index[key])
				
	def printDict(self):
		for key in sorted(self.index):
			print ( key)
			for link in self.index[key]:
				link.printEntry() 	
	#EACH DOC ID SPLIT AT ***
	#WITHIN EACH ENTRY, LEFT to + is docID , right to + is posiList(positions)
	#WITHIN EACH posiList(positions) , separation by comma
	def writeDictToFile(self):
		fLine = open(self.dict1, "w", encoding='utf-8')
		fFull = open(self.dict2, "w", encoding='utf-8')
		
		lineString=""
		fullString =""
		count = 1 ; 
		for key in sorted(self.index):
			lineString =lineString + key + ":" +str( count) +"\n"
			fullString=str(count) + " : "
			for link in self.index[key]:
				fullString =fullString  + link.getEntryString() +"***"
			
			fFull.write(fullString)
			fFull.write('\n')
			count+=1
		fLine.write(lineString)
			
		fLine.close()
		fFull.close()	
		
	def getFromDict(self,key):
		fLine = open(self.dict1, "r",encoding ="utf-8")
		lineDict ={}
		readDict1 = fLine.read().split('\n')
		for iter in readDict1:
			split = iter.split(":")
			if(split[0].find(key)>=0 and len(split[0])== len(key)):
				print("FOUND")
				lineNum = split[1]
				#GO TO SECOND FILE
				print (split[0] + "  " + split[1])
				fullLine = linecache.getline(self.dict2,int(lineNum))
				print ( fullLine)
		#print (readDict1)
		#lineNumber = linecache.getline(self.dict1, key)
		fLine.close()
		

str2='<html><head><title>Wel	co me  		to	 Chill, icothe,Missouri,   &nbsp The City,in the Country!</title><meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1"><!--comm   --> pqr'

class prepareIndex:

	def __init__(self,path,path2):
		self.path = path
		self.path2 = path2
		self.extTags=['script']

		
	def createIndex(self):
		self.dict =Dict(self.path2,"dict1.txt","dict2.txt")
	
		for file in range(408066,408067):
			fullPath = self.path +str(file)
			str1=getFileContents(fullPath)
			string = Text(str1)
			string.printMe()
			"""
			for x in self.extTags:
				string.extractTags(x)
			
			string.printMe()
			
			filteredString = string.text.split(" ")
			#print(filteredString)
			pos=0
			for iter in filteredString:
				stopWordRegex=['a','an','and','are','as','at','be','by','for','from','has','he','in','is','its','of','on','that','the','to','was','were','will','with']
				if iter.lower() in stopWordRegex:
					None 
				else:
					#print (dict)
					self.dict.insertEntry(iter.lower(),file,pos)
					pos+=1
		#self.dict.writeDictToFile()
			"""

if __name__ == "__main__":
	cmdArgs= sys.argv
	path ='Z:\\IIT GUWAHATI\\IR\\Data\\Set2\\'
	path2 = 'Z:\\IIT GUWAHATI\\IR\\Project\\'
	
	if len(cmdArgs)>1:
		if('prepare' in cmdArgs):
			indexing =prepareIndex(path,path2)
			indexing.createIndex()
		if('get' in cmdArgs):		
			dict =Dict(path2,"dict1.txt","dict2.txt")
			dict.getFromDict("you")
			dict.getFromDict("are")
			dict.getFromDict("good")
			

			
