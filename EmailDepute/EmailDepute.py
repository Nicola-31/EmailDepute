# *-* coding: utf8 *-*

appli = " Assemble Nationale fr "
__version__ = "1.1.2021"
appli_ver = appli + "V"+ __version__

import ttk
import sqlite3
import tkFileDialog
from PIL import Image, ImageTk
from tkMessageBox import *
from Tkinter import * 
from AssembleNationaleFr import *
import re

class Accueil_tk(Tk):
	def __init__(self,parent):
		Tk.__init__(self,parent)
		self.parent = parent
		self.title(appli_ver)
		self.assemb = AssembleNationale()
		self.selectionParti = 'Tous les partis("Tous les partis")'
		self.selectionRegion = "Toutes les regions"
		self.selectionDepart ="Tous les départements"
		self.ligne = 1
		self.colonne = 1
		self.initialize() #Toujours en dernier (main loop)
		
	def initialize(self):

		# Initialisation frame 0 TOP ###########################
# 		frame0 = Frame(self)
#		frame0.pack(side=TOP)
	
		# Image
#		photo = PhotoImage(file="Logo_Assemblee_nationale_francaise.gif")
		
#		canvas1 = Canvas(frame0, width=1140, height=185)
#		canvas1.create_image(0,0,anchor=NW, image=photo)
#		canvas1.pack()
				
		# Initialisation frame 1 MIDDLE ###########################
		frame1 = Frame(self)
		frame1.pack()
		
		# Boite texte
		frame11 = Frame(frame1)
		frame11.pack(side=LEFT, padx=10)

		lb_frame111 = LabelFrame(frame11, text="Adresses mail", padx=10, pady=10)
		lb_frame111.grid()

		# Sous boite Adresses mail
		self.ed_txt = Text(lb_frame111, width=60, height=32, bg='ivory',selectbackground='black', selectforeground='white')
		self.ed_txt.pack(padx=5, pady=5)
		
		# Boite de sélection des députés
		frame12 = Frame(frame1)
		frame12.pack(side=RIGHT, padx=10, expand=1)
		
		lb_frame121 = LabelFrame(frame12, text="Selection des deputes", padx=10, pady=10)
		lb_frame121.grid()
		
		# Sous boite "Sélection du parti" ***************************************************
		lb_frame1211 = LabelFrame(lb_frame121, text="Selection du parti (double clic)", padx=20, pady=20)
		lb_frame1211.grid(column=1, row=0, columnspan=3, sticky=N+S+E+W, padx=10, pady=10)

		self.listPartis = []
		self.list_partis = Listbox(lb_frame1211, exportselection=0, height=3,relief=RAISED,width=52, listvariable = self.listPartis, selectmode="single",selectbackground='black',selectforeground='white')
		# exportselection=0 : pour que la sélection reste en surbrillance, même si on clique sur un autre objet
		self.list_partis.bind("<Button-1>",self.onListPartis_click) #clic gauche
		self.list_partis.insert(0, 'Tous les partis("Tous les partis")')
		self.listPartis.append('Tous les partis("Tous les partis")')
		i=1
		for parti in self.assemb.getPartis():
			self.listPartis.append(parti)
			self.list_partis.insert(i, parti)
			i = i+1
		self.list_partis.pack()
		
		# Sous boite "choix par région ou par département
		lb_frame1214 = LabelFrame(lb_frame121, text="Choix geographique ", padx=40, pady=20)
		lb_frame1214.grid(column=1, row=1)
		
		self.radioButtonValue = StringVar()
		self.radioButtonValue.set('')
		self.regionButton = Radiobutton(lb_frame1214, text="Region     ",command=self.regionRadioButton_click,variable=self.radioButtonValue, value="region")
		self.regionButton.grid()
		
		self.departButton = Radiobutton(lb_frame1214, text="Departement",command=self.departRadioButton_click,variable=self.radioButtonValue, value="depart")
		self.departButton.grid()

		# Sous boite "Selection courante
		lb_frame1215 = LabelFrame(lb_frame121, text="Selection courante ", padx=40, pady=20)
		lb_frame1215.grid(column=3, row=1)
		
		self.label1 = Label(lb_frame1215, text="Tous les partis", width=25)
		self.label1.pack(anchor=NW)
		self.selectionParti = 'Tous les partis("Tous les partis")'
		
		self.label2 = Label(lb_frame1215, text="Toutes les régions", width=25)
		self.label2.pack(anchor=NW)
		
		self.selectionDepart=="Tous les départements"
		
		# Sous boite "Sélection de la région" ***************************************************
		lb_frame1212 = LabelFrame(lb_frame121, text="Selection de la region (double clic)", padx=40, pady=20)
		lb_frame1212.grid(column=1, row=2, columnspan=3, sticky=N+S+E+W, padx=10, pady=10)

		self.listRegions = []
		self.list_regions = Listbox(lb_frame1212, exportselection=0, height=3,relief=RAISED,width=52, listvariable = self.listRegions, selectbackground='black',selectforeground='white')
		# exportselection=0 : pour que la sélection reste en surbrillance, même si on clique sur un autre objet
		self.list_regions.bind("<Button-1>",self.onListRegions_click) #clic gauche
		self.list_regions.insert(0, 'Toutes les regions')
		self.listRegions.append('Toutes les regions')
		i=1
		for region in self.assemb.getRegions():
			self.listRegions.append(region)
			self.list_regions.insert(i, region)
			i = i+1
		self.list_regions.pack()
		self.list_regions.configure(state='disabled')
		
		# Sous boite "Sélection du departement" ***************************************************
		lb_frame1213 = LabelFrame(lb_frame121, text="Selection du département (double clic)", padx=40, pady=20)
		lb_frame1213.grid(column=1, row=3, columnspan=3, sticky=N+S+E+W, padx=10, pady=10)

		self.listDeparts = []
		self.list_departs = Listbox(lb_frame1213, exportselection=0, height=3,relief=RAISED,width=52, listvariable = self.listDeparts, selectmode="single",selectbackground='black',selectforeground='white')
		# exportselection=0 : pour que la sélection reste en surbrillance, même si on clique sur un autre objet
		self.list_departs.bind("<Button-1>",self.onListDeparts_click) #clic gauche
		self.list_departs.insert(0, 'Tous les départements')
		self.listDeparts.append('Tous les départements')
		i=1
		for depart in self.assemb.getDepartements():
			self.listDeparts.append(depart)
			self.list_departs.insert(i, depart)
			i = i+1
		self.list_departs.pack()
		self.list_departs.configure(state='disabled')

		# bouton de sortie
		self.boutonOK=Button(lb_frame121, text="Appliquer la selection", padx=20, command=self.globalSelection_click)
		self.boutonOK.grid(row=4,column=0,columnspan=3)
		
		#Bouton de reset de la sélection
		#self.boutonReset=Button(lb_frame121, text="Re-initialiser la selection", padx=20, command=self.globalSelectionReset_click)
		#self.boutonReset.grid(row=4,column=3,columnspan=3)

		# Initialisation frame 2 BOTTOM ###########################
		frame2 = Frame(self, padx=20, pady = 20)
		frame2.pack(side=BOTTOM)
		
		self.boutonReload=Button(frame2, text="Recharger les donnees depuis internet", padx=20, command=self.globalReload_click)
		self.boutonReload.grid(row=1,column=15)

		self.mainloop()

	def onListPartis_click(self, event):
		"Traitement de la sélection du parti"
		index = self.list_partis.curselection()
		if index != ():
			#logging.warning("Liste des valeurs : " + str(self.listPartis))
			logging.warning("Index : " + str(index)+ " " + str(type(index)))
			for ind in index:
				logging.warning("ind : " + str(ind) + " " + str(type(ind)))
				self.selectionParti = self.listPartis[ind]
			logging.warning("Selection : " + str(self.selectionParti)+ " " + str(type(self.selectionParti)))
			regex=re.compile('.*\("(.*)"\)')
			res=regex.search(self.selectionParti)
			if res:
				logging.warning("res : " + str(res)+ " " + str(type(res)))
				logging.warning("Selection abbrege : " + str(res.group(1))+ " " + str(type(res.group(1))))
				self.label1.config(text=res.group(1))
			else:
				logging.warning("Recherche infructueuse")
		
		
	def onListRegions_click(self, event):
		"Traitement de la sélection de la région"
		index = self.list_regions.curselection()
		if index != ():
			logging.warning("Liste des valeurs : " + str(self.listRegions))
			logging.warning("Index : " + str(index)+ " " + str(type(index)))
			for ind in index:
				logging.warning("ind : " + str(ind) + " " + str(type(ind)))
				self.selectionRegion = self.listRegions[ind]
			logging.warning("Selection : " + str(self.selectionRegion)+ " " + str(type(self.selectionRegion)))
			self.label2.config(text=self.selectionRegion)
		
	def onListDeparts_click(self, event):
		"Traitement de la sélection de la région"
		index = self.list_departs.curselection()
		if index != ():
			logging.warning("Liste des valeurs : " + str(self.listDeparts))
			logging.warning("Index : " + str(index)+ " " + str(type(index)))
			for ind in index:
				logging.warning("ind : " + str(ind) + " " + str(type(ind)))
				self.selectionDepart = self.listDeparts[ind]
			logging.warning("Selection : " + str(self.selectionDepart)+ " " + str(type(self.selectionDepart)))
			self.label2.config(text=self.selectionDepart)
				
	def regionRadioButton_click(self):
		logging.warning("Selection d'une region")
		self.list_regions.configure(state='normal')
		self.list_departs.configure(state='disabled')

	def departRadioButton_click(self):
		logging.warning("Selection d'un département")
		self.list_regions.configure(state='disabled')
		self.list_departs.configure(state='normal')
	
	def globalSelectionReset_click(self):
		logging.warning("Reset")
		logging.warning("Ligne : "+str(self.ligne)+" Colonne : "+str(self.colonne))
		colnd = str(self.ligne-1)+'.'+str(self.colonne)
		logging.warning('1.1 to '+ colnd)
		self.ed_txt.delete('1.0',colnd)
		self.boutonOK.configure(state='normal')
			
	def globalReload_click(self):
		if askokcancel("Recharger les données depuis Internet", "Cette requête prend quelques minutes"):
			self.assemb.closeBdd()
			#1.Suppression des fichiers locaux
			os.remove(bddName)
			os.remove(regionsName)
			os.remove(departementsName)
			os.remove(partisName)
			#2.Désactivation de l'interface GUI
