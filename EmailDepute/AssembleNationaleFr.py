# *-* coding: utf8 *-*

import urllib
import csv
import codecs
import unicodedata
import sqlite3
import re
import os
import xml.etree.ElementTree as XPATH  # https://docs.python.org/fr/2.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
import zipfile
import logging

# Codage fichier Iso-latin-1 (iso-8859-1)
# Fichier contenant le parti politique de chaque député
url1 = u"https://data.assemblee-nationale.fr/static/openData/repository/15/amo/deputes_actifs_csv_opendata/liste_deputes_excel.csv"
fname1 = u"liste_deputes_excel-ascii.csv"

# Fichier contenant les adresses email à récupérer
url2 = u"http://data.assemblee-nationale.fr/static/openData/repository/15/amo/deputes_actifs_mandats_actifs_organes_divises/AMO40_deputes_actifs_mandats_actifs_organes_divises_XV.xml.zip"
fname2 = u"liste_deputes_excel.xml"

bddName="depute1.db"
regionsName="RegionsFrancaises"
departementsName="DepartementFrancais"
partisName="GroupePolitiqueFrancais"

class PasswdDialect(csv.Dialect):
    # Séparateur de champ
    delimiter = ";"
    # Séparateur de ''chaine''
    quotechar = None
    # Gestion du separateur dans les ''chaines''
    escapechar = None
    doublequote = None
    # Fin de ligne
    lineterminator = "\r\n"
    # Ajout automatique du separateur de chaine (pour ''writer'')
    quoting = csv.QUOTE_NONE
    # Ne pas ignorer les espaces entre le delimiteur de chaine
    # et le texte
    skipinitialspace = False

class Partis():
	"Liste des partis française"
	def __init__(self):
		self.partis=[]
		try:
			self.file = open(partisName, "rt")
			logging.warning("Le fichier des partis " + partisName + " existe déjà, rien à faire")
			print("Le fichier des partis " + partisName + " existe déjà, rien à faire")
			self.partis=self.file.readlines()
			regex=re.compile("\n")
			for i in range(len(self.partis)):
				self.partis[i] =regex.sub("",self.partis[i])
			logging.warning("Les partis : " + str(self.partis))
			self.file.close()
			self.file=open(partisName,"at")
		except IOError:
			logging.warning("Le fichier des partis " + partisName + " n'existe pas, il faut le construire")
			print("Le fichier des partis " + partisName + " n'existe pas, il faut le construire")
			self.file=open(partisName,"wt")
			logging.warning("Ouverture du fichier " + partisName)
		
	def add(self,unParti):
		if unParti in self.partis:
			return
		else:
			logging.warning("Le parti " + unParti + " est ajoute dans " + str(self.partis))
			self.partis.append(unParti)
			self.file.writelines(unParti+"\n")
			self.file.flush()
			
	def get(self):
		self.partis.sort()
		return self.partis
	
	def close(self):
		self.file.close()
		
class Regions():
	"Liste des régions française"
	def __init__(self):
		self.regions=[]
		try:
			self.file = open(regionsName, "rt")
			logging.warning("Le fichier des regions " + regionsName + " existe déjà, rien à faire")
			print("Le fichier des regions " + regionsName + " existe déjà, rien à faire")
			self.regions=self.file.readlines()
			regex=re.compile("\n")
			for i in range(len(self.regions)):
				self.regions[i] =regex.sub("",self.regions[i])
			logging.warning("Les regions : " + str(self.regions))
			self.file.close()
			self.file=open(regionsName,"at")
		except IOError:
			logging.warning("Le fichier des regions " + regionsName + " n'existe pas, il faut le construire")
			print("Le fichier des regions " + regionsName + " n'existe pas, il faut le construire")
			self.file=open(regionsName,"wt")
			logging.warning("Ouverture du fichier " + regionsName)
		
	def add(self,uneRegion):
		if uneRegion in self.regions:
			return
		else:
			logging.warning("La region " + uneRegion + " est ajoutee dans " + str(self.regions))
			self.regions.append(uneRegion)
			self.file.writelines(uneRegion+"\n")
			self.file.flush()
	
	def get(self):
		self.regions.sort()
		return self.regions

	def close(self):
		self.file.close()

