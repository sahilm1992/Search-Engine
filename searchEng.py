import os,glob,re
from bs4 import BeautifulSoup
from bs4  import  Comment
import linecache
import sys
import math

class Text:

	def __init__(self, string):
		self.text =str( string)
		self.extTags=["script"]


		#self.text = re.sub(reg,' ',self.text)
		#print ("string2"+self.text )

	def extractTags(self):
		soup =BeautifulSoup(self.text, 'html.parser')

		#[s.extract() for s in soup['script']]
		#for x in self.extTags:
		#	for y in soup.find_all(x):
		#		y.extract()

		#remove Comment
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]
		self.text= soup.get_text()

	def removeSymbols(self):
		"""
		#stopWordRegex='( a )+|( an )+|( and )+|( are )+|( as )+|( at )+|( be )+|( by )+|( for )+|( from )+|( has )+|( he )+|( in )+|( is )+|( its )+|( of )+|( on )+|( that )+|( the )+|( to )+|( was )+|( were )+|( will )+|( with )+'
		
		#for x in stopWordRegex:
		#	reg =  re.compile(x,re.IGNORECASE)#print (str(soup))
			self.text = re.sub(reg,' ',self.text)
		
		reg =  re.compile('[;]+|[,]+|[.]+|[\']+|[&]+|[\"]+|[-]+|[+]+')#print (str(soup))

		reg =  re.compile('[\s]+')#print (str(soup))
		self.text = re.sub(reg,' ',self.text)
		"""

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
		None
		#self.removeComments()
		self.extractTags()
		##reg =  re.compile('<[^<]+?>|&nbsp|&amp|<!--*?-->')#print (str(soup))
		#temp =re.sub(reg,'',self.text)
		#self.text = self.text.
		#self.printMe()
		self.removeSymbols(	)

	def printMe(self):
		None
		print("\n " + str(self.text))
	
def getFileContents(path):
	#dirList = os.listdir(path)
	#readData= file.read()

	for file in glob.glob(path):
		readData=""
		file = open(file, "r", encoding="latin-1")
		for line in file.readlines():
			readData+=line

		readData = readData.replace("\n",' ')
		readData = readData.replace("\t",' ')
		readData = readData.replace("\r",' ')

		readData =readData.encode("utf-8")
		print("file length"+ str(len(readData)))
	#print( "Read String is : ", readData)
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
		
		string = str(self.docId)+"	+" + str(self.count) + "+"
		for iter in self.posiList:
			string = string+str(iter)+","
		#string=string+"" +str(self.count)
		return string
	
	
