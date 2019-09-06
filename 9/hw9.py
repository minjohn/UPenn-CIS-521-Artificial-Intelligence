############################################################
# CIS 521: Homework 9
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

import homework9_data as data

# Include your imports here, if any are used.



############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.N = iterations
        self.w = {}
        for i in range(iterations):
            for elem in examples:
                xi = elem[0]
                yi = elem[1]
                dot_product = 0
                for feature in xi:
                    if feature not in self.w:
                        self.w[feature] = 0
                    dot_product += xi[feature]*self.w[feature]
                if dot_product>0 and yi==False:
                    for f in xi:
                        self.w[f] -= xi[f]
                if dot_product<=0 and yi==True:
                    for f in xi:
                        self.w[f] += xi[f]

    def predict(self, x):
        dot_product = 0
        for f in x:
            if f not in self.w:
                self.w[f] = 0
            dot_product+=x[f]*self.w[f]
        if dot_product>0:
            return True
        else:
            return False

class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        self.N = iterations
        self.w = {}
        for i in range(iterations):
            for (xi,yi) in examples:
                if yi not in self.w:
                    self.w[yi] = {}
                max_dot_product = -99999
                predicat_lable = "<START>"
                for yk in self.w:
                    dot_product = 0
                    for f in xi:
                        if f not in self.w[yk]:
                            self.w[yk][f]=0
                        dot_product += self.w[yk][f]*xi[f]
                    if max_dot_product<dot_product:
                        max_dot_product=dot_product
                        predicat_lable = yk
                if predicat_lable!=yi:
                    for f in xi:
                        self.w[yi][f] += xi[f]
                        self.w[predicat_lable][f] -= xi[f]

    def predict(self, x):
        max_dot_product = -99999
        predict_lable = "<START>"
        for yk in self.w:
            dot_product = 0
            for f in x:
                if f not in self.w[yk]:
                    self.w[yk][f] = 0
                dot_product += x[f] * self.w[yk][f]
            if max_dot_product<dot_product:
                max_dot_product=dot_product
                predict_lable = yk
        return predict_lable

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        iterations = 30
        data_list = []
        for (x,y) in data:
            d = {}
            for i in range(4):
                d["p%s"%i] = x[i]
            data_list.append((d,y))
        self.p = MulticlassPerceptron(data_list,iterations)

    def classify(self, instance):
        d = {}
        for i in range(4):
            d["p%s"%i] = instance[i]
        return self.p.predict(d)

class DigitClassifier(object):

    def __init__(self, data):
        iterations = 9
        data_list = []
        for (x,y) in data:
            d ={}
            for i in range(64):
                d["p%s"%i]=x[i]
            data_list.append((d,y))
        self.p = MulticlassPerceptron(data_list,iterations)

    def classify(self, instance):
        d = {}
        for i in range(64):
            d["p%s"%i]=instance[i]
        return self.p.predict(d)

class BiasClassifier(object):

    def __init__(self, data):
        iterations = 4
        data_list = []
        for (x,y) in data:
            d = {}
            d["p1"]=x-1
            data_list.append((d,y))
        self.p = BinaryPerceptron(data_list,iterations)

    def classify(self, instance):
        d ={}
        d["p1"]=instance-1
        return self.p.predict(d)

class MysteryClassifier1(object):

    def __init__(self, data):
        iterations = 4
        data_list = []
        for (x,y) in data:
            d={}
            d["p1"]=x[0]*x[0]+x[1]*x[1]-4
            data_list.append((d,y))
        self.p = BinaryPerceptron(data_list,iterations)

    def classify(self, instance):
        d = {}
        d["p1"]=instance[0]*instance[0]+instance[1]*instance[1]-4
        return self.p.predict(d)

class MysteryClassifier2(object):

    def __init__(self, data):
        iterations = 4
        data_list = []
        for (x,y) in data:
            d={}
            d["p1"]=x[0]*x[1]*x[2]
            data_list.append((d,y))
        self.p=BinaryPerceptron(data_list,iterations)

    def classify(self, instance):
        d={}
        d["p1"]=instance[0]*instance[1]*instance[2]
        return self.p.predict(d)

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
About 8 hours
"""

feedback_question_2 = """
The understanding of perceptrons I found most challenging
"""

feedback_question_3 = """
The usage of visualize the training data and usage of Kernel function
"""