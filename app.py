# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date, timedelta
from config import Config
from models import db, Event, DailyNote, GymLog
import calendar

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ---------- Helper functions ----------

def get_week_dates(start_date=None):
    """Return a list of 7 dates (Mon-Sun) for the week of start_date."""
    if start_date is None:
        start_date = date.today()
    # make start_date = Monday of that week
    start_date = start_date - timedelta(days=start_date.weekday())
    return [start_date + timedelta(days=i) for i in range(7)]

# ---------- Routes ----------

@app.route("/")
def dashboard():
    today = date.today().strftime("%Y-%m-%d")
    events_today = Event.query.filter_by(date=today).all()
    note = DailyNote.query.filter_by(date=today).first()
    gym_today = GymLog.query.filter_by(date=today).first()

    # Simple stats
    total_events = Event.query.count()
    total_gym_days = GymLog.query.count()

    return render_template(
        "dashboard.html",
        today_str=today,
        events_today=events_today,
        note=note,
        gym_today=gym_today,
        total_events=total_events,
        total_gym_days=total_gym_days
    )

@app.route("/calendar")
def calendar_view():
    # Get month and year from query params or use current
    year = request.args.get("year", type=int, default=date.today().year)
    month = request.args.get("month", type=int, default=date.today().month)

    cal = calendar.Calendar(firstweekday=0)  # Monday = 0 in some systems; here 0=Monday or Sunday depending OS
    month_days = list(cal.itermonthdates(year, month))

    # fetch events for this month
    events = Event.query.all()
    events_by_date = {}
    for event in events:
        events_by_date.setdefault(event.date, []).append(event)

    return render_template(
        "calendar.html",
        year=year,
        month=month,
        month_days=month_days,
        events_by_date=events_by_date
    )

@app.route("/day/<string:day_str>", methods=["GET", "POST"])
def day_view(day_str):
    # day_str = "YYYY-MM-DD"
    if request.method == "POST":
        # Add or update note
        content = request.form.get("note_content", "")
        note = DailyNote.query.filter_by(date=day_str).first()
        if note:
            note.content = content
        else:
            note = DailyNote(date=day_str, content=content)
            db.session.add(note)
        db.session.commit()
        return redirect(url_for("day_view", day_str=day_str))

    events = Event.query.filter_by(date=day_str).all()
    note = DailyNote.query.filter_by(date=day_str).first()
    gym_log = GymLog.query.filter_by(date=day_str).first()

    return render_template(
        "daily.html",
        day_str=day_str,
        events=events,
        note=note,
        gym_log=gym_log
    )

@app.route("/week")
def week_view():
    # Optional query param ?date=YYYY-MM-DD
    date_str = request.args.get("date")
    if date_str:
        start_day = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        start_day = date.today()

    week_dates = get_week_dates(start_day)
    events = Event.query.all()

    # group events by date
    events_by_date = {}
    for event in events:
        events_by_date.setdefault(event.date, []).append(event)

    return render_template(
        "weekly.html",
        week_dates=week_dates,
        events_by_date=events_by_date
    )

@app.route("/events", methods=["GET", "POST"])
def events_page():
    if request.method == "POST":
        title = request.form.get("title")
        date_str = request.form.get("date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        category = request.form.get("category")
        notes = request.form.get("notes")

        new_event = Event(
            title=title,
            date=date_str,
            start_time=start_time,
            end_time=end_time,
            category=category,
            notes=notes
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for("events_page"))

    all_events = Event.query.order_by(Event.date).all()
    return render_template("events.html", events=all_events)

@app.route("/gym", methods=["GET", 'POST'])
def gym_page():
    if request.method == "POST":
        date_str = request.form.get("date")
        # toggle gym log
        existing = GymLog.query.filter_by(date=date_str).first()
        if existing:
            db.session.delete(existing)  # remove if clicked again
        else:
            log = GymLog(date=date_str, went=True)
            db.session.add(log)
        db.session.commit()
        return redirect(url_for("gym_page"))

    logs = GymLog.query.order_by(GymLog.date).all()
    return render_template("gym.html", logs=logs)

# ---------- Initialize DB ----------

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

