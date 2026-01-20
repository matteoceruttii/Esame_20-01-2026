import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._artists_list = []
        self.load_all_artists()

        # attributi d'istanza per la creazione del grafo
        self._nodes = []
        self._edges = []
        self._id_map = {}

        # attributi d'istanza per la ricorsione
        self._soluzione_best = []
        self.peso = float('-inf')


# funzione che gestice la lettura di tutti gli artisti
    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()


# A) funzione che gestisce la lettura degli artisti del database con il vincolo del valore inserito dall'utente (nodi)
    def load_artists_with_min_albums(self, min_albums):
        self._nodes = DAO.get_nodes(min_albums)
        for artist in self._nodes:
            self._id_map[artist.id] = artist


# B) funzione che gestisce la creazione del grafo
    def build_graph(self):
        self.G.clear()
        # aggiungo i nodi
        self.G.add_nodes_from(self._nodes)

        # aggiungo gli archi
        self._edges = DAO.get_edges()
        for (u, v, w) in self._edges:
            if u in self._id_map and v in self._id_map and self._id_map[u] != self._id_map[v]:
                u = self._id_map[u]
                v = self._id_map[v]
                self.G.add_edge(u, v, weight = w)


# C) funzione che gestice la componente connessa all'artista selezionato
    def get_connected_artists(self, start):
        nodo_inizio = self._id_map[start]
        connected_artists = list(nx.node_connected_component(self.G, nodo_inizio))
        connected_artists.sort(key = lambda c: c.id, reverse = False)
        print(connected_artists)
        return connected_artists


# D) funzione che gestice la componente connessa per la ricorsione
    def get_connected_artists_recursive(self, start):
        nodo_inizio = self._id_map[start.id]
        connected_artists = list(nx.node_connected_component(self.G, nodo_inizio))
        return connected_artists

# E) funzione che gestisce e chiama la funzione ricorsiva per la ricerca del cammino massimo
    def get_best_path(self, start_artist, durata, max_num):
        component = self.get_connected_artists_recursive(start_artist)
        self._ricorsione(component, [start_artist], durata, max_num)
        return self._soluzione_best, self.peso

    # funzione ricorsiva
    def _ricorsione(self, artists, current_set, durata, max_num):
        # condizione di uscita
        if len(current_set) > max_num:
            self._soluzione_best = current_set[:]

        # passo ricorsivo
        for artista in artists:
            if artista in current_set:
                continue
            nuovo_peso = self.peso + durata
            if nuovo_peso <= self.peso:
                current_set.append(artista)
                self._ricorsione(artists, current_set, nuovo_peso, max_num)
                current_set.pop()