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
    Anime.create_table()

    keys = Anime.check_keys(list(data.keys()))

    if keys != []:
        return {"available_keys": Anime.available_keys, "wrong_keys_sended": keys}, HTTPStatus.UNPROCESSABLE_ENTITY

    data = Anime.capitalize(data)

    anime = Anime(**data)

    try:
        created_anime = anime.create_anime()
    except UniqueViolation as e:
        return{"error": "anime already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    serialized_anime = Anime.serialize(created_anime)

    return serialized_anime, HTTPStatus.CREATED

def get_anime_by_id(id: str):

    Anime.create_table()

    anime = Anime.get_by_id(id)
    if anime == []:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND

    serialised_anime = Anime.serialize(anime)

    return {"data": serialised_anime}, HTTPStatus.OK

def update_anime(id: str):
    Anime.create_table()

    data = request.get_json()

    keys = Anime.check_keys(list(data.keys()))

    if keys != []:
        return {"available_keys": Anime.available_keys, "wrong_keys_sended": keys}, HTTPStatus.UNPROCESSABLE_ENTITY

    data = Anime.capitalize(data)

    updated_anime = Anime.update_anime(id, data)

    if not updated_anime:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND

    serialized_anime = Anime.serialize(updated_anime)

    return {"data": serialized_anime}, HTTPStatus.OK

def delete_anime(id: str):
    Anime.create_table()

    deleted_anime = Anime.delete_anime(id)

    print(deleted_anime)

    if deleted_anime == None:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND


    return {"data": deleted_anime}, HTTPStatus.NO_CONTENT
