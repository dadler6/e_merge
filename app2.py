#!/bin/python

from flask import Flask, render_template, request, jsonify, redirect
import sys
import os.path
from check_login import Login

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index2.html', name=name)

@app.route('/patient_information', methods=['GET','POST'])
def login_information():
    patient_data = dict()
    patient_data['Note'] = ''
    known = ['FirstName','LastName','Age','Sex','Weight','HeightFt','HeightIn','Symptom','Note']
    FirstName = request.form["firstname"]
    LastName = request.form["lastname"]
    if os.path.isfile('patient_data/' + FirstName + LastName + '.txt'):
        in_file = open('patient_data/' + FirstName + LastName + '.txt', 'r')
        for line in in_file.readlines():
            if line != '':
                data = line.split(':')
                # Check if exists
                if data[0].strip() not in patient_data:
                    patient_data[data[0].strip()] = ''
                if data[0].strip() not in known:
                    patient_data['Note'] += (data[0].strip() + ': ' + data[1].strip() + '\n')
                else:
                    patient_data[data[0].strip()] += (data[1].strip() + '\n')
        global global_patient_data
        global_patient_data = patient_data
        return render_template('hospital.html', name=next)
    else:
        return render_template('index2.html', name=next)
       
@app.route('/get_data', methods=['GET','POST'])
def get_data():
    return jsonify(global_patient_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')