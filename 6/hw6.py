############################################################
# CIS 521: Homework 6
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
from os import listdir

############################################################
# Section 1: Probability
############################################################

# Set the following variables to True or False.
section_1_problem_1a = False # a,b independent can not give a b conditionally independent given c
section_1_problem_1b = True
section_1_problem_1c = False # can only tell a is independent of b and c, no relationship between b,c could be given

# Set the following variables to True or False.
section_1_problem_2a = True
section_1_problem_2b = False
section_1_problem_2c = False
section_1_problem_2d = False
section_1_problem_2e = True
section_1_problem_2f = False
section_1_problem_2g = False
section_1_problem_2h = True

# Set the following variables to probabilities, expressed as decimals between 0
# and 1.
section_1_problem_3a = 0.01162455
section_1_problem_3b = 0.98837545
section_1_problem_3c = 0.10871841
section_1_problem_3d = 0.102114796
section_1_problem_3e = 0.042926393
section_1_problem_3f = 0.000007463
section_1_problem_3g = 0.000514553


############################################################
# Section 2: Spam Filter
############################################################
def load_tokens(email_path):
    tokens = []
    infile = open(email_path)
    message = email.message_from_file(infile)
    #for part in email.iterators.typed_subpart_iterator(message,'text','plain'):
    for body_line in email.iterators.body_line_iterator(message):
        str_list = body_line.split()
        for elem in str_list:
            tokens.append(elem)
    return tokens

def log_probs(email_paths, smoothing):
    prob_dict = {}
    count_dict = {}
    tokens_list = []
    alpha = smoothing
    #from training corpus,extract vocabulary
    for path in email_paths:
        tokens = load_tokens(path)
        tokens_list+=tokens
        for i in range(len(tokens)):
            if tokens[i] in count_dict:
                count_dict[tokens[i]]+=1
            else:
                count_dict[tokens[i]]=1
            if i!=len(tokens)-1:
                tokens_list.append((tokens[i],tokens[i+1]))
                if (tokens[i],tokens[i+1]) in count_dict:
                    count_dict[(tokens[i],tokens[i+1])]+=1
                else:
                    count_dict[(tokens[i],tokens[i+1])]=1
    print count_dict
    #for each word in vocabulary,calculate the probabilty of occurance
    #add the laplace-smoothed log probabilities to prob_dict
    count_sum = len(tokens_list)
    V = len(count_dict)
    for feature in count_dict:
        count = count_dict[feature]
        pw = (count+alpha)/(count_sum+alpha*(V+1))
        prob_dict[feature] = math.log(pw)
    #add unkown tokens unk to prob_dict
    prob_dict["<UNK>"]=math.log(alpha/(count_sum+alpha*(V+1)))
    return prob_dict

class SpamFilter(object):

    # Note that the initialization signature here is slightly different than the
    # one in the previous homework. In particular, any smoothing parameters used
    # by your model will have to be hard-coded in.

    def __init__(self, spam_dir, ham_dir):
        spam_files = [f for f in listdir(spam_dir)]
        ham_files = [f for f in listdir(ham_dir)]
        spam_paths = [spam_dir+"/"+fname for fname in spam_files]
        ham_paths = [ham_dir+"/"+fname for fname in ham_files]
        self.smoothing = 1e-5
        self.spam_dict = log_probs(spam_paths,self.smoothing)
        self.ham_dict = log_probs(ham_paths,self.smoothing)
        self.p_spam = len(spam_files)/float(len(spam_files)+len(ham_files))
        self.p_ham = len(ham_files)/float(len(spam_files)+len(ham_files))

    def is_spam(self, email_path):
        tokens = load_tokens(email_path)
        ps = self.p_spam
        ph = self.p_ham
        for i in range(len(tokens)):
            if tokens[i] in self.spam_dict:
                ps+=self.spam_dict[tokens[i]]
            else:
                ps+=self.spam_dict["<UNK>"]
            if tokens[i] in self.ham_dict:
                ph+=self.ham_dict[tokens[i]]
            else:
                ps+=self.ham_dict["<UNK>"]
            if i!=len(tokens)-1:
                if (tokens[i],tokens[i+1]) in self.spam_dict:
                    ps+=self.spam_dict[(tokens[i],tokens[i+1])]
                if (tokens[i],tokens[i+1]) in self.ham_dict:
                    ph+=self.ham_dict[(tokens[i],tokens[i+1])]
        if ps>ph:
            return True
        else:
            return False

    def testProb(self,dir_path,flag):
        files = [f for f in listdir(dir_path)]
        file_paths = [dir_path + "/" + fname for fname in files]
        print file_paths
        true_list = []
        for fp in file_paths:
            true_list.append(self.is_spam(fp))
        print true_list
        if flag == "spam":
            spam_count = true_list.count(True)
            return spam_count / float(len(file_paths))
        if flag == "ham":
            ham_count = true_list.count(False)
            return ham_count / float(len(file_paths))


#sf = SpamFilter("data/train/spam", "data/train/ham")
#print sf.testProb("data/dev/spam","spam")

print log_probs(["data/train/spam/test_file"],1e-5)

