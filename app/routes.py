from flask import Blueprint, render_template, redirect
import os
import sqlite3
from datetime import datetime
from .forms import AppointmentForm



bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")

@bp.route("/", methods=['GET', 'POST'])
def main():
  form = AppointmentForm()
  if form.validate_on_submit():
    with sqlite3.connect(DB_FILE) as conn:
      curs = conn.cursor()
      curs.execute("""
                  INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
                  VALUES (:name, :start_datetime, :end_datetime, :description, :private)
                  """,
                  { 'name': form.name.data,
                    'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
                    'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
                    'description': form.description.data,
                    'private': form.private.data
                  })
      return redirect('/')


  with sqlite3.connect(DB_FILE) as conn:
    curs = conn.cursor()
    curs.execute("SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime;")
    rows = curs.fetchall()
    # print(rows)

  appts = []

  for row in rows:
    appts.append((row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime("%H:%M"), datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")))

  print(appts)

  return render_template('main.html', appts=appts, rows=rows, form=form)
