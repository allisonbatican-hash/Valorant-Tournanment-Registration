from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# =====================
# APP SETUP
# =====================
app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for flash messages

# =====================
# DATABASE CONFIG
# =====================
# XAMPP DEFAULT:
# username: root
# password: (EMPTY)
# database: tournament_db
# phpMyAdmin is only the viewer, NOT the database itself

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/tournament_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# DATABASE MODEL
# =====================
class Squad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    captain = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    player1 = db.Column(db.String(100), nullable=False)
    player2 = db.Column(db.String(100), nullable=False)
    player3 = db.Column(db.String(100), nullable=False)
    player4 = db.Column(db.String(100), nullable=False)
    player5 = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)

# =====================
# ROUTES
# =====================
@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    required_fields = [
        'team_name', 'captain', 'contact',
        'player1', 'player2', 'player3', 'player4', 'player5'
    ]

    # validation
    for field in required_fields:
        if field not in request.form or request.form[field].strip() == "":
            flash("All fields are required!", "error")
            return redirect(url_for('home'))

    squad = Squad(
        team_name=request.form['team_name'].strip(),
        captain=request.form['captain'].strip(),
        contact=request.form['contact'].strip(),
        player1=request.form['player1'].strip(),
        player2=request.form['player2'].strip(),
        player3=request.form['player3'].strip(),
        player4=request.form['player4'].strip(),
        player5=request.form['player5'].strip()
    )

    try:
        db.session.add(squad)
        db.session.commit()
        flash("Squad registered successfully!", "success")
        return redirect(url_for('success'))
    except Exception as e:
        db.session.rollback()
        flash(f"Database Error: {e}", "error")
        return redirect(url_for('home'))


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/tournament')
def tournament():
    squads = Squad.query.all()
    return render_template('tournament.html', squads=squads)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    squad = Squad.query.get_or_404(id)
    try:
        db.session.delete(squad)
        db.session.commit()
        flash("Squad deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Delete failed: {e}", "error")

    return redirect(url_for('tournament'))

# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # auto-create tables

    app.run(debug=True)
