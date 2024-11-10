from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint("xinshu_plugin_api", __name__, url_prefix="/xinshu/api")
api = ExternalApi(bp)

from . import invite, xinshu
