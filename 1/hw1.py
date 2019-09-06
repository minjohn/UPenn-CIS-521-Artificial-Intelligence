############################################################
# CIS 521: Homework 1
############################################################

student_name = "Zhimin Zhao"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is strongly typed, because operations need to be performed 
on objects of the same type. For example, you can only add two integer
together (a = 1, b = 5, c = "apple", d = a + b), but not integer and 
string (e = a + c is not allowed).
Python is dynamically typed, because variables come into existence when
first assigned, its type is also automatically determined by the assigned 
object. For example, code "a = 1" assigns integer 1 to variable a. Another 
line "a = 'apple' " will change variable a's type to string. Besides, 
functions in Python has no type signatures.
"""

python_concepts_question_2 = """
List is unhashable in Python. We can use tuples to represent the 2-D points
code: points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"} 
"""

python_concepts_question_3 = """
For larger inputs, function concatenate2(string) with str.join() is better. 
Because looping takes longer time than str.join() function for large inputs.
"""

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [item for subset in seqs for item in subset]

def transpose(matrix):
    mlen = len(matrix[0])
    result = [[] for i in xrange(mlen)]
    for column in xrange(mlen):
        for row in matrix:
            result[column].append(row[column])
    return result
        
############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    y = seq[:]
    return y

def all_but_last(seq):
    y = seq[:-1]
    return y

def every_other(seq):
    return seq[::2]


############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in xrange(len(seq)+1):
        yield seq[:i]

def suffixes(seq):
    for i in xrange(len(seq)+1):
        yield seq[i:]

def slices(seq):
    for i in xrange(len(seq)+1):
        for j in range(i+1,len(seq)+1):
            yield seq[i:j]


############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    return ' '.join([word.lower() for word in text.split()])

def no_vowels(text):
    for vowel in ['a','e','i','o','u','A','E','I','O','U']:
        text = text.replace(vowel, '')
    return text

def digits_to_words(text):
    d={'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six', \
       '7':'seven','8':'eight','9':'nine','0':'zero'}
    return ' '.join([d[digit] for digit in text if digit in d])

def to_mixed_case(name):
    temp = [word for word in name.split('_') if word]
    name = ' '.join(temp)
    name = name.title()
    name = name[:1].lower() + name[1:]
    return name.replace(" ",'')


############################################################
# Section 6: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        temp = list(self.polynomial)
        for i in xrange(len(temp)):
            (m,n) = temp[i]
            temp[i] = (-m,n)
        return Polynomial(tuple(temp))
        
    def __add__(self, other):
        return Polynomial(self.polynomial + other.polynomial)

    def __sub__(self, other):
        other = -other
        return Polynomial(self.polynomial + other.polynomial)

    def __mul__(self, other):
        result = []
        for pair_in_a in self.polynomial:
            for pair_in_b in other.polynomial:
                (coa,powa) = pair_in_a
                (cob,powb) = pair_in_b
                tempa = coa*cob
                tempb = powa + powb
                result.append((tempa,tempb))  
        return Polynomial(result)

    def __call__(self, x):
        return sum([item[0]*(x**item[1]) for item in self.polynomial])

    def simplify(self):
        temp = self.polynomial
        result = []
        powlist = []
        for i in xrange(len(temp)):
            powa = temp[i][1]
            coea = temp[i][0]
            if (powa not in powlist):
                for j in xrange(i+1,len(temp)):    
                    powb = temp[j][1]
                    coeb = temp[j][0]
                    if(powa == powb):
                        coea += coeb
                powlist.append(powa)
                if(coea!=0):
                    result.append((coea,powa))
        result.sort(key = lambda tup: tup[1],reverse = True)
        self.polynomial = tuple(result)
                 

    def __str__(self):
        polys = self.polynomial
        result = ""
        for i in xrange(len(polys)):
            temp = ""
            coeff = polys[i][0]
            powa = polys[i][1]
            if coeff>= 0:
                signa = '+'
            else:
                signa = '-'
            coeff = abs(coeff)
            if i==0:
                if signa == '-':
                    temp += signa
            else:
                temp += signa + " "
            if coeff!=1: 
                temp += str(abs(coeff))
            else:
                if powa==0:
                    temp += str(abs(coeff))
            if powa == 1:
                temp += 'x'
            elif powa > 1:
                temp += 'x^' + str(powa)
            else:
                temp += ''
            if i!= len(polys)-1:
                temp += ' '
            result += temp
        return result
                

q = Polynomial([(1, 1), (2, 3)])
print str(q) 
print str(q * q) 
print str(-q * q)

############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
About 5 Hours.
"""

feedback_question_2 = """
The simplify and the __str__ function may be the most complicated 
part for me. There were no significant stumbling blocks.
"""

feedback_question_3 = """
This assignment is really good for me to review my Python coding skill.
I think it is good enough!
"""
