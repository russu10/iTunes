from pprint import pprint

from model.modello import Model

mymodel = Model()
grafo = mymodel.buildGraph(120)
nodes = mymodel.getNumNodes()
print(len(grafo.edges()))