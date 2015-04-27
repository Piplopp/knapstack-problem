#!/usr/bin/python

#@author: Jerome PIVERT
#@date: 6/10/2014 - 01/12/2014

#@resume: all filling strategies (5+2)
#@func fillBoxesStrategy1(objectsDictionnary, nbBoxes): fill nbBoxes randomly with the keys of dict
#@func fillBoxesStrategy2(objectsDictionnary, nbBoxes): fill nboxes randomly with roughly weight-equal boxes
#@func fillBoxesStrategy3(objectsDictionnary, nbBoxes): sort (decreasing) by value and fill box by box, when reach end, restart at first box
#@func fillBoxesStrategy3_bis(objectsDictionnary, nbBoxes):same as strat3 but when reach end, continue to fill from the end of the list of boxes and going towards the first
#@func fillBoxesStrategy4(objectsDictionnary, nbBoxes):
#@func fillBoxesStrategy5(objectsDictionnary, nbBoxes):saturate a box before moving to the next, if all boxes are saturated -> add to the smallest; not using the getBoxSize function from box_functions
#@func fillBoxesStrategy5_bis(objectsDictionnary, nbBoxes): same as strat5 but using the getBoxSize function

#General imports
import string
import os, sys
import random
import numpy as np

#Other imports
import classes
import others
import box_functions

#@resume: first strategy, random filling in n boxes

def fillBoxesStrategy1(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)] #new list of nbBoxes empty lists
	for i in objectsDictionnary.keys():
		listOfBoxes[random.randint(0, nbBoxes - 1)].append(i)

	return listOfBoxes
	

#@resume: second strategy, random filling with roughly equal boxes

def fillBoxesStrategy2(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)]
	listOfValues = [0]*nbBoxes
	
	list_keys = objectsDictionnary.keys(); #list_keys.sort(); list_keys = list_keys[::-1]
	
	for i in list_keys:
		index_min=listOfValues.index(min(listOfValues)) #get index of min value (same for the keys)
		listOfBoxes[index_min].append(i)
		listOfValues[index_min]+=objectsDictionnary[i]
		
	return listOfBoxes


#@resume: third strategy, sorted filling

#fill: top to bot --> top to bot
def fillBoxesStrategy3(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)]
	ordered_list = sorted(objectsDictionnary, key=objectsDictionnary.__getitem__, reverse=True)
				#return list of keys sorted by their values
				
	cpt=0
	for i in ordered_list:
		if cpt >= nbBoxes:
			cpt=0
		listOfBoxes[cpt].append(i)
		cpt+=1
		
	return listOfBoxes

#fill: top to bot --> bot to top --> top to bot
def fillBoxesStrategy3_bis(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)]
	ordered_list = sorted(objectsDictionnary, key=objectsDictionnary.__getitem__, reverse=True)
	

	actual_pos=0 #position indicator, from 0 to nbBoxes and from nbBoxes to 0
	nb_iter=0 #global counter of iterations
	reverse=False
	for i in ordered_list:
		if reverse==True:
			listOfBoxes[actual_pos-1].append(i)
			actual_pos-=1
			if actual_pos<=0:
				reverse=False
		else:
			listOfBoxes[actual_pos].append(i)
			actual_pos+=1
			if actual_pos>nbBoxes-1:
				reverse=True
		nb_iter+=1
		if nb_iter==len(ordered_list):
			break #exit loop
	return listOfBoxes


#@resume: fourth strategy, similar to strat 2 but on an value-ordered list

def fillBoxesStrategy4(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)]
	listOfValues = [0]*nbBoxes
	
	list_keys = objectsDictionnary.keys(); 
	list_keys = sorted(objectsDictionnary, key=objectsDictionnary.__getitem__, reverse=True) #booya ! ordered 
	
	for i in list_keys:
		index_min=listOfValues.index(min(listOfValues)) #get index of min value (same for the keys)
		listOfBoxes[index_min].append(i)
		listOfValues[index_min]+=objectsDictionnary[i]
		
	return listOfBoxes


#@resume: fifth strategy, saturate a box before moving to the next, if all boxes are saturated -> add to the smallest
#N.B. If the highest value is > optimalAverageBoxSize it will consider the box (index 0) as a full box
#this can be resolved by forcing the first value in the first box before the for-loop and starting the for-loop at 1
#@version-1: without using the getBoxSize function

def fillBoxesStrategy5(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)]
	listOfSize = [0]*nbBoxes
	optimalAverageBoxSize = box_functions.getOptimalAverageBoxSize(objectsDictionnary, nbBoxes)
	
	list_keys = objectsDictionnary.keys(); 
	list_keys = sorted(objectsDictionnary, key=objectsDictionnary.__getitem__, reverse=True) #booya ! ordered 
	

	actualBox=0
	listOfBoxes[actualBox].append(list_keys[0])		
	listOfSize[actualBox]+=objectsDictionnary[list_keys[0]]
	for i in range(1,len(list_keys)): #i --> index of current key in dict.keys()
		if actualBox >= nbBoxes: #if all boxes are already filled and there is keys:values left
			index_min=listOfSize.index(min(listOfSize))
			listOfBoxes[index_min].append(list_keys[i])
			listOfSize[index_min]+=objectsDictionnary[list_keys[i]]
			continue

		elif (listOfSize[actualBox]+objectsDictionnary[list_keys[i]]) > optimalAverageBoxSize:
			actualBox+=1
			if actualBox==nbBoxes: #if we are over the last box, force store of current element
				index_min=listOfSize.index(min(listOfSize))
				listOfBoxes[index_min].append(list_keys[i])
				listOfSize[index_min]+=objectsDictionnary[list_keys[i]]	
				continue

		#fill the actual box; skipped if all boxes are saturated
		listOfBoxes[actualBox].append(list_keys[i])		
		listOfSize[actualBox]+=objectsDictionnary[list_keys[i]]

	return listOfBoxes


#@version-2: using the getBoxSize function

def fillBoxesStrategy5_bis(objectsDictionnary, nbBoxes):
	listOfBoxes = [[] for i in range(nbBoxes)]
	listOfSize = [0]*nbBoxes
	optimalAverageBoxSize = box_functions.getOptimalAverageBoxSize(objectsDictionnary, nbBoxes)
	
	list_keys = objectsDictionnary.keys(); 
	list_keys = sorted(objectsDictionnary, key=objectsDictionnary.__getitem__, reverse=True) #booya ! ordered 
	

	actualBox=0
	listOfBoxes[actualBox].append(list_keys[0])		
	listOfSize[actualBox]+=objectsDictionnary[list_keys[0]]
	for i in range(1,len(list_keys)): #i --> index of current key in dict.keys()
		if actualBox >= nbBoxes: #if all boxes are already filled and there is keys:values left
			index_min=listOfSize.index(min(listOfSize))
			listOfBoxes[index_min].append(list_keys[i])
			listOfSize[index_min]+=objectsDictionnary[list_keys[i]]
			continue

		elif (box_functions.getBoxSize(listOfBoxes[actualBox],objectsDictionnary)+objectsDictionnary[list_keys[i]]) > optimalAverageBoxSize:
			actualBox+=1
			if actualBox==nbBoxes: #if we are over the last box, force store of current element
				index_min=listOfSize.index(min(listOfSize))
				listOfBoxes[index_min].append(list_keys[i])
				listOfSize[index_min]+=objectsDictionnary[list_keys[i]]	
				continue

		#fill the actual box; skipped if all boxes are saturated
		listOfBoxes[actualBox].append(list_keys[i])		
		listOfSize[actualBox]+=objectsDictionnary[list_keys[i]]

	return listOfBoxes
