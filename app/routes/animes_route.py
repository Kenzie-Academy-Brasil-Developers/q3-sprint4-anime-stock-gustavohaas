from flask import Blueprint
from app.controllers import animes_controler

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(animes_controler.get_animes)
bp.post("")(animes_controler.create_anime)
