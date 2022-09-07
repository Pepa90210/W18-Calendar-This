from flask import Blueprint, render_template
import os

bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
  return render_template('main.html')

