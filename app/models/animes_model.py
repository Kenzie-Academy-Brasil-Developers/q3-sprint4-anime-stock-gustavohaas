from psycopg2 import sql
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
    def capitalize(cls, data):
        if data["anime"]:
            anime = data["anime"].split()
            anime_list = []
            for word in anime:
                word = word.capitalize()
                anime_list.append(word)
            anime = " ".join(anime_list)
            data["anime"] = anime
            return data
        else:
            return data

    @classmethod
    def check_keys(cls, keys):
        wrong_keys = []
        for i in range(len(keys)):
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
    
    @classmethod
    def get_by_id(cls, id: str):
        cls.get_conn_cur()

        query = f"SELECT * FROM animes WHERE id={id};"

        cls.cur.execute(query)
        anime = cls.cur.fetchall()

        cls.commit_and_close()

        return anime

    @classmethod
    def update_anime(cls, id: str, data: dict):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]
        sql_anime_id = sql.Literal(id)

        query = sql.SQL(
            """
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                id = {id}
            RETURNING *;
            """
        ).format(
            id=sql_anime_id,
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)

        updated_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_anime

    @classmethod
    def delete_anime(cls, id: str):
        cls.get_conn_cur()

        query = f"DELETE FROM animes WHERE id = {id} RETURNING *"

        cls.cur.execute(query)

        deleted_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return deleted_anime
