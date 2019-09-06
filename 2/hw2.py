############################################################
# CIS 521: Homework 2
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import math
import random
import copy
############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return math.factorial(n**2)/(math.factorial(n**2-n)*math.factorial(n))

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    col_set = set()
    diagonal_set = set()
    subdiag_set = set()
    for row in range(len(board)):
        col = board[row]
        diagonal = col - row
        subdiag = col + row
        if(col in col_set) or (diagonal in diagonal_set) or (subdiag in subdiag_set):
            return False
        else:
            col_set.add(col)
            diagonal_set.add(diagonal)
            subdiag_set.add(subdiag)
    return True

def n_queens_solutions(n):
    for val in n_queens_helper(n,[]):
        yield val
def n_queens_helper(n, board):
    row = len(board)
    if row == n:
        yield board
    for col in range(n):
        board.append(col)
        if n_queens_valid(board):
            for val in n_queens_helper(n,board):
                yield val
        board.pop()

#print len(list(n_queens_solutions(8)))
############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.nrow = len(board)
        self.mcol = len(board[0])
        self.movement = [[0,0],[1,0],[-1,0],[0,1],[0,-1]]

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        if row >= 0 and row < self.nrow and col >= 0 and col < self.mcol:
            for x in self.movement:
                trow,tcol = row + x[0],col+x[1]
                if trow<0 or tcol<0 or trow == self.nrow or tcol == self.mcol:
                    continue
                self.board[trow][tcol] = not self.board[trow][tcol]

    def scramble(self):
        for i in range(self.nrow):
            for j in range(self.mcol):
                if random.random() < 0.5:
                    self.perform_move(i,j)

    def is_solved(self):
        for row in self.board:
            for elem in row:
                if elem: return False
        return True

    def copy(self):
        new_board = copy.deepcopy(self.board)
        return LightsOutPuzzle(new_board)

    def successors(self):
        for i in range(self.nrow):
            for j in range(self.mcol):
                copy_p = self.copy()
                copy_p.perform_move(i,j)
                yield ((i,j),copy_p)

    def convert2tuple(self):
        board = tuple([tuple(row) for row in self.board])
        return board

    def find_solution(self):
        if self.is_solved():
            return []
        board_set = set()
        board_set.add(self.convert2tuple())
        head,tail = 0,0
        queue = [[(-1,-1),self.copy(),-1]]
        is_Solve = False
        # use bfs to solve the problem
        while(tail<=head):
            p = queue[tail][1]
            for move,new_p in p.successors():
                board = new_p.convert2tuple()
                if(board not in board_set):
                    board_set.add(board)
                    head+=1
                    queue.append([move,new_p,tail])
                if new_p.is_solved():
                    is_Solve = True
                    break
            tail+=1
            if is_Solve:
                break
        if is_Solve == False:
            return None
        # trace back to output the queue of the move
        sequence = []
        parent = head
        while True:
            if parent == 0:
                return list(reversed(sequence))
            sequence.append(queue[parent][0])
            parent = queue[parent][2]


def create_puzzle(rows, cols):
    board = [([False for j in range(cols)])for i in range(rows)]
    return LightsOutPuzzle(board)

############################################################
# Section 3: Linear Disk Movement
############################################################
class LinearDisk(object):
    def __init__(self,cells,n):
        self.cells = cells
        self.length = len(cells)
        self.n=n

    def get_cells(self):
        return self.cells

    def perform_move(self,i,j):
        if i>=0 and i<self.length and j>=0 and j<self.length:
            self.cells[i],self.cells[j] = self.cells[j],self.cells[i]

    def is_solved(self):
        for i in range(self.n):
            if self.cells[self.length-i-1] == False:
                return False
        return True

    def check_order(self):
        for i in range(self.n):
            if self.cells[self.length-i-1] > (i+1):
                return False
        return True

    def copy(self):
        new_cells = copy.deepcopy(self.cells)
        return LinearDisk(new_cells,self.n)

    def successors(self):
        c=self.cells
        l=self.length
        for i in range(l):
            if c[i]==True and i<l-1:
                if c[i+1]==False:
                    copy_c = self.copy()
                    copy_c.perform_move(i,i+1)
                    yield ((i,i+1),copy_c)
            if c[i]== True  and i<l-2:
                if c[i+1]== True and c[i+2]== False:
                    copy_c = self.copy()
                    copy_c.perform_move(i,i+2)
                    yield ((i,i+2),copy_c)


