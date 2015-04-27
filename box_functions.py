#!/usr/bin/python

#@author: Jerome PIVERT
#@date: 6/10/2014 - 14/11/2014

#@resume: box related functions
#@func getRandomObjects(nbObjects, valMin, valMax): generating random dict
#@func getOptimalAverageBoxSize(objectDictionnary, numberOfBoxes): compute optimal average box size
#@func getBoxSize(objectsBox, objectsDictionnary): get size of one box
#@func getBiggestBoxSize(listOfBoxes, objectsDictionnary): get the biggest box in a list of boxes
#@func getSmallestBoxSize(listOfBoxes, objectsDictionnary): get the smallest box in a list of boxes
#@func getNumberOfBoxesAboveThreshold(listOfBoxes, sizeThreshold, objectsDictionnary): cf poly
#@func computeSizeThreshold(listOfBoxes,percentage, objectsDictionnary): cf poly
#@func getCumulatedError(listOfBoxes, objectsDictionnary): get cumulated error from a list of boxes

#General imports
import string
import os, sys
import numpy as np

#Other imports
import classes

#Creation d'un dictionnaire aleatoire de taille definie
#@return: <dict> dic
def getRandomObjects(nbObjects, valMin, valMax):
	dic = dict()
	
	for i in range(nbObjects):
		dic[i+1] = np.random.uniform(valMin, valMax+1.0)
				
	return dic


#Calculer la taille moyenne optimale d'une boite
#@return: <float>
def getOptimalAverageBoxSize(objectDictionnary, numberOfBoxes):
	return (sum(objectDictionnary.values())/float(numberOfBoxes))


#Retourner la taille d'une boite (la somme des tailles des objets dans cette boite)
#@return: <float> box_size
def getBoxSize(objectsBox, objectsDictionnary):
	box_size = 0
	for i in objectsBox:
		box_size = box_size + objectsDictionnary[i]
	return box_size


#Depuis une liste de boites, retourner la taille de la plus grande boite
#@return: <float> max_size
def getBiggestBoxSize(listOfBoxes, objectsDictionnary):
	max_size = 0
	for i in listOfBoxes:
		tmp_size = getBoxSize(i, objectsDictionnary)
		max_size = tmp_size if 	tmp_size > max_size else max_size
	return max_size


#Depuis une liste de boites, retourner la taille de la plus petite boite
#@return: <float> min_size
def getSmallestBoxSize(listOfBoxes, objectsDictionnary):
	min_size = 0
	for i in listOfBoxes:
		tmp_size = getBoxSize(i, objectsDictionnary)
		min_size = tmp_size if 	tmp_size < min_size else min_size
	return min_size


#Retourne le nombres de boites ayant une taille strictement superieure a une taille voulue
#@return: <int> box_number
def getNumberOfBoxesAboveThreshold(listOfBoxes, sizeThreshold, objectsDictionnary):
	box_number = 0
	for i in listOfBoxes:
		#box_number+=1 if getBoxSize(i, objectsDictionnary) > sizeThreshold else pass
		if(getBoxSize(i, objectsDictionnary) > sizeThreshold):
			box_number+=1
		else:
			pass
	return box_number
	

#Depuis une liste de boites, huuuuuu ca ressemble aux quantiles
#@return: <float> listOfSizes[counter-1]
def computeSizeThreshold(listOfBoxes,percentage, objectsDictionnary):
	listOfSizes = list()
	counter = 0
	for i in listOfBoxes:
		listOfSizes.append(getBoxSize(i, objectsDictionnary))
	listOfSizes.sort();# listOfSizes[::-1]
	
	for i in listOfSizes:
		#i if i < np.percentile(listOfSizes, percentage) else return listOfSizes[i-1]
		if (i >= np.percentile(listOfSizes, percentage)):
			return listOfSizes[counter-1]
		counter+=1
		

#Renvoie la somme des differences absolues entre taille reelle et taille optimale
#@return: <float> sum_diff
def getCumulatedError(listOfBoxes, objectsDictionnary):
	sum_diff = 0
	optimal_size_box = getOptimalAverageBoxSize(objectsDictionnary, len(listOfBoxes))
	for i in listOfBoxes:
		sum_diff = sum_diff + abs((getBoxSize(i, objectsDictionnary) - optimal_size_box))
		
	return sum_diff
