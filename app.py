from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Applied')
    date_applied = db.Column(db.String(50), default='')
    notes = db.Column(db.Text, default='')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    jobs = Job.query.order_by(Job.date_added.desc()).all()
    total = len(jobs)
    applied = Job.query.filter_by(status='Applied').count()
    interview = Job.query.filter_by(status='Interview').count()
    offer = Job.query.filter_by(status='Offer').count()
    rejected = Job.query.filter_by(status='Rejected').count()
    return render_template('index.html', jobs=jobs, total=total,
                           applied=applied, interview=interview,
                           offer=offer, rejected=rejected)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        job = Job(
            company=request.form['company'],
            role=request.form['role'],
            location=request.form['location'],
            status=request.form['status'],
            date_applied=request.form['date_applied'],
            notes=request.form['notes']
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    job = Job.query.get_or_404(id)
    if request.method == 'POST':
        job.company = request.form['company']
        job.role = request.form['role']
        job.location = request.form['location']
        job.status = request.form['status']
        job.date_applied = request.form['date_applied']
        job.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', job=job)

@app.route('/delete/<int:id>')
def delete(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)