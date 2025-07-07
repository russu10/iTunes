import flet as ft

from model.album import Album


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.grafo = None
        self.albumSelezionato = None
        self.soglia = None

    def handleCreaGrafo(self, e):
        durata = self._view._txtInDurata.value
        if durata == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci durata"))
            self._view.update_page()
            return
        try :
            dur = int(durata)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci durata valida"))
            self._view.update_page()
            return

        self.grafo = self._model.buildGraph(dur)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {len(self.grafo.nodes)} "
                                                      f"nodi e {len(self.grafo.edges)} archi"))
        self._view._ddAlbum.options.clear()
        for a in self.grafo.nodes:
            self._view._ddAlbum.options.append(ft.dropdown.Option(key=(a.albumId), text=a.titolo))
        self._view.update_page()
        return

    def getSelectedAlbum(self, e):
        self.albumSelezionato  = self._model.idMapAlbum[int(self._view._ddAlbum.value)]
        return



    def handleAnalisiComp(self, e):
        if self.albumSelezionato is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona un album"))
            self._view.update_page()
            return
        dimensione , durata = self._model.getInfoConnessa(self.albumSelezionato)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f" Componente connessa {self.albumSelezionato.titolo} \n "
                                                      f"Dimensione della componente connessa : {dimensione} \n"
                                                      f" Durata totale : {durata}"))
        self._view.update_page()
        return

    def handleGetSetAlbum(self, e):
        sos = self._view._txtInSoglia.value
        if sos is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci una soglia"))
            self._view.update_page()
            return
        try :
            self.soglia = int(sos)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci una soglia valida"))
            self._view.update_page()
            return
        setOfNodes, sumDurate = self._model.getSetOfNodes(self.albumSelezionato, self.soglia)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Ho trovato un set di album che soddisfa le specifiche, "
            f"dimensione: {len(setOfNodes)}, durata totale: {sumDurate}."))
        self._view.txt_result.controls.append(ft.Text(
            f"Di seguito gli album che fanno parte della soluzione trovata:"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()

