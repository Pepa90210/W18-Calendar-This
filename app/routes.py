from pkgutil import extend_path
from flask import Blueprint, render_template
import os
import sqlite3
from datetime import date, datetime


bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
  with sqlite3.connect(DB_FILE) as conn:
    curs = conn.cursor()
    curs.execute("SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;")
    rows = curs.fetchall()
    # print(rows)

  appts = []

  for row in rows:
    appts.append((row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime("%H:%M"), datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")))

  # print(appts)

  return render_template('main.html', appts=appts, rows=rows)
