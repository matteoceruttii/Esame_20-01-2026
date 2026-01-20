from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:
# funzione che legge tutti gli artisti presenti nella tabella artist
    @staticmethod
    def get_all_artists():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'], numero_album=None)
            result.append(artist)
        cursor.close()
        conn.close()
        return result

# funzione che legge dal database tutti gli artisti che verranno usati come nodi nel grafo
    @staticmethod
    def get_nodes(n_alb):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = ''' select at.id, at.name, count(*) as numero_album
                    from album a, artist at
                    where a.artist_id = at.id
                    group by at.id, at.name
                    having count(*) >= %s '''
        cursor.execute(query, (n_alb, ))

        for row in cursor:
            artist = Artist(**row)
            result.append(artist)
        cursor.close()
        conn.close()
        return result

# funzione che legge gli archi del grafo
    @staticmethod
    def get_edges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = ''' select least(a1.artist_id, a2.artist_id) as a1,
                            greatest(a1.artist_id, a2.artist_id) as a2,
                            count(*) as peso
                    from album a1, album a2, track t1, track t2
                    where t1.genre_id = t2.genre_id and t1.album_id = a1.id and t2.album_id = a2.id and a1.id <> a2.id
                    group by a1, a2 '''
        cursor.execute(query)

        for row in cursor:
            result.append((row['a1'], row['a2'], row['peso']))
        cursor.close()
        conn.close()
        return result