#			self.globalSelectionReset_click()
			self.list_partis.configure(state='disabled')
			self.list_regions.configure(state='disabled')
			self.list_departs.configure(state='disabled')
			self.regionButton.configure(state='disabled')
			self.departButton.configure(state='disabled')
			self.boutonOK.configure(state='disabled')
#			self.boutonReset.configure(state='disabled')
			self.boutonReload.configure(state='disabled')
			#3.Rechargement des données
			self.assemb = AssembleNationale()
			#4.Rechargement des listes de l'interface
			i=1
			for parti in self.assemb.getPartis():
				logging.warning('parti : '+ parti)
				self.listPartis.append(parti)
				self.list_partis.insert(i, parti)
				i = i+1
		
			i=1
			for region in self.assemb.getRegions():
				logging.warning('region : '+ region)
				self.listRegions.append(region)
				self.list_regions.insert(i, region)
				i = i+1
			
			i=1
			for depart in self.assemb.getDepartements():
				logging.warning('departement : '+ depart)
				self.listDeparts.append(depart)
				self.list_departs.insert(i, depart)
				i = i+1
			#5.Réactivation de l'interface GUI
			self.list_partis.configure(state='normal')
			self.regionButton.configure(state='normal')
			self.departButton.configure(state='normal')
			self.boutonOK.configure(state='normal')
