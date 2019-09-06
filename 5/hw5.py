############################################################
# CIS 521: Homework 5
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
from os import listdir
import time
from os.path import isfile,join
############################################################
# Section 1: Spam Filter
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
        for w in tokens:
            if w in count_dict:
                count_dict[w]+=1
            else:
                count_dict[w]=1
    #for each word in vocabulary,calculate the probabilty of occurance
    #add the laplace-smoothed log probabilities to prob_dict
    count_sum = len(tokens_list)
    V = len(count_dict)
    for word in count_dict:
        count = count_dict[word]
        pw = (count+alpha)/(count_sum+alpha*(V+1))
        prob_dict[word] = math.log(pw)
    #add unkown tokens unk to prob_dict
    prob_dict["<UNK>"]=math.log(alpha/(count_sum+alpha*(V+1)))
    return prob_dict

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_files = [f for f in listdir(spam_dir)]
        ham_files = [f for f in listdir(ham_dir)]
        spam_paths = [spam_dir+"/"+fname for fname in spam_files]
        ham_paths = [ham_dir+"/"+fname for fname in ham_files]
        # spam_paths = [spam_dir+"/spam%d" %i for i in range(1,1010)]
        # ham_paths = [ham_dir+"/ham%d" %i for i in range(1,1010)]
        self.spam_dict = log_probs(spam_paths,smoothing)
        self.ham_dict = log_probs(ham_paths,smoothing)
        self.p_spam = len(spam_files)/float(len(spam_files)+len(ham_files))
        self.p_ham = len(ham_files)/float(len(spam_files)+len(ham_files))
        # self.p_spam = len(spam_paths)/float(len(spam_paths)+len(ham_paths))
        # self.p_ham = len(ham_paths)/float(len(spam_paths)+len(ham_paths))

    def is_spam(self, email_path):
        tokens = load_tokens(email_path)
        ps = self.p_spam
        ph = self.p_ham
        for w in tokens:
            if w in self.spam_dict:
                ps+=self.spam_dict[w]
            else:
                ps+=self.spam_dict["<UNK>"]
            if w in self.ham_dict:
                ph+=self.ham_dict[w]
            else:
                ph+=self.ham_dict["<UNK>"]
        if(ps>ph):
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        d = {}
        for word in self.spam_dict:
            if word in self.ham_dict:
                pw = math.exp(self.spam_dict[word])*self.p_spam + math.exp(self.ham_dict[word])*self.p_ham
                d[word] = self.spam_dict[word]-math.log(pw)
            # else:
            #     pw = math.exp(self.spam_dict[word])*self.p_spam + math.exp(self.ham_dict["<UNK>"])*self.p_ham
        sorted_list = sorted(d,key=d.__getitem__,reverse=True)
        return [sorted_list[i] for i in range(n)]

    def most_indicative_ham(self, n):
        d = {}
        for word in self.ham_dict:
            if word in self.spam_dict:
                pw = math.exp(self.spam_dict[word])*self.p_spam + math.exp(self.ham_dict[word])*self.p_ham
                d[word] = self.ham_dict[word]-math.log(pw)
            # else:
            #     pw = math.exp(self.spam_dict["<UNK>"])*self.p_spam + math.exp(self.ham_dict[word])*self.p_ham
        sorted_list = sorted(d,key=d.__getitem__,reverse=True)
        return [sorted_list[i] for i in range(n)]

    def testProb(self,dir_path,flag):
        files = [f for f in listdir(dir_path)]
        file_paths = [dir_path+"/"+fname for fname in files]
        true_list = []
        for fp in file_paths:
            true_list.append(self.is_spam(fp))
        if flag=="spam":
            spam_count = true_list.count(True)
            return spam_count/float(len(file_paths))
        if flag=="ham":
            ham_count = true_list.count(False)
            return ham_count/float(len(file_paths))

sf = SpamFilter("data/train/spam", "data/train/ham",1e-5)
print sf.testProb("data/dev/spam","spam")

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
about 12 hours
"""

feedback_question_2 = """
Understanding the algorithm of calculating probability
"""

feedback_question_3 = """
The spam filter is very intersting
"""