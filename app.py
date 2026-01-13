from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy  # Added missing import for SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tournament.db')
db = SQLAlchemy(app)  # Added db initialization


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
    # Added basic validation to ensure all required fields are present
    required_fields = ['team_name', 'captain', 'contact', 'player1', 'player2', 'player3', 'player4', 'player5']
    if not all(field in request.form and request.form[field].strip() for field in required_fields):
        return "Error: All fields are required and cannot be empty.", 400

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
        return redirect(url_for('success'))
    except Exception as e:
        db.session.rollback()
        return f"Error registering squad: {str(e)}", 500


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/tournament')
def tournament():
    squads = Squad.query.all()
    return render_template('tournament.html', squads=squads)


@app.route('/delete/<int:id>',
           methods=['POST'])  # Changed to POST for security (requires form submission from template)
def delete(id):
    squad = Squad.query.get_or_404(id)
    try:
        db.session.delete(squad)
        db.session.commit()
        return redirect(url_for('tournament'))
    except Exception as e:
        db.session.rollback()
        return f"Error deleting squad: {str(e)}", 500


# =====================
# RUN
# =====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)