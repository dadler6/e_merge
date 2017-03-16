'''
Created on Oct 3, 2015

@author: daadler0309

python EmergencyAppTraining.py training_file.txt training_structure.txt
'''
import sys

class EmergencyAppTraining:
    
    '''
    Structure: {Condition : [(phrase, importance),...]}
    '''
    def __init__(self):
        pass
    
    '''
    Data format: Condition: Condition1&Ranking1|...
    @param training_file is the name of the file to train
    '''
    def trainData(self, training_file):
        self.training_set = dict()
        infile = open(training_file, 'r')
        self.training_set = dict()
        training_file = infile.read().split('\n')
        for i in training_file:
            data = i.split(':')
            if data[0] not in self.training_set:
                self.training_set[data[0]] = []
            for n in data[1].split('|'):
                data_info = n.split('&')
                if len(n) > 0:
                    self.training_set[data[0]].append((data_info[0],data_info[1]))
    
    '''
    Save file to data structure
    @param training_output = the name of the file to save it too.
    '''
    def saveData(self, training_output):
        out_file = open(training_output,'w')
        out_file.write(str(self.training_set))
        out_file.close()
        
def main():
    eapp_train = EmergencyAppTraining()
    eapp_train.trainData(sys.argv[1])
    eapp_train.saveData(sys.argv[2])
    
main()
