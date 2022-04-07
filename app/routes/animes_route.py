from flask import Blueprint
from app.controllers import animes_controler

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(animes_controler.get_animes)
bp.post("")(animes_controler.create_anime)
bp.get("/<id>")(animes_controler.get_anime_by_id)
bp.patch("/<id>")(animes_controler.update_anime)
bp.delete("/<id>")(animes_controler.delete_anime)