class Departements():
	"Liste des départements française"
	def __init__(self):
		self.departements=[]
		try:
			self.file = open(departementsName, "rt")
			logging.warning("Le fichier des departements " + departementsName + " existe déjà, rien à faire")
			print("Le fichier des departements " + departementsName + " existe déjà, rien à faire")
			self.departements=self.file.readlines()
			regex=re.compile("\n")
			for i in range(len(self.departements)):
				self.departements[i] =regex.sub("",self.departements[i])
			logging.warning("Les departements : " + str(self.departements))
		except IOError:
			logging.warning("Le fichier des departements " + departementsName + " n'existe pas, il faut le construire")
			print("Le fichier des departements " + departementsName + " n'existe pas, il faut le construire")
			self.file=open(departementsName,"wt")
			logging.warning("Ouverture du fichier " + departementsName)
	
	def add(self,unDepartement):
		if unDepartement in self.departements:
			return
		else:
			logging.warning("Le département " + unDepartement + " est ajoutee dans " + str(self.departements))
			self.departements.append(unDepartement)
			self.file.writelines(unDepartement+"\n")
			self.file.flush()
	
	def get(self):
		self.departements.sort()
		return self.departements
		
	def close(self):
		self.file.close()	
			
class AssembleNationale():
	"Liste des Députés de l'assemblée Nationale Française"
	def __init__(self):
		self.regions=Regions()
		self.departements=Departements()
		self.partis=Partis()
		
		try:
			file = open(bddName, "r")
			logging.warning("La BDD " + bddName + " existe déjà, rien à faire")
			print("La BDD " + bddName + " existe déjà, rien à faire")
			file.close()
			self.dbLoad = sqlite3.connect(bddName)
			self.cursor = self.dbLoad.cursor()
		except IOError:
			self.dbLoad = sqlite3.connect(bddName)
			self.cursor = self.dbLoad.cursor()
			logging.warning("Il faut construire la BDD " + bddName + " qui n'existe pas....")
			print("Il faut construire la BDD " + bddName + " qui n'existe pas....")
			self.init_data()
		
	def init_data(self):
		"Recherche les fichiers de données sur Internet et crée la base de données"
		
		"1. Ouverture du premir fichier contenant les noms des députés avec le nom de leurs parties"
		print "1. Recuperation du fichier " + url1 + " sur Internet"
		logging.warning( "1. Recuperation du fichier " + url1 + " sur Internet")
		try:
			sock = urllib.urlopen(url1)
		except:
			print "fichier: "+ url1 + " introuvable sur internet"
		txt = sock.read()
