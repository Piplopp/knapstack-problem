#!/usr/bin/python

#@author: Jerome PIVERT
#@date: 6/10/2014 - 01/12/2014

#@resume: other functions
#@func readObjectsFromFiles(filePath): create dict from file
#@func shuffle(listToShuffle): shuffle a list
#@func run_stats(listOfBoxes, objectsDictionnary, percentage): run simple stats for one strategy
#@func run_stats_n_times(nbIter, nbBoxes, nbObjects, objectsSizeFactor, percentage, fromFile): run stats n times
#@func stats_mean(listOfStratsData): mean of all stats on all strats
#@func create_stats_report(dictOfStats, outfile, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor): print a short report in a file
#@func create_boxplot(data, xlabel, graphTitle, filename): create a boxplot
#@func export_raw_data(data): export data from list in a file

#General imports
import string
import os, sys
import random
import time
import numpy as np
from collections import defaultdict
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


#Other imports
import classes
import box_functions
import strategies


#@resume: create dict from 2-col-file passed in argument; first col will be interpreted as the key and the second as the value
#@return <dict>
def readObjectsFromFiles(filePath):
	dic = dict()

	with open(filePath, 'r') as f:
		for line in f:
			key, val = line.strip().split()
			dic[int(key)] = int(val)
	return dic



#@resume: shuffle a list passed in argument (use of import random)
#@return <list>
def shuffle(listToShuffle):
	random.shuffle(listToShuffle)
	return listToShuffle



#@resume: run simple stats for one strategy and print the result on terminal or return them;
#@args listOfBoxes <list>: must be a list of list
#@args objectsDictionnary <dict>: values have to be numbers
#@args percentage <int>: between 0 and 100
#@args terminal <bool>: False for returning the values or True for printing in console
#@return <list>
def run_stats(listOfBoxes, objectsDictionnary, percentage, terminal):

	nbObjects = len(objectsDictionnary)
	biggestBox = box_functions.getBiggestBoxSize(listOfBoxes, objectsDictionnary)
	sizeThreshold = box_functions.getOptimalAverageBoxSize(objectsDictionnary, len(listOfBoxes))
	nbBoxOpti = box_functions.getNumberOfBoxesAboveThreshold(listOfBoxes, sizeThreshold, objectsDictionnary)
	size_seuil = box_functions.computeSizeThreshold(listOfBoxes,percentage, objectsDictionnary)
	cumul_err = box_functions.getCumulatedError(listOfBoxes, objectsDictionnary)
	average_err = cumul_err/len(listOfBoxes)
	
	if terminal == True:
		print classes.bcolors.HEADER + "Objects number: " + classes.bcolors.ENDC + "%d" %(nbObjects)
		print classes.bcolors.HEADER + "Average optimal box size: " + classes.bcolors.ENDC + "%.3f" %(sizeThreshold)
		print classes.bcolors.HEADER + "Biggest box size: " + classes.bcolors.ENDC + "%.3f" %(biggestBox)
		print classes.bcolors.HEADER + "Nb boxes > optimal: " + classes.bcolors.ENDC + "%.3f" %(nbBoxOpti)
		print classes.bcolors.HEADER + "Size > ", percentage, "% boxes: " + classes.bcolors.ENDC + "%.3f" %(size_seuil)
		print classes.bcolors.HEADER + "Cumulated error: " + classes.bcolors.ENDC + "%.3f" %(cumul_err)
		print classes.bcolors.HEADER + "Average error: " + classes.bcolors.ENDC + "%.3f" %(average_err)
	else:
		return [sizeThreshold, biggestBox, nbBoxOpti, size_seuil, cumul_err, average_err]
	


#@resume: run stats for all 5 main strategies and 2 "bis" strategies and return a list of strat datas
#@args nbIter <int>: how many times we do this magical thing ?
#@args nbBoxes <int>: how many boxes ? (for strategies)
#@args nbObjects <int>: how many items in a dict ?
#@args smallestAllowedItem <int>: smallest value allowed in dict
#@args objectsSizeFactor <int>: ratio between the largest and the smallest value in dict
#@args percentage <int>: between 0-100
# data structure: 
# stratn:[
#		[ average optimal box size ],
#		[ biggest box size ],
#		[ nb boxes > optimal ],
#		[ size > x% boxes ],
#		[ cumulated error ],
#		[ average error ],
#		[ comput. time (s) ]
#	 ]

