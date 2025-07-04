from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos usando variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@postgres-service:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Estudiante(db.Model):
    __tablename__ = 'alumnos'
    __table_args__ = {'schema': 'public'}  # Esquema explícito
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return {
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre
        }

# Rutas con vistas

@app.route('/')
def index():
    alumnos = Estudiante.query.all()
    return render_template('index.html', alumnos=alumnos)

@app.route('/alumnos/new', methods=['GET', 'POST'])
def create_estudiante():
    if request.method == 'POST':
        no_control = request.form['no_control']
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        ap_materno = request.form['ap_materno']
        semestre = int(request.form['semestre'])

        nuevo_estudiante = Estudiante(
            no_control=no_control,
            nombre=nombre,
            ap_paterno=ap_paterno,
            ap_materno=ap_materno,
            semestre=semestre
        )
        db.session.add(nuevo_estudiante)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create_estudiante.html')

@app.route('/alumnos/update/<string:no_control>', methods=['GET', 'POST'])
def update_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.ap_paterno = request.form['ap_paterno']
        estudiante.ap_materno = request.form['ap_materno']
        estudiante.semestre = int(request.form['semestre'])
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_estudiante.html', estudiante=estudiante)

@app.route('/alumnos/delete/<string:no_control>')
def delete_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
