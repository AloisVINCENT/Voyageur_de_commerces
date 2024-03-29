from City import City
from Population import Population
from Route import Route
from GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt
from matplotlib import image as mpimpg
import numpy as np


################################################
# Binôme : Aloïs VINCENT et Jean REESE
# Implémentation d'un algorithme génétique pour résoudre le problème du voyageur de commerces
################################################

#####################################
#!###### Création des villes ########
#####################################

#?                    x   y    Nom
city_list = [City(290,180, "Paris"),
                City(390,420, "Marseille"),
                City(380,320, "Lyon"),
                City(250,410, "Toulouse"),
                City(450,410, "Nice"),
                City(170,260, "Nantes"),
                City(340,410, "Montpellier"),
                City(460,200, "Strasbourg"),
                City(200,360, "Bordeaux"),
                City(310,100, "Lilles"),
                ]

colors = ['red','blue','green','purple','pink']
nb_cities = len(city_list)

# Extraction des attributs des villes
names = [city.name for city in city_list]
x = [city.x for city in city_list]
y = [city.y for city in city_list]

#####################################
#!##### Création du graphique #######
#####################################
image = mpimpg.imread("map.jpg")
plt.imshow(image)
plt.scatter(x, y, c='red', marker='.')
for i, name in enumerate(names):
    plt.text(x[i]+5, y[i]+5, name, size = 'xx-small')
plt.show(block=False)

#####################################
#!###### Traçage des chemins ########
#####################################
def drawBestRoutes(population, nb_routes):
    # On ne peut pas sélectionner plus de routes qu'il n'y en a dans la pop
    nb_routes = min(nb_routes, len(population.routes))
    # 5 est notre nombre de routes maximal
    nb_routes = min(nb_routes, 5)

    # On efface les routes précédentes
    plt.cla()

    # On affiche la carte et les villes
    plt.imshow(image)
    plt.scatter(x, y, c='red', marker='.')
    for i, name in enumerate(names):
        plt.text(x[i]+5, y[i]+5, name, size = 'xx-small')
    
    # On trace les chemins
    for i in range(nb_routes) : 
        villes = population.routes[i].cities
        for j in range(len(villes) - 1):
            plt.plot([villes[j].x, villes[j+1].x], [villes[j].y, villes[j+1].y], color = colors[i])

    #? Garde le graphique ouvert lors de l'exécution du code
    plt.show(block = False)    
    plt.pause(5) #Nombre de secondes d'affichage

#####################################
#!#### Génération des parents #######
#####################################
#? A partir de la liste de villes, créer 20 chemins "parents"

algo = GeneticAlgorithm(mutation_rate = 0.05, population_size = 20, city_list = city_list, nb_iterations = 10)
gen0 = algo.init_population()
# gen0.printPopulation()
best2gen0 = Population(city_list=city_list, routes=gen0.selectFittest(2))
best2gen0.printPopulation()
drawBestRoutes(population=Population(gen0.selectFittest(5), city_list), nb_routes=1)
#####################################
#!########## Croisements ############
#####################################
enfant1, enfant2 = algo.crossOver(best2gen0.routes[0], best2gen0.routes[1])
childPop = Population(routes=[enfant1, enfant2], city_list=city_list)
childPop.printPopulation()
#drawBestRoutes(population=childPop, nb_routes=2)