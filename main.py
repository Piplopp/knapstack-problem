#!/usr/bin/python

#@author: Jerome PIVERT
#@date: 6/10/2014 - 01/12/2014

#Argparse
import argparse

parser=argparse.ArgumentParser(usage='./%(prog)s [-h] [-i/--infile INFILE] [-o/--output OUTFILE] [-e/--export_raw]', description='Comparaison de differentes strategies pour le probleme du sac a dos')

parser.add_argument('-o', '--outfile',
	help = 'specifier un fichier sortie', 
	dest='outfilename', 
	required=False,
	default=None,
	type=argparse.FileType('w')
)
parser.add_argument('-i', '--infile',
	help = 'specifier un fichier en entree',
	dest='infilename',
	required=False,
	default=None,
	type=argparse.FileType('r')
)
parser.add_argument('--export_raw', '-e',
	help = 'exporter les donnees brutes dans un fichier texte raw.txt, pas disponible pour les tests',
	required=False,
	default=False,
	action='store_true'
)
args=parser.parse_args()



#@resume: main functions for executing the programm, plus 3 basic test functions
#@func main()
#@func final_print(meanStratsData, outfile, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor)
#@func test_strat_by_strat()
#@func test_dico_ent()
#@func test_dico_random()




#General imports
import string
import os, sys
import math
import time

#Strategy imports
import strategies

#Other imports
import classes
import others
import box_functions
	

def main():
	#Initialisation des valeurs
	nbObjects=int(math.pow(4,7))
	smallestAllowedItem=1	#objets iront de 1
	objectsSizeFactor=1000  #a 1000 dans ce cas
	nbBoxes=400
	percentage=90 #seuil de 90%

	os.system('clear')
	
	
	#Avec ou sans fichier en entree ?
	if args.infilename != None: #si fichier en entree donne on bosse dessus
		os.system('clear')
		print classes.bcolors.OKBLUE + 'Infile : ' + classes.bcolors.ENDC + args.infilename.name
		
		
		StratsData = others.run_stats_n_times(500, nbBoxes, nbObjects, smallestAllowedItem, objectsSizeFactor, percentage, args.infilename.name) #run n times
		args.infilename.close()
		meanStratsData=others.stats_mean(StratsData) #do the maths		
		final_print(meanStratsData, args.outfilename, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor)
		

	else: #sinon sur des dicos random
		StratsData = others.run_stats_n_times(500, nbBoxes, nbObjects, smallestAllowedItem, objectsSizeFactor, percentage, "") #run n times
		meanStratsData=others.stats_mean(StratsData) #do the maths
		final_print(meanStratsData, args.outfilename, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor)
		


	#Exporter les donnees si l'option est specifiee
	if args.export_raw:
		others.export_raw_data(StratsData) #export raw data
	else:
		pass
	
	
	#Effectuer les boxplots
	others.display_boxplot(StratsData) #do boxplots









#@resume: YOU SHALL NOT PRINT IN A FILE ! or maybe yes... depending on arguments
def final_print(meanStratsData, outfile, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor):
	if outfile != None: #Si fichier sortie specifie
		others.create_stats_report(meanStratsData, outfile.name, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor) #on print dans un fichier
		outfile.close() #we dont need you anymore..
		print classes.bcolors.OKBLUE + 'Outfile	: ' + classes.bcolors.ENDC + outfile.name
	else: #sinon console
		others.print_on_term(meanStratsData, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor)






#@resume: fonction pour tester les strategies une a une avec un retour direct dans la console
#possibilite d'utiliser soit le dictionnaire de l'ENT soit un random soit un dico tres simple manuel
def test_strat_by_strat():
	#Initialisation des valeurs
	nbObjects=int(math.pow(4,7))
	smallestAllowedItem=1	#objets iront de 1
	objectsSizeFactor=1000  #a 1000 dans ce cas
	nbBoxes=400
	percentage=90 #seuil de 90%

	#Dictionnaire de l'ENT
	random_dict=others.readObjectsFromFiles("listeObjetsControle.txt")


	#Tests generaux sur petits jeux de donnees manuels (pas oublier de changer nbBoxes)