class Dict:
	#index={} #posting List within each index[i]
	def __init__(self,path,dict1,dict2 ,numDocs):
		self.index = {}
		self.dict1=path+dict1
		self.dict2=path+dict2
		self.lineDict ={}
		self.numDocs=numDocs
		self.retrievedDictionary={}

	def insertEntry(self,key,docId,pos):
		if(key in self.index ):
				self.index[key]={}
				flag=0
				index =0 
				for iter in list :
					if(iter.docId>docId):
						entry = Entry(docId,pos)
						list.insert(index,entry)
						
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
		modulo = 0
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
		returnValue =False
		fLine = open(self.dict1, "r",encoding ="utf-8")
		readDict1 = fLine.read().split('\n')
		for iter in readDict1:
			split = iter.split(":")
			if(split[0].lower().find(key.lower())>=0 and len(split[0])== len(key)):
				print("FOUND")
				lineNum = split[1]

				#GO TO SECOND FILE
				print (split[0] + "  " + split[1])
				returnValue = linecache.getline(self.dict2,int(lineNum))

		fLine.close()
		return returnValue

	def getEntryParameters(self,entryString):
		Entry = entryString.split("+") # Entry[0] DocID  +    Entry[1] :count + Entry[2]: posiList
		count = Entry[1]
		docId = Entry[0].rstrip("\t")
		#print (Entry[2])
		posiList= Entry[2].split(",")
		posiList= posiList[0:len(posiList)-1]

		return count , docId, posiList

	def getEntries(self,lineString):
		entries=[]
		entries = lineString.split(":") # each item has Entry Data Structure
		entries = entries[1] # each item has Entry Data Structure
		return entries.split("***")

	def getRelVal(self,td,D,df):
		return td*math.log(D/df ,10)

	def relevance(self,key):
		relList={}
		lineString = self.getFromDict(key)
		if(lineString is not False):
			entriesList = self.getEntries(lineString)
			entriesList= entriesList[0:len(entriesList)-1]
			relList[key]={}
			counter =0
			for iter in entriesList:

					count,docId,posiList =self.getEntryParameters(iter)
					print ( "\n #" +key+ str(counter)+" docID: " + str(docId)  + " COUNT : " + str(count)   + " pList : " +str( posiList))
					relVal = self.getRelVal(int(count),self.numDocs,len(entriesList))
					relList[key][docId]=count,posiList,float(relVal)
					
					#relList.append([docId,posiList,float(relVal)])
					counter+=1

			relList.sort(key=lambda x: x[2],reverse=True)
			print (str(relList))
			return relList
		else:
			print (key + "  is Not Found")


	def intersectionRelList(self,relListsArray):
		relLists =sorted(relListsArray,key=len)
		# for iter in relListsArray[0])

		for iter in relLists:
			docId,posList,rel = iter[0],iter[1],iter[2]
			print(iter.docId)

		#finalSet  =set( relLists[0])
		for iter in relLists:
			finalSet  = finalSet.intersection(set(iter))
		return finalSet

#str2='<html><head><title>Wel	co me  		to	 Chill, icothe,Missouri,   &nbsp The City,in the Country!</title><meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1"><!--comm   --> pqr'

class prepareIndex:

	def __init__(self,path,path2):
		self.path = path
		self.path2 = path2

		
	def createIndex(self):
		file1=400000
		file2=402000
		self.dict =Dict(self.path2,"dict1.txt","dict2.txt",file2-file1)
		for file in range(file1,file2):
		#for file in range(408062,408065):
			fullPath = self.path +str(file)
			str1=getFileContents(fullPath)
			string = Text(str1)
			print("print ")
			#string.printMe()
			try:
				#print("print2 ")
				string.removeHTML()
				#string.printMe()

				filteredString = string.text.split(" ")
				#print(filteredString)
				#print("print3 " + str(len(filteredString)))
				pos=0
				for iter in filteredString:
					stopWordRegex=['a','an','and','are','as','at','be','by','for','from','has','he','in','is','its','of','on','that','the','to','was','were','will','with']
					if iter.lower() in stopWordRegex:
						None
					else:
						#print (dict)
						self.dict.insertEntry(iter.lower(),file,pos)
					#print("print4 ")
					pos+=1

				print("print me"+str(file))
				#print(filteredString)
			except Exception as e:
				print("EXCEPTION" +  "  " +str(e) )
				x = input(" ")
		self.dict.writeDictToFile()


if __name__ == "__main__":
	cmdArgs= sys.argv
	path ='Z:\\IIT GUWAHATI\\IR\\Data\\Set2\\'
	path2 = 'Z:\\IIT GUWAHATI\\IR\\Project\\'
	
	if len(cmdArgs)>1:
		if('p' in cmdArgs):
			indexing =prepareIndex(path,path2)
			indexing.createIndex()
		if('g' in cmdArgs):
			dict =Dict(path2,"dict1.txt","dict2.txt",2000)
			#dict.getFromDict("you")
			#dict.getFromDict("are")
			#dict.getFromDict("good")
			#dict.relevance("california")
			#x = dict.intersectionRelList([[1,0,3,5,98],[23,4,0,1],[2,3,0,1,4]])
			#print (x)
			relList=[]
			query = ["INDIAN","CITIZEN"]
			#dict.relevance((query[]))
			for iter in query:
				relList.append(dict.relevance(iter))
			print (relList)

			x = dict.intersectionRelList(relList)


