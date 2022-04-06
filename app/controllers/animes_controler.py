from http import HTTPStatus
from flask import jsonify, request
from psycopg2.errors import UniqueViolation

from app.models.animes_model import Anime

def get_animes():

    Anime.create_table()

    animes = Anime.get_animes()

    serialized_animes = [Anime.serialize(anime) for anime in animes]

    return {"data": serialized_animes}, HTTPStatus.OK

def create_anime():
    data = request.get_json()

    keys = Anime.check_keys(list(data.keys()))

    if keys != []:
        return {"available_keys": Anime.available_keys, "wrong_keys_sended": keys}, HTTPStatus.UNPROCESSABLE_ENTITY

    anime = Anime(**data)

    try:
        created_anime = anime.create_anime()
    except UniqueViolation as e:
        return{"error": "anime already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    serialized_anime = Anime.serialize(created_anime)

    return serialized_anime, HTTPStatus.CREATED
