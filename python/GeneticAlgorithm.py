from Population import Population
from Route import Route
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image as mpimpg
import os
class GeneticAlgorithm:
    ######################################
    #!########## Constructeur ############
    ######################################       
    # Initialisation des paramètres de l'algo
    def __init__(self, mutation_rate, population_size, city_list, nb_iterations):
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.city_list = city_list
        self.nb_cities = len(city_list)
        self.nb_iterations = nb_iterations
        # Chemin d'accès à l'image, selon l'OS
        if os.name == "nt" : # Windows
            path = "data\\map.jpg"
        else : # Unix
            path = "data/map.jpg"
        self.map_France = mpimpg.imread(path)

        # Extraction des attributs des villes
        self.names = [city.name for city in city_list]
        self.x = [city.x for city in city_list]
        self.y = [city.y for city in city_list]

    #####################################
    #!###### Traçage des chemins ########
    #####################################
    def drawBestRoutes(self, population, nb_routes):
        # Initialisation des variables
        x = self.x
        y = self.y
        names = self.names
        colors = ['pink','purple','green','blue','red']

        # On ne peut pas sélectionner plus de routes qu'il n'y en a dans la pop
        nb_routes = min(nb_routes, len(population.routes))
        # 5 est notre nombre de routes maximal à afficher
        nb_routes = min(nb_routes, 5)

        # On efface les routes précédentes
        plt.cla()

        # On affiche la carte et les villes
        plt.imshow(self.map_France)
        plt.scatter(self.x, self.y, c='red', marker='.')
        for i, name in enumerate(self.names):
            plt.text(x[i]+5, y[i]+5, name, size = 'xx-small')
        
        # On trace les chemins
        for i in range(nb_routes) : 
            villes = population.routes[i].cities
            for j in range(len(villes) - 1):
                plt.plot([villes[j].x, villes[j+1].x], [villes[j].y, villes[j+1].y], color = colors[i])

        #? Garde le graphique ouvert lors de l'exécution du code
        plt.show(block = False)    
        plt.pause(0.5) #Nombre de secondes d'affichage

    ##############################################################
    #!########## Génération d'une population initiale ############
    ##############################################################
    # Renvoie une population 
    def init_population(self):
        #? Ordre aléatoire, mais la première ville doit également être la dernière du chemin
        # Initialisation 
        indexes = list((range(1,self.nb_cities)))
        population = [None] * (self.population_size)
        city_list = self.city_list

        for i in range(self.population_size):
            orderedList = [None] * (self.nb_cities+1)
            # On change l'ordre de remplissage
            random.shuffle(indexes)
            # Pour remplir un parent aléatoire
            for j in range(1,self.nb_cities) :
                orderedList[j] = city_list[indexes[j-1]]
            # La première et la dernière ville sont fixées
            orderedList[0] = city_list[0]
            orderedList[-1] = city_list[0]
            newRoute = Route(i, orderedList)
            # On ajoute ce parent à la population
            population[i] = newRoute
        # On renvoie un tableau de n parents néo-formés
        return Population(city_list = city_list, routes = population)

    ###################################
    #!########## Crossover ############
    ###################################
    # Prend 2 parents, et renvoie deux Route enfants, qui correspondent aux parents avec des segments échangés
    def crossOverDeLaMortQuiTue(self, parent1, parent2):
        nb_cities = self.nb_cities
        start, end = sorted(random.sample(range(1, nb_cities), 2))
        p1, p2 = parent1.cities, parent2.cities # p = parent

        # On définit les segments à échanger :
        l1, l2 = p1[start:end+1], p2[start:end+1] # l = liste (je sais pas trop pourquoi mais c'était plus intuitif)
        # On fait des listes contenants les valeurs propres à un seul segment
        # Pour chaque élément de l1, qui n'est pas dans l2, on le met dans u1, et vice versa pour u2
        u1, u2 = [e for e in l1 if e not in l2], [e for e in l2 if e not in l1] # u = unique

        # On initialise les enfants, vides
        c1, c2 = [None] * (nb_cities+1), [None] * (nb_cities+1) # c = child
        # On copie les segments dans les enfants :
        c1[start:end+1] = l2 
        c2[start:end+1] = l1

        # On définit la première et la dernière ville
        for c in [c1, c2]:
             c[0] = c[-1] = self.city_list[0]

        # On remplit le reste des villes, sans toucher à la première et dernière ville
        def fill(c, p, u) :
            idx = 1
            for e in p: # Pour chaque élément du parent 
                if e not in u and e not in c: # Si il n'est pas dans la séquence unique à échanger, et qu'il n'est pas déjà ajouté
                    while c[idx] is not None and idx < nb_cities : # On parcourt l'enfant pour trouver un None 
                        idx += 1
                    c[idx] = e # On ajoute l'élément 
        fill(c1, p1, u2)
        fill(c2, p2, u1)
        
        return Route("Child 1", c1), Route("Child 2", c2)

    ###############################################
    #!########## Fonctions de mutation ############
    ###############################################
    def mutate(self, population):
        for i in range(len(population.routes)): 
            for j in range(1, self.nb_cities - 1) :  
                if random.random() < self.mutation_rate:
                    x = random.randint(0, 2)
                    if x == 0 :
                        population.routes[j] = self.fullReverse(population=population, position = j)
                    elif x == 1 :
                        population.routes[j] = self.partReverse(population=population, position = j)
                    elif x == 2 :
                        population.routes[j] = self.moveTwo(population=population, position=j)
                    #TODO : Rajouter d'autres types de mutations 
        return population

    # Mutation qui inverse l'ordre de toutes les villes
    def fullReverse(self, population, position):
        cities = population.routes[position].cities
        # Slicing pour obtenir la liste inversée
        return Route(name = population.routes[position].name, cities=cities[::-1])

    # Mutation qui inverse l'ordre de deux villes adjacentes
    def partReverse(self, population, position):
        cities = population.routes[position].cities
        # Définition de la position de la mutation
        x = random.randint(2, self.nb_cities)
        #Vérification supplémentaire qu'on ne bouge pas la ville de départ
        while cities[x].name == "Paris" or cities[x-1].name == "Paris" :
            x = random.randint(2, self.nb_cities)  
        # Affichage de la modification
        print("Inverted " + cities[x].name + " and " + cities[x-1].name)
        # Déballage de tuple pour échanger les positions  
        cities[x], cities[x - 1] = cities[x - 1], cities[x]
        return Route(name=population.routes[position].name, cities=cities)

    # Mutation qui interchange les positions de deux villes
    def moveTwo(self, population, position) :
        cities = population.routes[position].cities
        nb_cities = len(cities) - 1
        # Définition des positions à échanger mutation
        pos1, pos2 = random.randint(1, nb_cities), random.randint(1, nb_cities)
        # Vérification supplémentaire qu'on ne bouge pas la ville de départ, et que les positions 1 et 2 sont !=
        while cities[pos1].name == "Paris" :
            pos1 = random.randint(1, nb_cities) 
        while pos1 == pos2 or cities[pos2].name == "Paris" :
            pos2 = random.randint(1, nb_cities)
        # Affichage de la modification
        print("Moved " + cities[pos1].name + " and " + cities[pos2].name)
        # Déballage de tuple pour échanger les positions  
        cities[pos1], cities[pos2] = cities[pos2], cities[pos1]
        return Route(name=population.routes[position].name, cities=cities)

    ####################################
    #!########## Itérations ############
    ####################################
    def iterate(self, pop) :
        pop_size = self.population_size
        # Pour chaque génération : 
        for i in range(self.nb_iterations) :
            # On sélectionne les 50% meilleures Routes de la population précédente
            newPopRoutes = pop.selectFittest(int(pop_size/2)).routes
            # On choisit des positions aléatoires, correspondant aux parents, qu'on met dans deux listes
            x, y = random.sample(range(pop_size), int(pop_size/2)), random.sample(range(pop_size), int(pop_size/2))
            # On fait des cross-overs
            for j in range(int(pop_size/2)):
                e1, e2 = self.crossOverDeLaMortQuiTue(pop.routes[x[j]], pop.routes[y[j]])
                newPopRoutes.append(e1)
                newPopRoutes.append(e2)
            newPop = Population(newPopRoutes, city_list=self.city_list)
            print("-------------------------------------------\nItération n°" + str(i) +"\n\nMutations :\n")
            newPop = self.mutate(newPop)
            print("\n############################################\n\n2 Meilleurs enfants :\n")
            pop = newPop.selectFittest(pop_size)
            # Afficher les 2 meilleures nouvelles routes
            Population(pop.routes, self.city_list).selectFittest(2).printPopulation()
            self.drawBestRoutes(pop,1)
