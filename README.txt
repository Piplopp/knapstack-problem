Jérome PIVERT - 02/12/2014

Python 2.7.3

Ce README contient également (en bas) les réponses à différentes questions
Ce programme permet de tester différentes stratégies pour résoudre le problème du sac à dos, il produit egalement des boxplots sur differentes statistiques de chaque strategies.
Il prend peut prendre en compte des arguments tels que des fichiers en entrée ou en sortie ou encore une option pour
exporter les données brutes vers un fichier.

Le fichier créé lors de l'export peut être utilisé pour effectuer des analyses plus poussées (sous R par exemple)

N.B. Les stratégies 3_bis et 5_bis sont de légères variantes (par curiosité) des stratégies 3 et 5
	la stratégie 3_bis va remplir de haut en bas puis de bas en haut puis de haut en bas etc..
	la stratégie 5_bis fait appel à la fonction getBoxSize() --> c'est plus lent en général
	

usage: ./main.py [-h] [-i/--infile INFILE] [-o/--output OUTFILE] [-e/--export_raw]
optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILENAME, --outfile OUTFILENAME
                        specifier un fichier sortie, n'affiche rien dans la console (sortie par defaut)
  -i INFILENAME, --infile INFILENAME
                        specifier un fichier en entree (ne fait pas de dico aleatoires)
  --export_raw, -e      exporter les donnees brutes dans un fichier texte raw.txt, pas disponible pour les tests



exemples:
	./main.py -i listeObjetsControle.txt -o resume_strats.txt
		execution du programme sur le fichier donne et les resultats sont retournes dans le fichier donne
	./main.py -e
		execution du programme sur la console et export des donnees brutes vers un fichier texte


Liste des fichiers:
	main.py			contient les principales fonctions du programme
	box_functions.py	fonctions liées aux boites
	others.py		diverses fonctions pour executer le prog, contient notamment les fonctions de stats
	strategies.py		toutes les strategies
	classes.py		COULEURS ! LE MONDE IL EST JOLI LE MONDE IL BÔ
	README.txt

	graphiques/		contient des graphiques fait sur 500 dicos aléatoires et servant d'exemples
	sorties_jerome/		contient différents fichier de sorties et de données brutes



####################
Réponse au questions:
####################

#Question 1:
Nombre de configurations possibles: combinaison de 16000 dans 400 --> trop grand pour être calculé

#Question 16:
Complexité des stratégies:
	avec n: nombre d'éléments dans le dictionnaire, en considérant O(1)
	stratégie 1: O(n)
	stratégie 2: O(n)
	stratégie 3: O(nlog(n)) a cause du tri, on peut negliger log(n) -> O(n)
	stratégie 3bis: idem strat 3
	stratégie 4: idem strat 3
	stratégie 5: idem strat 3
	stratégie 5bis: O(nlogn+n*k) k=nombre d'object dans une boite, négligeable --> O(nlog(n)) --> O(n)