#	random_dict = {'first':1, 'second':2, 'third':3, 'fourth':4, 'fifth':5, 'sixth':6, 'seventh':7, 'zero':0, 'zerobis':0}



	#Tests generaux sur dictionnaire genere aleatoirement
#	random_dict = box_functions.getRandomObjects(nbObjects, 1, 1*objectsSizeFactor)


	tic = time.time()
	#Strategie 1
#	random_box_list = strategies.fillBoxesStrategy1(random_dict, nbBoxes)
	#Strategie 2
#	random_box_list = strategies.fillBoxesStrategy2(random_dict, nbBoxes)
	#Strategie 3
#	random_box_list = strategies.fillBoxesStrategy3(random_dict, nbBoxes)
	#Strategie 3 bis
#	random_box_list = strategies.fillBoxesStrategy3_bis(random_dict, nbBoxes)
	#Strategie 4
	random_box_list = strategies.fillBoxesStrategy4(random_dict, nbBoxes)
	#Strategie 5
#	random_box_list = strategies.fillBoxesStrategy5(random_dict, nbBoxes)
	#Strategie 5 bis
#	random_box_list = strategies.fillBoxesStrategy5_bis(random_dict, nbBoxes)
	tac = time.time()
	
	
	elapsed_time = tac - tic
	print classes.bcolors.WARNING + "Elapsed time: " + classes.bcolors.ENDC + str(elapsed_time)
	others.run_stats(random_box_list, random_dict, 90, True) #seuil 90%



#@resume: tester les 5 strategies sur le dictionnaire de l'ENT ainsi que les fonctions de stats, envoie la puree dans
#un fichier sortie
def test_dico_ent():
	#Initialisation des valeurs
	nbObjects=int(math.pow(4,7))
	smallestAllowedItem=1	#objets iront de 1
	objectsSizeFactor=1000  #a 1000 dans ce cas
	nbBoxes=400
	percentage=90 #seuil de 90%

	#Dictionnaire de l'ENT
	tic = time.time()

	StratsData = others.run_stats_n_times(20, nbBoxes, nbObjects, smallestAllowedItem, objectsSizeFactor, percentage, "tests/listeObjetsControle.txt") #run n times
	meanStratsData=others.stats_mean(StratsData) #do the maths
	others.create_stats_report(meanStratsData, 'report_all_strats_FICHIER_ENT.txt', nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor) #black magic for creating a report
	
	tac = time.time()		
	elapsed_time = tac - tic
	print classes.bcolors.WARNING + "Elapsed time: " + classes.bcolors.ENDC + str(elapsed_time)




#@resume: idem que fonction precedente mais pour un dictionnaire random
def test_dico_random():
	#Initialisation des valeurs
	nbObjects=int(math.pow(4,7))
	smallestAllowedItem=1	#objets iront de 1
	objectsSizeFactor=1000  #a 1000 dans ce cas
	nbBoxes=400
	percentage=90 #seuil de 90%

	
	#Sur un dictionnaire random
	tic = time.time()
	StratsData = others.run_stats_n_times(500, nbBoxes, nbObjects, smallestAllowedItem, objectsSizeFactor, percentage, "") #run n times
	meanStratsData=others.stats_mean(StratsData) #do the maths
	others.create_stats_report(meanStratsData, 'report_all_strats_DICO_RANDOM.txt', nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor) #black magic for creating a report

	tac = time.time()		
	elapsed_time = tac - tic
	print classes.bcolors.WARNING + "Elapsed time: " + classes.bcolors.ENDC + str(elapsed_time)




main()

#Tests:
#test_strat_by_strat()
#test_dico_ent()
#test_dico_random()	

