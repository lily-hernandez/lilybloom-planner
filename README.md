# LilyBloom Planner 🌸

LilyBloom Planner is an aesthetic web-based planner built with Python and Flask.

It helps you balance:

- 🌸 School schedule  
- 🌸 Work schedule  
- 🌸 Appointments and events  
- 🌸 Gym days  
- 🌸 Daily notes and to-dos  

## Features

- Dashboard with today’s events, daily note, and gym status  
- Monthly calendar view with color-coded events (work, school, gym, family, other)  
- Day view with events, note, and gym toggle  
- Week-at-a-glance view  
- Events page to add work/school/gym/family/other events  
- Gym tracker page to log gym days  

## Tech Stack

- Python 3  
- Flask  
- SQLite (via SQLAlchemy)  
- HTML + CSS  

## How to Run Locally

```bash
python3 -m venv venv
source venv/bin/activate       # on Mac
pip3 install -r requirements.txt  # or: python3 -m pip install -r requirements.txt
python3 init_db.py
python3 app.py