#		logging.info(txt)
		sock.close()
		
		"2. Transcodage du fichier de iso-8859-1 latin en ascii et sauvegarde en local"
		print "2. Transcodage du fichier de iso-8859-1 latin en ascii"
		logging.warning( "2. Transcodage du fichier de iso-8859-1 latin en ascii")
		
		txtUtf8 = txt.decode('iso-8859-1').encode('utf8')
		txtAscii = unicodedata.normalize('NFKD',txtUtf8.decode('utf8')).encode('ascii', 'ignore')
		logging.info(txtAscii)
		
		try:
			self.file1 = codecs.open(fname1,'w', encoding='ascii')
		except:
			print "Impossible de creer un fichier local dans le repertoire : " + os.getcwd()
			return
		self.file1.write(txtAscii)
		self.file1.close()
		logging.info(txtAscii)
		
		"3. Creation de la BDD locale des deputes"
		print "3.Création de la BDD locale : " + bddName
		logging.warning("3.Création de la BDD locale : " + bddName)
		self.cursor.execute('''DROP TABLE IF EXISTS depute1''') 
		self.cursor.execute('''CREATE TABLE depute1 (uid integer PRIMARY KEY, prenom text, Nom text, Region real, Departement txt, Parti text, Ab text, email text)''')
		
		self.file1 = codecs.open(fname1, "r", encoding='utf8')

		try:
			firstLine = 1
			reader = csv.reader(self.file1, PasswdDialect() )
			for row in reader:
				if firstLine == 1:
					# on passe la première ligne du fichier
					firstLine = 2
					continue
				#
				# Création des enregistrements de la BDD
				#
				logging.debug("Ligne: "+str(row))
				regex1 = re.compile('\'')
				regex2 = re.compile('\"')
				for i in range(8):
					row[i] = regex1.sub(' ',row[i])
					row[i] = regex2.sub('',row[i],2)
				command = "INSERT INTO depute1 VALUES ( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' );".format(int(row[0]), row[1], row[2], row[3], row[4], row[7], row[8], " ")
				self.regions.add(row[3])
				self.departements.add(row[4])
				self.partis.add(row[7]+"("+row[8]+")")
				logging.debug(command)
				self.cursor.execute(command)
				self.dbLoad.commit()
		finally:
			pass
			
		"4. Récupération d'un autre fichier sur Internet pour récupérer les adresses email des députés"
		print "4. Recuperation sur Internet du fichier " + url2 + " pour recuperer les adresses email des deputes"
		logging.warning( "4. Recuperation sur Internet du fichier " + url2 + " pour recuperer les adresses email des deputes")

		urllib.urlretrieve(url2,"assemNat-1.zip")
		with zipfile.ZipFile("assemNat-1.zip", 'r') as zip_ref:
			zip_ref.extractall(".")

		fileList = os.listdir("./acteur")
		
		"5. Modification de la BDD pour ajouter les adresses email de chaque députés"  
		print "5. Modification de la BDD pour ajouter les adresses email de chaque deputes"
		logging.warning("Modification de la BDD pour ajouter les adresses email de chaque deputes")
		
		regex2=re.compile('.+@assemblee-nationale.fr')
		for file in fileList:
			regex1=re.compile("PA([0-9]*).xml")
			res=regex1.search(file)
			if not res:
				continue
		
			logging.debug(file)
			id = int(res.group(1))
			
			command = "SELECT * FROM depute1 WHERE uid = {};".format(id)
			logging.debug(command)
			self.cursor.execute(command)
			row = self.cursor.fetchall()
			logging.debug(row)
	
			tree = XPATH.parse("./acteur/" + file)
			root = tree.getroot()
			logging.debug(root.tag)
	
			for child in root:
				logging.debug(child.tag)
    
			for email in root.iter('valElec'):
				res = regex2.search(email.text)
				if res:
					command = "REPLACE INTO depute1 (uid, prenom, Nom, Region, Departement, Parti, Ab, email) VALUES ( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(int(row[0][0]), row[0][1], row[0][2], row[0][3], row[0][4], row[0][5], row[0][6], email.text)
					logging.debug(command)
					self.cursor.execute(command)
					self.dbLoad.commit()
		
		self.regions.close()
		self.departements.close()
		self.partis.close()
		print "6. Fin de l'initialisation des donnees"
		logging.warning("6. Fin de l'initialisation des donnees")
			
	def getRegions(self):
		return self.regions.get()
		
	def getDepartements(self):
		return self.departements.get()
		
	def getPartis(self):
		return self.partis.get()
		
	def getSelectionAll(self):
		#Cas 01 : Selection de tous les email
		command = "SELECT email FROM depute1;"
		logging.warning("Cas 01 : " + command)
		self.cursor.execute(command)
		row = self.cursor.fetchall()
		logging.debug(row)
		return row
		
	def getSelectionParti(self,parti):
		#Cas 02 : Sélection des email par parti
		command = "SELECT email FROM depute1 WHERE Parti = '{}';".format(str(parti))
		logging.warning("Cas 02 : " + command)
		self.cursor.execute(command)
		row = self.cursor.fetchall()
		logging.debug(row)
		return row
	
	def getSelection(self,parti, geo, geoType):
		
		if geoType== 'depart':
			#Cas 03 : Sélection sur le  parti et le département
			command = "SELECT email FROM depute1 WHERE Parti = '{}' AND Departement = '{}' ;".format(parti, geo)
			logging.warning("Cas 03 : " + command)
			self.cursor.execute(command)
			row = self.cursor.fetchall()
			logging.debug(row)
			return row
		elif geoType== 'region':
			#Cas 04 : Sélection sur le  parti et la région
			command = "SELECT email FROM depute1 WHERE Parti = '{}' AND Region = '{}' ;".format(parti, geo)
			logging.warning("Cas 04 : " + command)
			self.cursor.execute(command)
			row = self.cursor.fetchall()
			logging.debug(row)
			return row
		else:
			logging.warning("Sélection inconnue")
			return None
			

	def getSelectionDepartement(self, geo):
			#Cas 05 : Sélection sur le  département
			command = "SELECT email FROM depute1 WHERE Departement = '{}' ;".format(geo)
			logging.warning("Cas 05 : " + command)
			self.cursor.execute(command)
			row = self.cursor.fetchall()
			logging.debug(row)
			return row

	def getSelectionRegion(self, geo):
			#Cas 06 : Sélection sur la région
			command = "SELECT email FROM depute1 WHERE Region = '{}' ;".format(geo)
			logging.warning("Cas 06 : " + command)
			self.cursor.execute(command)
			row = self.cursor.fetchall()
			logging.debug(row)
			return row
			
	def closeBdd(self):
		logging.warning("Fermeture de la BDD : " + bddName)
		self.cursor.close()
		self.dbLoad .close()
		logging.warning("Fermeture fichier : " + regionsName)
		self.regions.close()
		logging.warning("Fermeture fichier : " + departementsName)
		self.departements.close()
		logging.warning("Fermeture fichier : " + partisName)
		self.partis.close()
		
# Programme principal
if __name__ == '__main__' :
	
	logging.basicConfig(filename='trace.log',filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
	
	app = AssembleNationale()
	regions = app.getRegions()
	for reg in regions:
		print reg				
			