#			self.boutonReset.configure(state='normal')
			self.boutonReload.configure(state='normal')
	
	def globalSelection_click(self):
		"Traitement global de la sélection"
		logging.warning("Calcul de la selection : radioButtonValue = " + str(self.radioButtonValue.get()))
		logging.warning("selectionParti = " + self.selectionParti)
		logging.warning("selectionRegion = " + self.selectionRegion)
		logging.warning("selectionDepart = " + self.selectionDepart)
		
		self.globalSelectionReset_click()
		
		if self.selectionParti == 'Tous les partis("Tous les partis")':
			#Pas de sélection sur le parti
			if self.radioButtonValue.get() == 'depart':
				#Pas de sélection sur la région
				if self.selectionDepart=="Tous les départements":
					#Pas de sélection sur le département
					logging.warning("branch1")
					row=self.assemb.getSelectionAll()
				else:
					#Sélection sur le département
					logging.warning("branch2")
					row=self.assemb.getSelectionDepartement(self.selectionDepart)
			elif self.radioButtonValue.get() == 'region':
				# Sélection sur la région
				if self.selectionRegion=="Toutes les regions":
					# Toutes régions
					logging.warning("branch3")
					row=self.assemb.getSelectionAll()
				else:
					#Sélection sur la région	
					logging.warning("branch4")
					row=self.assemb.getSelectionRegion(self.selectionRegion)
			else:
				#Pas de sélection ni sur le département, ni sur la région
				logging.warning("branch5")
				row=self.assemb.getSelectionAll()
		else:
			#Sélection sur le parti
			regex=re.compile('\(".*"\)')
			self.selectionParti = regex.sub('',self.selectionParti)
			if self.radioButtonValue.get() == 'depart':
				#Pas de sélection sur la région
				if self.selectionDepart=="Tous les départements":
					logging.warning("branch6")
					row=self.assemb.getSelectionParti(self.selectionParti)
				else:
					logging.warning("branch7")
					row=self.assemb.getSelection(self.selectionParti, self.selectionDepart, 'depart')
			elif self.radioButtonValue.get() == 'region':
				# Sélection sur la région
				if self.selectionRegion=="Toutes les regions":
					logging.warning("branch8")
					row=self.assemb.getSelectionParti(self.selectionParti)
				else:
					logging.warning("branch9")
					row=self.assemb.getSelection(self.selectionParti, self.selectionRegion, 'region')
			else:
				logging.warning("branch10")
				row=self.assemb.getSelectionParti(self.selectionParti)
			
		email = str(row)
		logging.warning(email+str(type(email))) 
		self.ligne = 1
		for email in row:
			coord = str(self.ligne) + ".1"
			logging.warning("coord : " + coord)
			self.ligne=self.ligne+1
			self.ed_txt.insert(coord, email[0]+";\n")	
		self.colonne = len(email[0])+2
		
#		self.boutonOK.configure(state='disabled')

		showinfo("Selection email", "Sélectionner les adresses qui vous interessent avec la souris,\npuis, utiliser le raccourci CTRL-c pour copier dans le presse papier,\n puis CTRL-v pour le coller ailleurs. ")
			
if __name__ == "__main__":

	logging.basicConfig(filename='trace.log',filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

	app = Accueil_tk(None)
