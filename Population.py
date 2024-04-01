class Population :
    def __init__(self, routes, city_list) :
        self.routes = routes
        self.city_list = city_list

    def printPopulation(self):
        for route in self.routes:
            print(route.toString())
    
    def selectFittest(self, nb): #* nb = nombre de routes qu'on sélectionne
        # On crée un tuple score, route 
        scores = [[route.score, route] for route in self.routes]
        # On trie le tuple de façon croissante sur le score
        scores.sort(key=lambda x: x[0])
        # On renvoie les routes dans le nouvel ordre
        sortedList = [score[1] for score in scores]
        result = [None] * nb
        for i in range(nb):
            result[i] = sortedList[i]
        return Population(result, self.city_list)