def solve_identical_disks(length, n):
    c = [True for i in range(n)]+[False for j in range(n,length)]
    disk = LinearDisk(c,n)
    if disk.is_solved():
        return []
    cells_set = set()
    cells_set.add(tuple(elem for elem in disk.get_cells()))
    tail,head = 0,0
    queue = [[(0,0),disk.copy(),-1]]
    is_solved = False
    while tail <= head:
        p = queue[tail][1]
        for move,new_p in p.successors():
            cells = tuple(elem for elem in new_p.get_cells())
            if cells not in cells_set:
                cells_set.add(cells)
                head+=1
                queue.append([move,new_p,tail])
                if new_p.is_solved():
                    is_solved = True
                    break
        tail+=1
        if is_solved:
            break
    if not is_solved:
        return None
    # find the path
    path = []
    parent = head
    while True:
        if parent == 0:
            print list(reversed(path))
            break
        path.append(queue[parent][0])
        parent = queue[parent][2]

class LinearDisk2(object):
    def __init__(self,cells,n):
        self.cells = cells
        self.length = len(cells)
        self.n=n

    def get_cells(self):
        return self.cells

    def perform_move(self,i,j):
        if i>=0 and i<self.length and j>=0 and j<self.length:
            self.cells[i],self.cells[j] = self.cells[j],self.cells[i]

    def is_solved(self):
        for i in range(self.n):
            if self.cells[self.length-i-1] != i:
                return False
        return True

    def check_order(self):
        for i in range(self.n):
            if self.cells[self.length-i-1] > i:
                return False
        return True

    def copy(self):
        new_cells = copy.deepcopy(self.cells)
        return LinearDisk2(new_cells,self.n)

    def successors(self):
        c=self.cells
        l=self.length
        for i in range(l):
            if c[i] >= 0:
                if i < l-1:
                    if c[i+1] < 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i+1)
                        yield ((i,i+1),copy_c)
                if i < l-2:
                    if c[i+2] < 0 and c[i+1] >= 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i +2)
                        yield ((i,i+2),copy_c)
                if i>=1:
                    if c[i-1] < 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i-1)
                        yield ((i,i-1),copy_c)
                if i>=2:
                    if c[i-2] < 0 and c[i-1] >= 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i-2)
                        yield ((i,i-2),copy_c)

def solve_distinct_disks(length, n):
    c = [i for i in range(n)]+[-1 for j in range(n,length)]
    disk = LinearDisk2(c,n)
    if disk.is_solved():
        return []
    cells_set = set()
    cells_set.add(tuple(elem for elem in disk.get_cells()))
    tail,head = 0,0
    queue = [[(0,0),disk.copy(),-1]]
    is_solved = False
    while tail <= head:
        p = queue[tail][1]
        for move,new_p in p.successors():
            cells = tuple(elem for elem in new_p.get_cells())
            if cells not in cells_set:
                #if new_p.check_order():
                    cells_set.add(cells)
                    head+=1
                    queue.append([move,new_p,tail])
                    if new_p.is_solved():
                        is_solved = True
                        break
        tail+=1
        if is_solved:
            break
    if not is_solved:
        return None
    # find the path
    path = []
    parent = head
    while True:
        if parent == 0:
            print list(reversed(path))
            break
        path.append(queue[parent][0])
        parent = queue[parent][2]

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
about 3 days
"""

feedback_question_2 = """
The debug part of the 3rd question is the hardest, I treat 0 as True initially
and I missuse elif ratherthan if, here is something I learn from this process:
use same data type to represent False is better, for example, -1
"""

feedback_question_3 = """
I really like the algorithm and guide in the second question,leed me to a good
solution
"""
