############################################################
# CIS 521: Homework 7
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import string
import re
import random
import math
############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    return re.findall(r"[\w]+|["+string.punctuation+"]",text)

def ngrams(n, tokens):
    ngram_list = []
    tokens.append("<END>")
    for i in range(len(tokens)):
        context = ()
        for j in reversed(range(n-1)):
            if i-j > 0:
                context+=(tokens[i-j-1],)
            else:
                context+=("<START>",)
        ngram_list.append((context, tokens[i]))
    return ngram_list

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.counts=[]

    def update(self, sentence):
        tokens = tokenize(sentence)
        self.counts += ngrams(self.n,tokens)

    def prob(self, context, token):
        token_count = 0
        context_count = 0
        for i in range(len(self.counts)):
            if context == self.counts[i][0]:
                context_count+=1
            if (context,token) == self.counts[i]:
                token_count += 1
        return token_count/float(context_count)

    def random_token(self, context):
        T = [self.counts[i][1] for i in range(len(self.counts)) if self.counts[i][0] == context]
        T.sort()
        r = random.random()
        # index = int(math.ceil(r*(len(T)-1)))
        if len(T)!=0:
            index = int(r*len(T))
            if index > len(T)-1:
                index = len(T)-1
            return T[index]
        else:
            return ' '
        # T = []
        # for i in range(len(self.counts)):
        #     if context == self.counts[i][0]:
        #         if self.counts[i][1] not in T:
        #             T.append(self.counts[i][1])
        # T.sort()
        # r=random.random()
        # cdf = 0.0
        # for j in range(len(T)):
        #     cdf += self.prob(context,T[j])
        #     if cdf > r:
        #         return T[j]


    def random_text(self, token_count):
        # context = self.set_starting_context()
        tokens_list = []
        token = ' '
        for i in range(token_count):
            if token == "<END>":
                context = self.set_starting_context()
            else:
                context = self.get_context(tokens_list)
            token = self.random_token(context)
            tokens_list.append(token)
        return ' '.join(tokens_list)

    def get_context(self,tokens_list):
        context = ()
        l = len(tokens_list)
        for j in reversed(range(self.n-1)):
            if l-1-j >=0:
                context +=(tokens_list[l-1-j],)
            else:
                context+=("<START>",)
        return context

    def set_starting_context(self):
        context = ()
        for i in range(self.n-1):
            context += ("<START>",)
        return context

    def perplexity(self, sentence):
        perplexity = 0.0
        tokens = tokenize(sentence)
        test_ngrams = ngrams(self.n,tokens)
        for i in range(len(test_ngrams)):
            perplexity += math.log(1.0/self.prob(test_ngrams[i][0],test_ngrams[i][1]))
        perplexity = math.exp(perplexity)
        return perplexity**(1./len(test_ngrams))

def create_ngram_model(n, path):
    m = NgramModel(n)
    infile = open(path)
    # message = email.message_from_file(infile)
    for lines in infile:
        m.update(lines)
    return m

# ############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
about 8 hours
"""

feedback_question_2 = """
Understanding the concept of ngram model
"""

feedback_question_3 = """
Test the probability and generating the ngram
"""