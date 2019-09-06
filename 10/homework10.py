############################################################
# CIS 521: Homework 10
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    def __eq__(self, other):
        pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __eq__(self, other):
        pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass
        
class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    def __eq__(self, other):
        pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    def __eq__(self, other):
        pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __eq__(self, other):
        pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __eq__(self, other):
        pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

def satisfying_assignments(expr):
    pass

class KnowledgeBase(object):
    def __init__(self):
        pass
    def get_facts(self):
        pass
    def tell(self, expr):
        pass
    def ask(self, expr):
        pass

############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()

# Write an Expr for each query that should be asked of the knowledge base
mythical_query = None
magical_query = None
horned_query = None

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = None
is_magical = None
is_horned = None

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
party_constraints = None

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = None

# Write your answer to the question in the assignment
puzzle_2_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
# guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
