############################################################
# CIS 521: Homework 8
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math


############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    infile = open(path)
    sentence_list =[]
    for lines in infile:
        line_tokens = []
        sentence = lines.split()
        for str in sentence:
            tokens = str.split("=")
            line_tokens.append((tokens[0],tokens[1]))
        sentence_list.append(line_tokens)
    return sentence_list

class Tagger(object):

    def __init__(self, sentences):
        alpha = 1e-3
        pi_count_dict = {}
        pi = {}
        a_count_dict = {}
        a = {}
        b_count_dict = {}
        b={}
        for s in sentences:
            if s[0][1] in pi_count_dict:
                pi_count_dict[s[0][1]]+=1
            else:
                pi_count_dict[s[0][1]]=1
            for i in range(len(s)):
                if i != len(s)-1:
                    if s[i][1] in a_count_dict:
                        if s[i+1][1] in a_count_dict[s[i][1]]:
                            a_count_dict[s[i][1]][s[i+1][1]]+=1
                        else:
                            a_count_dict[s[i][1]][s[i+1][1]]=1
                    else:
                        a_count_dict[s[i][1]] = {}
                        a_count_dict[s[i][1]][s[i+1][1]]=1
                if s[i][1] in b_count_dict:
                    if s[i][0] in b_count_dict[s[i][1]]:
                        b_count_dict[s[i][1]][s[i][0]]+=1
                    else:
                        b_count_dict[s[i][1]][s[i][0]]=1
                else:
                    b_count_dict[s[i][1]] = {}
                    b_count_dict[s[i][1]][s[i][0]]=1
        l = len(sentences)
        V_itag = len(pi_count_dict)
        for init_tag in pi_count_dict:
            tag_count = pi_count_dict[init_tag]
            p_itag = (tag_count + alpha) / (l + alpha * (V_itag + 1))
            pi[init_tag] = math.log(p_itag)
        pi["<UNK>"] = math.log(alpha / (l + alpha * (V_itag + 1)))

        for pre_tag in a_count_dict:
            a[pre_tag]={}
            post_tags = a_count_dict[pre_tag]
            V_post_dict = len(post_tags)
            sum_post_tags = sum(post_tags.itervalues())
            for post_tag in post_tags:
                post_tag_count = post_tags[post_tag]
                p_post_tag = (post_tag_count+alpha)/(sum_post_tags+alpha*(V_post_dict+1))
                a[pre_tag][post_tag]=math.log(p_post_tag)
            a[pre_tag]["<UNK>"]=math.log(alpha/(sum_post_tags+alpha*(V_post_dict+1)))

        for tag in b_count_dict:
            b[tag]={}
            word_dict = b_count_dict[tag]
            V_word = len(word_dict)
            sum_word = sum(word_dict.itervalues())
            for word in word_dict:
                word_count = word_dict[word]
                pw = (word_count+alpha)/(sum_word+alpha*(V_word+1))
                b[tag][word] = math.log(pw)
            b[tag]["<UNK>"]=math.log(alpha/(sum_word+alpha*(V_word+1)))
        self.pi = pi
        self.a = a
        self.b = b
        self.states = b.keys()

    def most_probable_tags(self, tokens):
        max_tags = []
        for token in tokens:
            max_prob = -99999
            max_tag = "<START>"
            for tag in self.b:
                if token in self.b[tag]:
                    tag_prob = self.b[tag][token]
                else:
                    tag_prob = self.b[tag]["<UNK>"]
                if tag_prob > max_prob:
                    max_prob = tag_prob
                    max_tag = tag
            max_tags.append(max_tag)
        return max_tags

    def viterbi_tags(self, tokens):
        V = [{}]
        #initialization
        for i in self.states:
            if tokens[0] in self.b[i]:
                V[0][i] = self.pi[i] + self.b[i][tokens[0]]
            else:
                V[0][i] = self.pi[i] + self.b[i]["<UNK>"]
        # Run Viterbi forward algorithm when t>0
        for t in range(1,len(tokens)):
            V.append({})
            for y in self.states:
                if tokens[t] in self.b[y]:
                    prob = max(V[t-1][y0]+self.a[y0][y]+self.b[y][tokens[t]] for y0 in self.states)
                else:
                    prob = max(V[t-1][y0]+self.a[y0][y]+self.b[y]["<UNK>"] for y0 in self.states)
                V[t][y] = prob
        # Find the optimized path by backpointers
        opt=[]
        for j in V:
            for x,y in j.items():
                if j[x]==max(j.values()):
                    opt.append(x)
        return opt



############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
About 8 hours
"""

feedback_question_2 = """
The understanding of viterbi algorithm
"""

feedback_question_3 = """
The implementation of the HMM
"""