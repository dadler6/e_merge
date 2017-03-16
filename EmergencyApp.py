'''
Created on Oct 3, 2015

Dan Adler
Parses through patient vitals information.

REQUIRES:
python-levenshtein
fuzzywuzzy

python EmergencyApp.py patient_data.txt
'''

import sys
import datetime
from collections import Counter
from fuzzywuzzy import fuzz

class EmergencyApp:
    
    '''
    Setup variables
    '''
    def __init__(self):
        self.patient_data = dict()
        self.patient_condition_scores = Counter()
        
    def openPatientData(self, patient_data):
        for i in patient_data:
            if i not in self.patient_data:
                self.patient_data[i] = []
            if i == 'Notes':
                for n in patient_data[i].split('|'):
                    self.patient_data[i].append(n)
            else:
                self.patient_data[i].append(patient_data[i])

    '''
    Open training and vitals data
    '''
    def openTrainingData(self):
        self.training_notes = eval(open('training_notes.txt','r').read())
        self.training_vitals = eval(open('training_vitals.txt','r').read())
    
    '''
    Go through the patient notes.
    For each note match to important patient fuzzy score terms.
    '''
    def getNoteFuzzyScore(self):
        for note in self.patient_data['Notes']:
            for condition in self.training_notes:
                if condition not in self.patient_condition_scores:
                    self.patient_condition_scores[condition] = 0
                count = 1
                # Check if actual condition is in the note
                self.patient_condition_scores[condition] += fuzz.partial_ratio(condition, note)*2
                for c in self.training_notes[condition]:
                    # Check if symptoms of condition are in the notes
                    score = fuzz.partial_ratio(c[0],note)
                    # Filter scores
                    if score >= 35:
                        self.patient_condition_scores[condition] += score*(int(c[1]) + 1)
                    count += 1
                self.patient_condition_scores[condition] \
                    = self.patient_condition_scores[condition] / count
    
    '''
    Find top two scores
    '''
    def GetTopScores(self):
        self.top = self.patient_condition_scores.most_common(3)
        
    '''
    Get notes data for top scores
    '''
    def rankNotes(self):
        self.note_counter = Counter()
        for note in self.patient_data['Notes']:
            for i in range(len(self.top)):
                self.note_counter[note] += fuzz.partial_ratio(self.top[i][0],note)*(len(self.top) - i)
        
        
    '''
    Rank Vitals
    '''
    def rankVitals(self):
        self.important_vitals = set()
        for condition in self.top:
            for vitals in self.training_vitals[condition[0]]:
                self.important_vitals.add(vitals[0])
        self.sorted = sorted(self.important_vitals)
            
    '''Print output'''
    def outputObject(self):
        name = 'patient_data/'+ self.patient_data['FirstName'][0] + \
            self.patient_data['LastName'][0] + '.txt'
        out_file = open(name, 'w')
        out_file.write('FirstName: ' + self.patient_data['FirstName'][0] + '\n')
        out_file.write('LastName: ' + self.patient_data['LastName'][0] + '\n')
        out_file.write('Sex: ' + self.patient_data['Sex'][0] + '\n')
        out_file.write('Age: ' + self.patient_data['Age'][0] + '\n')
        out_file.write('Weight: ' + self.patient_data['Weight'][0] + '\n')
        out_file.write('HeightFt: ' + self.patient_data['HeightFt'][0] + '\n')
        out_file.write('HeightIn: ' + self.patient_data['HeightIn'][0] + '\n')
        out_file.write('Symptom: ' + self.patient_data['Symptom'][0] + '\n')
        for i in self.note_counter:
            out_file.write('Note: ' + i.strip() + '\n')
        for i in self.sorted:
            out_file.write(i + ': ' + ', '.join(self.patient_data[i]) + '\n')
        out_file.close()