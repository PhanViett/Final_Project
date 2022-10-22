import pickle
import click
from flask.cli import with_appcontext
from application.extensions import pwd_context
from application.models import VanBangChuyenMon
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
import json


@click.command("init")
@with_appcontext
def init():
    return