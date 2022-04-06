from ssl import create_default_context
from app.models import DatabaseConnector

class Anime(DatabaseConnector):
    anime_colunm = ["id", "anime", "released_date", "seasons"]

    available_keys = ["anime", "released_date", "seasons"]

    def __init__(self, **kwargs):
        self.anime = kwargs["anime"]
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]

    @classmethod
    def serialize(cls, data: tuple):
        return dict(zip(cls.anime_colunm, data))

    @classmethod
    def check_keys(cls, keys):
        wrong_keys = []
        for i in range(3):
            if keys[i] != cls.available_keys[i]:
                wrong_keys.append(keys[i])
        return wrong_keys

    @classmethod
    def create_table(cls):
        cls.get_conn_cur()

        query = """
            CREATE TABLE IF NOT EXISTS animes (
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            )
        """

        cls.cur.execute(query)

        cls.commit_and_close()

        return 'Table created'

    @classmethod
    def get_animes(cls):
        cls.get_conn_cur()

        query = "SELECT * FROM animes;"

        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    def create_anime(self):
        self.get_conn_cur()

        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """

        query_values = tuple(self.__dict__.values())

        self.cur.execute(query, query_values)

        self.conn.commit()

        added_anime = self.cur.fetchone()

        self.cur.close()
        self.conn.close()

        return added_anime
