from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sidpersonalkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    doctor = db.relationship('Doctor', backref='patients')

USERNAME = 'admin'
PASSWORD = 'admin123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['username'] = request.form['username']
            flash('Login successful.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try again.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    total_patients = Patient.query.count()
    doctors = Doctor.query.all()
    all_patients = Patient.query.all()
    return render_template('dashboard.html', total_patients=total_patients, doctors=doctors, patients=all_patients)

@app.route('/patients')
def patients():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('patients.html', patients=patients, doctors=doctors)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        contact = request.form['contact']
        doctor_id = request.form.get('doctor_id')

        new_patient = Patient(
            name=name,
            dob=dob,
            gender=gender,
            contact=contact,
            doctor_id=doctor_id if doctor_id else None
        )
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient added successfully.')
        return redirect(url_for('patients'))

    doctors = Doctor.query.all()
    return render_template('add_patient.html', doctors=doctors)

@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)
    doctors = Doctor.query.all()

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.dob = request.form['dob']
        patient.gender = request.form['gender']
        patient.contact = request.form['contact']
        doctor_id = request.form.get('doctor_id')
        patient.doctor_id = doctor_id if doctor_id else None

        db.session.commit()
        flash('Patient info updated successfully.')
        return redirect(url_for('dashboard'))

    return render_template('edit_patient.html', patient=patient, doctors=doctors)

@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully.')
    return redirect(url_for('patients'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

def add_default_doctors():
    if not Doctor.query.first():
        db.session.add_all([
            Doctor(name='Dr. Sid', specialization='Cardiology'),
            Doctor(name='Dr. Patel', specialization='Neurology'),
            Doctor(name='Dr. Sharma', specialization='Pediatrics')
        ])
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_default_doctors()

    app.run(debug=True)
