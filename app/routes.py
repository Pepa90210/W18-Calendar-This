from flask import Blueprint, render_template, redirect, url_for
import os
import sqlite3
from datetime import datetime, timedelta
from .forms import AppointmentForm



bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
  current_date = datetime.now()
  return redirect(url_for(".daily", year=current_date.year, month=current_date.month, day=current_date.day))


@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def daily(year, month, day):
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

  day = datetime(year, month, day)
  next_day = day + timedelta(days=1)


  with sqlite3.connect(DB_FILE) as conn:
    curs = conn.cursor()
    curs.execute("""
                  SELECT id, name, start_datetime, end_datetime
                  FROM appointments
                  WHERE start_datetime BETWEEN :day AND :next_day
                  ORDER BY start_datetime;
                """,
                {
                  'day': day,
                  'next_day': next_day
                })
    rows = curs.fetchall()
    # print(rows)

  appts = []

  for row in rows:
    appts.append((row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime("%H:%M"), datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime("%H:%M")))

  # print(appts)

  return render_template('main.html', appts=appts, rows=rows, form=form)