def run_stats_n_times(nbIter, nbBoxes, nbObjects, smallestAllowedItem, objectsSizeFactor, percentage, fromFile):
	f=0 #not files yet
	strat1=[[] for i in range(7)] #7 different stats to store
	strat2=[[] for i in range(7)]
	strat3=[[] for i in range(7)]
	strat3_bis=[[] for i in range(7)]
	strat4=[[] for i in range(7)]
	strat5=[[] for i in range(7)]
	strat5_bis=[[] for i in range(7)]

	for i in range(nbIter):
		#Dict creation
		if fromFile and f==0:
			random_dict = readObjectsFromFiles(fromFile)
			f=1 #file is read now
		elif f==0:
			random_dict = box_functions.getRandomObjects(nbObjects, smallestAllowedItem, smallestAllowedItem*objectsSizeFactor)
		
		
		#Strategie 1
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy1(random_dict, nbBoxes)
		tac=time.time()
		strat1[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat1[j].append(tmp_stats[j])

		
		#Strategie 2
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy2(random_dict, nbBoxes)
		tac=time.time()
		strat2[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat2[j].append(tmp_stats[j])

		
		#Strategie 3
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy3(random_dict, nbBoxes)
		tac=time.time()
		strat3[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat3[j].append(tmp_stats[j])
			
		#Strategie 3 bis
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy3_bis(random_dict, nbBoxes)
		tac=time.time()
		strat3_bis[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat3_bis[j].append(tmp_stats[j])
			
		#Strategie 4
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy4(random_dict, nbBoxes)
		tac=time.time()
		strat4[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat4[j].append(tmp_stats[j])
		
		#Strategie 5
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy5(random_dict, nbBoxes)
		tac=time.time()
		strat5[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat5[j].append(tmp_stats[j])
		
		#Strategie 5 bis
		tic=time.time()
		random_box_list = strategies.fillBoxesStrategy5_bis(random_dict, nbBoxes)
		tac=time.time()
		strat5_bis[6].append(tac-tic)
		tmp_stats = run_stats(random_box_list, random_dict, 90, False)
		for j in range(6):
			strat5_bis[j].append(tmp_stats[j])
		
		avancement=float(i+1)*100.0/float(nbIter)
		sys.stdout.write('\rcurrent progress on %d iteration: %.1f%%' %(nbIter,avancement)) #\r move the cursor at the beginning of the line
		sys.stdout.flush() #empty buffer

		
	print ""
	print classes.bcolors.OKGREEN + "All %d dict done" %(nbIter)
	return [strat1, strat2, strat3, strat3_bis, strat4, strat5, strat5_bis]



#@resume: compute and return mean of all stats on all strats
#@args listOfStratsData <list>: list of list of list of numbers
#@return <dict>: key = strat and value = list of stats
def stats_mean(listOfStratsData):
	i=1 #number of strat
	dictOfStats=defaultdict(list)
	for strat in listOfStratsData: #for each strat
		for statistic in strat: #for each statistic
			dictOfStats[i].append(sum(statistic)/float(len(statistic)))
		i+=1
	return dictOfStats
	


#@resume: print in file the differents stats for each strategies and some basic informations about params
#N.B. PENSER A FAIRE GAFFE A CAUSE DES STATS n_bis LES NUMEROS SONT PAS LES MEMES QUE LE POLY
def create_stats_report(dictOfStats, outfile, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor):
	i=1 #number of strat
	with open(outfile, 'w') as out:
		out.write('General informations:\n')
		out.write('Nb objects in dict:\t %d\n' %(nbObjects))
		out.write('Nb boxes:\t %d\n' %(nbBoxes))
		out.write('Pourcentage (pour les boites au dessus du seuil):\t %d\n' %(percentage))
		out.write('Les objets vont de %d a %d\n' %(smallestAllowedItem, smallestAllowedItem*objectsSizeFactor))
		out.write('##############################################################################\n')
		for strat in dictOfStats: #each strats
			out.write('Strategie %d:\n' %(strat))
			out.write('Average optimal box size:\t %.2f\n' %(dictOfStats[strat][0]))
			out.write('Biggest box size:\t %.2f\n' %(dictOfStats[strat][1]))
			out.write('Nb boxes > optimal:\t %.2f\n' %(dictOfStats[strat][2]))
			out.write('size > %d %% boxes:\t %.2f\n' %(percentage, dictOfStats[strat][3]))
			out.write('Cumulated error:\t %.2f\n' %(dictOfStats[strat][4]))
			out.write('Average error:\t %.2f\n' %(dictOfStats[strat][5]))
			out.write('Comput. time (s):\t %.2f\n' %(dictOfStats[strat][6]))
			out.write('\n')
			i+=1



def print_on_term(dictOfStats, nbObjects, nbBoxes, percentage, smallestAllowedItem, objectsSizeFactor):
	print classes.bcolors.HEADER + "General informations:"
	print "Nb objects in dict: " + classes.bcolors.ENDC + "%d" %(nbObjects)
	print classes.bcolors.HEADER + "Nb boxes: " + classes.bcolors.ENDC + "%d" %(nbBoxes)
	print classes.bcolors.HEADER + "Pourcentage (pour les boites au dessus du seuil): " + classes.bcolors.ENDC + "%d" %(percentage)
	print classes.bcolors.HEADER + "Les objets vont de " + classes.bcolors.ENDC + "%d a %d\n" %(smallestAllowedItem, smallestAllowedItem*objectsSizeFactor)
	
	for strat in dictOfStats: #each strat
		print classes.bcolors.OKGREEN + "Strategie %d:" %(strat)
		print classes.bcolors.ENDC + "Average optimal box size: %.2f" %(dictOfStats[strat][0])
		print "Biggest box size: %.2f" %(dictOfStats[strat][1])
		print "Nb boxes > optimal: %.3f" %(dictOfStats[strat][2])
		print "Size > %d%% boxes: %.3f" %(percentage, dictOfStats[strat][3])
		print "Cumulated error: %.3f" %(dictOfStats[strat][4])
		print "Average error: %.3f" %(dictOfStats[strat][5])
		print classes.bcolors.WARNING + "Comput. time (s): " + classes.bcolors.ENDC + "%.2f\n" %(dictOfStats[strat][6])


#@resume: create the boxplot with given args, cannot append new data on an existing plot (due to fig.clear) in a file
def create_boxplot(data, xlabel, graphTitle, filename):
	# Create a figure instance
	fig = plt.figure(1, figsize=(9, 6))
	fig.clear() #clear graph (if not --> append the new graph)
	# Create an axes instance
	ax = fig.add_subplot(111)
	# Create the boxplot
	bp = ax.boxplot(data)
	ax.set_xticklabels(xlabel)
	# Remove top axes and right axes ticks 
	# Custom x-axis labels
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	ax.set_title(graphTitle)
	
	# Save the figure
	fig.savefig(filename)

#@resume: creating_all_boxplots from the dataset
#@data <list>
def display_boxplot(data):
	labels=['Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 3 bis', 'Strategy 4', 'Strategy 5', 'Strategy 5 bis']
	#Biggest box size
	compute_time=[data[0][1], data[1][1], data[2][1], data[3][1], data[4][1], data[5][1], data[6][1]]
	create_boxplot(compute_time, labels, 'Biggest box size', 'biggest_box_size.png')
	#Nb boxes > optimal
	compute_time=[data[0][2], data[1][2], data[2][2], data[3][2], data[4][2], data[5][2], data[6][2]]
	create_boxplot(compute_time, labels, 'Nb boxes > optimal', 'nbBoxes_over_opti.png')
	#Size > 90% boxes
	compute_time=[data[0][3], data[1][3], data[2][3], data[3][3], data[4][3], data[5][3], data[6][3]]
	create_boxplot(compute_time, labels, 'Size > 90% boxes', 'size_over_90.png')
	#Cumulated error
	compute_time=[data[0][4], data[1][4], data[2][4], data[3][4], data[4][4], data[5][4], data[6][4]]
	create_boxplot(compute_time, labels, 'cumulated error', 'cumul_err.png')
	#Average error
	compute_time=[data[0][5], data[1][5], data[2][5], data[3][5], data[4][5], data[5][5], data[6][5]]
	create_boxplot(compute_time, labels, 'Average error', 'average_err.png')
	#Compute time
	compute_time=[data[0][6], data[1][6], data[2][6], data[3][6], data[4][6], data[5][6], data[6][6]]
	create_boxplot(compute_time, labels, 'compute time (s)', 'compute_time.png')
	


#@resume: print in file 'raw_data.txt' all data from the list
def export_raw_data(data):
	nb_datas=len(data[0][1]) #number of raw data for a specific stat (same for all stats)
	current_strat=1
	with open('raw_data.txt', 'w') as exp:
		exp.write('strategy\tavgOptiBoxSize\tbiggestBox\tboxOverOpti\tsiveOver\tcumulErr\tavgErr\telapsedTime\n')
		for strategy in data:
			current_iter=0 #set to 0, iteration parser for statistics
			while current_iter < nb_datas:
				exp.write('strat%d' %(current_strat)) #current strat
				for stat in strategy:
					exp.write('\t%f' %(stat[current_iter])) #print all stat from a specific iter
				exp.write('\n')
				current_iter+=1 #next iteration
			current_strat+=1 #next strat
