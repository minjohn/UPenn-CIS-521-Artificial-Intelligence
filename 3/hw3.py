############################################################
# CIS 521: Homework 3
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import Queue

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board=[]
    num = 1
    for i in range(rows):
        board.append([])
        for j in range(cols):
            board[i].append(num)
            num+=1
    board[rows-1][cols-1]=0
    return TilePuzzle(board)

class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.__board = board
        self.__rows = len(board)
        self.__cols = len(board[0])
        self.__depth = 0
        self.__father = None
        self.__move = 'none'
        for i in range(self.__rows):
            for j in range(self.__cols):
                if board[i][j]==0:
                    self.__blank_row = i
                    self.__blank_col = j
                    break
                    break

    def set_move(self,move):
        self.__move = move

    def get_move(self):
        return self.__move

    def set_father(self,father):
        self.__father = father

    def get_father(self):
        return self.__father

    def get_board(self):
        return self.__board

    def update_depth(self):
        self.__depth += 1

    def set_depth(self,depth):
        self.__depth = depth

    def perform_move(self, direction):
        if direction == 'up':
            move = [-1, 0]
        if direction == 'down':
            move = [1, 0]
        if direction == 'left':
            move = [0, -1]
        if direction == 'right':
            move = [0, 1]
        pos = [self.__blank_row + move[0],self.__blank_col + move[1]]
        if (pos[0]<0) or (pos[0]>=self.__rows) or (pos[1]<0) or (pos[1]>=self.__cols):
           return False
        temp = self.__board[pos[0]][pos[1]]
        self.__board[pos[0]][pos[1]] = 0
        self.__board[self.__blank_row][self.__blank_col]=temp
        self.__blank_row = pos[0]
        self.__blank_col = pos[1]
        return True

    def scramble(self, num_moves):
        for i in range(num_moves):
            self.perform_move(random.choice(['up','down','left','right']))

    def is_solved(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if i==self.__rows-1 and j==self.__cols-1:
                    if self.__board[i][j]!= 0:
                        return False
                elif self.__board[i][j]!= i*self.__cols+j+1:
                    return False
        return True

    def copy(self):
        new_board = copy.deepcopy(self.__board)
        p = TilePuzzle(new_board)
        p.set_depth(self.__depth)
        return p

    def get_total_cost(self):
        cost = self.__depth
        for i in range(self.__rows):
            for j in range(self.__cols):
                num = self.__board[i][j]
                goal_row = (num-1)//self.__cols
                goal_col = (num-1)%self.__cols
                manhattan_distance = abs(goal_row-i)+abs(goal_col-j)
                cost+=manhattan_distance
        return cost

    def convert2tuple(self):
        return tuple([tuple(row) for row in self.__board])

    def successors(self):
        for move in ['up','down','left','right']:
            new_p = self.copy()
            if new_p.perform_move(move):
                new_p.set_move(move)
                yield move,new_p

    # Required
    def find_solutions_iddfs(self):
        limit=0
        is_solved = False
        while True:
            for val in self.iddfs_helper(limit,[]):
                if len(val) > 0:
                    is_solved = True
                    yield val
            if is_solved:
                break
            else:
                limit+=1

    def iddfs_helper(self,limit,move):
        if limit == 0:
            if self.is_solved():
                yield move
            else:
                yield[]
        else:
            seq = ['up','left','right','down']
            for i in range(4):
                if self.perform_move(seq[i]):
                    for val in self.iddfs_helper(limit-1,move+[seq[i]]):
                        yield val
                    self.perform_move(seq[3-i])

    # Required
    def find_solution_a_star(self):

        ini_node = self.copy()
        board_set = set()
        open_queue = Queue.PriorityQueue()
        close_list = []
        open_queue.put((ini_node.get_total_cost(),ini_node))
        board_set.add(ini_node.convert2tuple())
        while True:
            father = open_queue.get()[1]
            close_list.append(father)
            board_set.add(father.convert2tuple())
            if father.is_solved():
                break
            for move,child in father.successors():
                if child.convert2tuple() not in board_set:
                    child.set_father(father)
                    child.update_depth()
                    open_queue.put((child.get_total_cost(),child))
        ans = []
        node = father
        while node.get_father() != None:
            ans.append(node.get_move())
            node = node.get_father()
        return list(reversed(ans))


############################################
# Section 2: Grid Navigation
############################################################
class PointObject(object):

    def __init__(self, point, scene):
        self.__prow = point[0]
        self.__pcol = point[1]
        self.__scene = scene
        self.__srow = len(scene)
        self.__scol = len(scene[0])
        self.__father = None
        self.__depth = 0

    def set_father(self,father):
        self.__father = father

    def get_father(self):
        return self.__father

    def get_point(self):
        return (self.__prow,self.__pcol)

    def set_depth(self,depth):
        self.__depth = depth

    def update_depth(self):
        self.__depth+=1

    def perform_move(self, direction):
        if direction == 'up':
            move = [-1,0]
        if direction == 'down':
            move = [1,0]
        if direction == 'left':
            move = [0,-1]
        if direction == 'right':
            move = [0,1]
        if direction == 'up-left':
            move = [-1,-1]
        if direction == 'up-right':
            move = [-1,1]
        if direction == 'down-left':
            move = [1,-1]
        if direction == 'down-right':
            move = [1,1]

        pos = [self.__prow + move[0],self.__pcol + move[1]]

        if (pos[0]<0) or (pos[0]>=self.__srow) or (pos[1]<0) or (pos[1]>=self.__scol):
            return False
        elif self.__scene[pos[0]][pos[1]]:
            return False

        self.__prow = pos[0]
        self.__pcol = pos[1]
        return True

    def is_solved(self, goal):
        if (self.__prow == goal[0])and(self.__pcol == goal[1]):
            return True

    def copy(self):
        point = [self.__prow,self.__pcol]
        # shallow copy, only one scene no need to deepcopy
        p = PointObject(point,self.__scene)
        p.set_depth(self.__depth)
        return p

    def successors(self):
        move_seq = ['up','left','right','down','up-left','up-right','down-left','down-right']
        for move in move_seq:
            p = self.copy()
            if p.perform_move(move):
                yield p

    def get_total_cost(self,goal):
        cost = self.__depth
        if abs(goal[0]-self.__prow)>abs(goal[1]-self.__pcol):
            return cost + abs(goal[1]-self.__pcol)
        else:
            return cost + abs(goal[0]-self.__prow)

def find_path(start, goal, scene):
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None
    ini_node = PointObject(start,scene)
    open_queue = Queue.PriorityQueue()
    close_list = []
    point_set = set()
    open_queue.put((ini_node.get_total_cost(goal),ini_node))
    is_solved = False
    while not open_queue.empty():
        father = open_queue.get()[1]
        close_list.append(father)
        point_set.add(father.get_point())
        if father.is_solved(goal):
            is_solved = True
            break
        for child in father.successors():
            if child.get_point() not in point_set:
                child.set_father(father)
                child.update_depth()
                open_queue.put((child.get_total_cost(goal),child))
    if not is_solved:
        return None
    path=[]
    node = father
    while node != None:
        path.append(node.get_point())
        node = node.get_father()
    return list(reversed(path))

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

class LinearDisk(object):
    def __init__(self,cells,n):
        self.__cells = cells
        self.__length = len(cells)
        self.__n=n
        self.__depth = 0
        self.__father = None
        self.__move = (0,0)

    def update_depth(self):
        self.__depth += 1

    def set_depth(self, depth):
        self.__depth = depth

    def set_move(self,move):
        self.__move = move

    def get_move(self):
        return self.__move

    def get_father(self):
        return self.__father

    def set_father(self, father):
        self.__father = father

    def get_cells(self):
        return self.__cells

    def convert2tuple(self):
        return tuple([elem for elem in self.__cells])

    def perform_move(self,i,j):
        if i>=0 and i<self.__length and j>=0 and j<self.__length:
            self.__cells[i],self.__cells[j] = self.__cells[j],self.__cells[i]

    def is_solved(self):
        for i in range(self.__n):
            if self.__cells[self.__length-i-1] != i:
                return False
        return True

    def check_order(self):
        for i in range(self.__n):
            if self.__cells[self.__length-i-1] > i:
                return False
        return True

    def copy(self):
        new_cells = copy.deepcopy(self.__cells)
        new_LD = LinearDisk(new_cells,self.__n)
        new_LD.set_depth(self.__depth)
        return new_LD

    def get_total_cost(self):
        cost = self.__depth
        for i in range(self.__length):
            number = self.__cells[i]
            if number < 0:
                continue
            #number in final cells
            final_cell = self.__length-number-1
            h = abs(final_cell-i)
            cost+=h
        return cost

    def successors(self):
        c=self.__cells
        l=self.__length
        for i in range(l):
            if c[i] >= 0:
                if i < l-1:
                    if c[i+1] < 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i+1)
                        copy_c.set_move((i,i+1))
                        yield (i,i+1),copy_c
                if i < l-2:
                    if c[i+2] < 0 and c[i+1] >= 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i+2)
                        copy_c.set_move((i,i+2))
                        yield (i,i+2),copy_c
                if i>=1:
                    if c[i-1] < 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i-1)
                        copy_c.set_move((i,i-1))
                        yield (i,i-1),copy_c
                if i>=2:
                    if c[i-2] < 0 and c[i-1] >= 0:
                        copy_c = self.copy()
                        copy_c.perform_move(i,i-2)
                        copy_c.set_move((i,i-2))
                        yield (i,i-2),copy_c

