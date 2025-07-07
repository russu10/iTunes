import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.albums = None
        self.grafo = None
        self.idMapAlbum = {}
        self.archi = None
        self._bestSet = {}
        self._maxLen = 0



    def trovaAlbums(self,durata):
        self.albums = DAO.getAllAlbums(durata)
        return self.albums

    def buildGraph(self,durata):
        albums = []
        for a in self.trovaAlbums(durata):
            albums.append(a)
        self.grafo = nx.Graph()
        self.grafo.add_nodes_from(albums)
        self.idMapAlbum = {a.albumId: a for a in albums}
        edges = DAO.getAllEdges(self.idMapAlbum)
        self.grafo.add_edges_from(edges)
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes())
    def getNumEdges(self):
        return len(self.grafo.edges())
    def getInfoConnessa(self,album):
        connessa = nx.node_connected_component(self.grafo, album)
        durataTot = 0
        for nodo in connessa:

            durataTot += nodo.durata
        return len(connessa), durataTot

    def getSetOfNodes(self, a1 , soglia):
        self._bestSet = {}
        self._maxLen = 0
        parziale = {a1}
        cc = nx.node_connected_component(self.grafo, a1)
        cc.remove(a1)

        for n in cc:
            # richiamo la mia ricorsione
            parziale.add(n)
            cc.remove(n)
            self.ricorsione(parziale, cc, soglia)
            cc.add(n)
            parziale.remove(n)

        return self._bestSet, self.getDurataTot(self._bestSet)

    def ricorsione(self,parziale, rimanenti, soglia):


        # 1) verifico che parziale sia una soluzione ammissibile, ovvero se viola i vincoli.


        if self.getDurataTot(parziale) > soglia:
            return


        # 2) se parziale soddisfa i criteri, allora verifico se è migliore di bestSet


        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)


        # 3) aggiungo e faccio ricorsione


        for r in rimanenti:
            parziale.add(r)
            rimanenti.remove(r)
            self.ricorsione(parziale, rimanenti, soglia)
            parziale.remove(r)
            rimanenti.add(r)

    def getDurataTot(self, listOfNodes):
        # sumDurata = 0
        # for n in listOfNodes:
        #     sumDurata += n.dTot
        # return sumDurata
        return sum([n.durata for n in listOfNodes])