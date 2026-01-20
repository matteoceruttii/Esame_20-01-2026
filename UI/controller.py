import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model


# funzione che gestice l'handler per la creazione del grafo
    def handle_create_graph(self, e):
        # A) controllo che il valore inserito dall'utente sia valido
        try:
            self._valore = int(self._view.txtNumAlbumMin.value)
            if self._valore == 0:
                raise ValueError
        except ValueError:
            self._view.show_alert("Numero album minimo non valido")

        # B) grafo semplice, non orientato e pesato
        self._model.load_artists_with_min_albums(self._valore)
        self._model.build_graph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Grafo creato: {self._model.G.number_of_nodes()} nodi (artisti) '
                                                      f'e {self._model.G.number_of_edges()} archi'))

        # aggiorno la dropdown per gli artisti
        self._view.ddArtist.clean()
        self._view.ddArtist.disabled = False
        self._view.ddArtist.options = [ft.dropdown.Option(key = artista.id, text = artista.name) for artista in self._model.G.nodes()]
        self._view.btnArtistsConnected.disabled = False
        self._view._page.update()


# funzione che gestisce la componente connessa
    def handle_connected_artists(self, e):
        self._artista_selezionato = int(self._view.ddArtist.value)
        self._model.get_connected_artists(self._artista_selezionato)

        # aggiorno la listview
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {self._artista_selezionato}, "
                                                      f"{self._model._id_map[self._artista_selezionato].name}: "))
        self._connessi = self._model.get_connected_artists(self._artista_selezionato)
        for connesso in self._connessi:
            self._view.txt_result.controls.append(ft.Text(f'{connesso.id}, {connesso.name} - Numero di generi in comune: '))

        # aggiorno i bottoni e boxes per continuare con la ricorsione
        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.btnSearchArtists.disabled = False
        self._view._page.update()


# funzione che gestisce la parte ricorsiva
    def handler_cammino(self, e):
        # controllo che il valore immesso dall'utente sia accettabile (durata minima)
        try:
            self._durata = float(self._view.txtMinDuration.value)
            if self._durata == 0:
                raise ValueError
        except ValueError:
            self._view.show_alert("Durata minima non valida")


        # controllo che il valore inserito per il numero massimo di artisti sia accettabile
        try:
            self._numero_artisti = int(self._view.txtMaxArtists.value)
            if self._numero_artisti < 1 or self._numero_artisti > len(self._connessi):
                raise ValueError
        except ValueError:
            self._view.show_alert("Numero artisti non valido (non rispetta il range previsto)")

        # chiamata della funzione del model che gestisce la ricorsione
        start_artist = self._model._id_map[self._artista_selezionato]
        path, peso = self._model.get_best_path(start_artist, self._durata, self._numero_artisti)

        # aggiorno la listview
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dall'artista {self._artista_selezionato},"
                                                      f"{self._model._id_map[self._artista_selezionato].name}: "))
        # -> lunghezza del cammino
        self._view.txt_result.controls.append(ft.Text(f'Lunghezza {len(path) - 1}'))

        # -> dettagli della ricorsione
        for nodo in path:
            self._view.txt_result.controls.append(ft.Text(f'{nodo.id}, {nodo.name}'))

        # -> peso massimo ricavato
        self._view.txt_result.controls.append(ft.Text(f'Peso massimo {peso}'))
        self._view._page.update()