def solve_distinct_disks(length, n):

    cell = [i for i in range(n)]+[-1 for j in range(n,length)]
    disk = LinearDisk(cell,n)

    open_queue = Queue.PriorityQueue()
    close_list = []
    cell_set = set()
    open_queue.put((disk.get_total_cost(),disk))
    is_solved = False

    while not open_queue.empty():
        father = open_queue.get()[1]
        close_list.append(father)
        cell_set.add(father.convert2tuple())
        if father.is_solved():
            is_solved = True
            break
        for move,child in father.successors():
            if child.convert2tuple() not in cell_set:
                cell_set.add(child.convert2tuple)
                child.set_father(father)
                child.update_depth()
                open_queue.put((child.get_total_cost(),child))

    if is_solved == False:
        return None
    ans = []
    node = father
    while node.get_father() != None:
        ans.append(node.get_move())
        node = node.get_father()
    return list(reversed(ans))

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board =  [([False for i in range(cols)])for j in range(rows)]
    return DominoesGame(board)

class DominoesGame(object):
    MAX_LEVEL = True
    MIN_LEVEL = False
    INFINITY = 99999
    NUMBERFLAG = 314159
    # Required
    def __init__(self, board):
        self.__board = board
        self.__nrow = len(board)
        self.__ncol = len(board[0])

    def get_board(self):
        return self.__board

    def reset(self):
        for row in range(self.__nrow):
            for col in range(self.__nrow):
                self.__board[row][col] = False

    def is_legal_move(self, row, col, vertical):
        if (row < 0) or (row >= self.__nrow):
            return False
        if (col < 0) or (col >= self.__ncol):
            return False
        if vertical:
            if row + 1 >= self.__nrow:
                return False
            if self.__board[row][col] or self.__board[row+1][col]:
                return False
        else:
            if col + 1 >= self.__ncol:
                return False
            if self.__board[row][col] or self.__board[row][col+1]:
                return False
        return True

    def legal_moves(self, vertical):
        for row in range(self.__nrow):
            for col in range(self.__ncol):
                if self.is_legal_move(row,col,vertical):
                    yield (row,col)

    def perform_move(self, row, col, vertical):
        if vertical:
            self.__board[row][col] = True
            self.__board[row+1][col] = True
        else:
            self.__board[row][col] =True
            self.__board[row][col+1] = True

    def game_over(self, vertical):
        for row in range(self.__nrow):
            for col in range(self.__ncol):
                if self.is_legal_move(row,col,vertical):
                    return False
        return True

    def copy(self):
        board = copy.deepcopy(self.__board)
        return DominoesGame(board)

    def successors(self, vertical):
        for move0 in self.legal_moves(vertical):
            node = self.copy()
            node.perform_move(move0[0],move0[1],vertical)
            yield move0,node

    def number_legal_moves(self,vertical):
        count = 0
        for row in range(self.__nrow):
            for col in range(self.__ncol):
                if self.is_legal_move(row,col,vertical):
                   count += 1
        return count


    def get_random_move(self, vertical):
        pass

    def dfs(self,vertical,level,limit,lower_bound,upper_bound):
        # return type is the grade
        if (limit <= 0) or (self.game_over(vertical)):
            if level == self.MAX_LEVEL:
               return self.number_legal_moves(vertical) - self.number_legal_moves(not vertical),1
            else:
               return self.number_legal_moves(not vertical) - self.number_legal_moves(vertical),1

        #initialization
        leaves_count = 0
        for move,node in self.successors(vertical):
            score,n_leves = node.dfs(not vertical,not level,limit -1,lower_bound,upper_bound)
            leaves_count += n_leves
            # means the search is terminated at the last level
            if score == self.NUMBERFLAG:
                continue
            if level == self.MAX_LEVEL:
                if score >= upper_bound:
                    return self.NUMBERFLAG,leaves_count
                if score > lower_bound:
                    lower_bound = score
            if level == self.MIN_LEVEL:
                if score <= lower_bound:
                   return self.NUMBERFLAG,leaves_count
                if score < upper_bound:
                    upper_bound = score
        if level == self.MAX_LEVEL:
            return lower_bound,leaves_count
        else:
            return upper_bound,leaves_count

    # Required
    def get_best_move(self, vertical, limit):
        max_score = - self.INFINITY
        move = None
        leaf_count = 0
        for move0,node in self.successors(vertical):
            value,n_leaf= node.dfs(not vertical,self.MIN_LEVEL,limit-1, max_score,self.INFINITY)
            leaf_count += n_leaf
            if value == self.NUMBERFLAG:
                continue
            if value > max_score:
                max_score = value
                move = move0
        return (move,max_score,leaf_count)


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
3 days
"""

feedback_question_2 = """
A* algorithm
"""

feedback_question_3 = """
I like the practice question 2 and 3
"""