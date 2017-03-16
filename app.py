#!/bin/python

from flask import Flask, render_template, request, jsonify, redirect
import sys
from check_login import Login
from EmergencyApp import EmergencyApp

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/login_information', methods=['GET','POST'])
def login_information():
    username = request.form["username"]
    password = request.form["password"]
    login = Login(username,password)
    login.queryData()
    i = login.checkUsername()
    if login.checkPassword(i):
        return render_template('home.html', name=next)
    else:
        return render_template('index.html', name=next)

@app.route('/get_patient_information', methods=['GET','POST'])
def get_patient_information():
    try:
        em_app = EmergencyApp()
        em_app.openPatientData(request.json)
        em_app.openTrainingData()
        em_app.getNoteFuzzyScore()
        em_app.GetTopScores()
        em_app.rankNotes()
        em_app.rankVitals()
        em_app.outputObject()
        return 'True'
    except:
        return 'False'


@app.route('/load_patient_information', methods=['GET','POST'])
def load_patient_information():
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    patient_data = open(first_name + last_name + ".txt", "r")

if __name__ == '__main__':
    app.run(host='0.0.0.0')