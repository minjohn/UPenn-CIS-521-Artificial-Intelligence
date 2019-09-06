############################################################
# CIS 521: Homework 4
############################################################

student_name = "Zhimin Zhao"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
#import time
#import timeit

############################################################
# Section 1: Sudoku
############################################################


def read_board(path):
    scene = []
    with open(path) as infile:
        for row, line in enumerate(infile, start=1):
            scene.append([])
            for col, char in enumerate(line.strip(), start=1):
                if char == "*":
                    scene[-1].append('0')
                elif char > 0:
                    scene[-1].append(char)
                else:
                    print ("Unrecognized character '%s' at line %d, column %d" %
                        (char, row, col))
                    #return None
    if len(scene) < 1:
        print "Scene must have at least one row"
        return None
    if len(scene[0]) < 1:
        print "Scene must have at least one column"
        return None
    if not all(len(row) == len(scene[0]) for row in scene):
        print "Not all rows are of equal length"
        return None

    return scene


def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cells.append((i, j))
    return cells

    # 1 line
    #  [00,01][00,02][00,03][00,04]...[00,07][00,08](72)
    #  [01,00][01,02][01,03][01,04]...[01,07][01,08]
    #   ...
    #  [08,00][08,01][08,02][08,03]...[08,06][08,07]

    # 2   row:
    #     [00,10][00,20][00,30]...[00,70][00,80](72)
    #     [10,00][10,20][10,30]...[10,70][10,80]
    #     [20,00][20,10][20,30]...[20,70][20,80]
    #     ...
    #     [80,00][80,10][80,30]...[80,60][80,70]
def sudoku_arcs():
    arcs=set()
    # line:rows:
    for i in range(9):
        for j in range(9):
             for k in range(9):
                 if k!=j:
                    arc1=((i,j),(i,k))
                    arc2=((j,i),(k,i))
                    arcs.add(arc1)
                    arcs.add(arc2)
    # in the nine cubes
    for i in range(9):
        for j in range(9):
            for k1 in range(3):
                for k2 in range(3):
                    x1=int(i/3)*3+k1
                    y1=int(j/3)*3+k2
                    if i !=x1 or j != y1:
                        arc3=((i,j),(x1,y1))
                        arcs.add(arc3)
    return arcs


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board=board
        self.board_map={}
        #self.confirm_map={}
        self.confirm=0
        #self.record_list=[]
        #self.record_map={}

        for i in range(9):
            for j in range(9):
                _char = board[i][j]
                if _char == '0':
                    self.board_map.update({(i, j): self.turn_1_tuple(range(1,10))})
                else:
                    tp = set()
                    tp.add(int(_char))
                    self.board_map.update({(i, j): tp})
                    self.confirm+=1

    def copy(self):
        map = {i:self.board_map[i] for i in self.board_map}
        s=Sudoku(self.board)
        s.board_map=map
        #s.confirm=self.confirm
        return s
    def turn_1_tuple(self, a):
        result=set()
        for item in a:
            result.add(item)
        return result

    def get_values(self, cell):

        return self.board_map[cell]

    def find_neighbor(self,cell):
        neighbor=set()
        for row in range(9):
            if row != cell[0]:
                neighbor.add((row,cell[1]))
        for col in range(9):
            if col != cell[1]:
                neighbor.add((cell[0],col))
        for ci in range(3):
            for cj in range(3):
                x1=int(cell[0]/3)*3+ci
                y1=int(cell[1]/3)*3+cj
                if x1!=cell[0] or y1!=cell[1]:
                    #a=(int(cell[0]/3)*3+ci,int(cell[1]/3)*3+cj)
                    neighbor.add((x1,y1))
        return neighbor

    def is_solves(self):
        for i in range(9):
            for j in range(9):
                if len(self.get_values((i,j))) > 1:
                    return False
        return True

    def remove_inconsistent_values(self, cell1, cell2):
        tp1 = self.get_values(cell1)
        tp2 = self.get_values(cell2)
        _result = set()
        #if len(tp1) == 1:
        #    return False

        a = list(tp2)[0]
        for i in tp1:
            if i != a:
                _result.add(i)
        if len(_result):
            self.board_map.update({cell1: _result})
            if len(_result)==1:
                self.confirm+=1
            return True
        return False

    def infer_ac3(self):
        que = []
        for arc in self.ARCS:
            que.append(arc)
        while que:
            arc = que.pop()
            if len(self.board_map[arc[0]])>1 and len(self.board_map[arc[1]])==1:
                if self.remove_inconsistent_values(arc[0], arc[1]):
                    #if len(self.board_map[arc[0]])==1:#??????????????????????
                        #self.ARCS.pop()#??????????????????????????????
                    for Xk in self.find_neighbor(arc[0]):
                        que.append((Xk, arc[0]))
        return 1


    def find_cell_neighbor_in_cube(self,cell):

        if len(self.board_map[cell]) == 1:
            return False
        neighbor = set()
        for ci in range(3):
            for cj in range(3):
                x1 = int(cell[0]/3)*3+ci
                x2 = int(cell[1]/3)*3+cj
                if x1 == cell[0] and x2 == cell[1]:
                    continue
                else:
                    a = (x1, x2)
                    it = self.board_map[a]
                    if len(it) == 1:
                        continue
                    for ttt in it:
                        neighbor.add(ttt)
        if len(neighbor) == 9:
            return False
        for itm in self.board_map[cell]:
            if itm in neighbor:
                continue
            else:
                return itm
        return False

    def find_cell_neighbor_in_row(self, cell):
        if len(self.board_map[cell]) == 1:
            return False
        neighbor = set()
        for i in range(9):
                if i != cell[1]:
                    it = self.board_map[(cell[0], i)]
                    if len(it)==1:
                        return False
                    for ttt in it:
                            neighbor.add(ttt)
        if len(neighbor) == 9:
            return False
        for itm in self.board_map[cell]:
            if itm not in neighbor:
                return itm
        return False

    def find_cell_neighbor_in_col(self, cell):
        if len(self.board_map[cell]) == 1:
            return False
        neighbor = set()
        for i in range(9):
                if i != cell[0]:
                    it = self.board_map[(i, cell[1])]
                    if len(it)==1:
                        return False
                    for ttt in it:
                            neighbor.add(ttt)
        if len(neighbor) == 9:
            return False
        for itm in self.board_map[cell]:
            if itm not in neighbor:
                return itm
        return False

    def set_store(self):
        return {1:[0],2:[0],3:[0],4:[0],5:[0],6:[0],7:[0],8:[0],9:[0]}

    def update_cell_0(self):
        changed=False
        store=self.set_store()
        for i in range(3):
            for j in range(3):

                for ci in range(3):
                    for cj in range(3):
                        cell=(i*3+ci,j*3+cj)
                        if len(self.board_map[cell]) == 1:
                            continue
                        else:
                            key=self.board_map[cell]
                            for every_key in key:
                                store[every_key][0]+=1
                                store[every_key].append(cell)
                for _key in store.keys():
                    if store[_key][0] == 1:
                        changed = True
                        rst=set()
                        rst.add(_key)
                        c_cell=store[_key][1]
                        self.board_map.update({c_cell:rst})
                        if len(rst)==1:
                            self.confirm+=1
                        break
                store=self.set_store()
        return changed

    def update_cell_1(self):
        changed=False
        store_r=self.set_store()
        for i in range(9):
            for j in range(9):
                cell_r=(i,j)
                if len(self.board_map[cell_r])==1:
                    continue
                else:
                    key_r=self.board_map[cell_r]
                    for every_key_r in key_r:
                        store_r[every_key_r][0]+=1
                        store_r[every_key_r].append(cell_r)
            for _key_r in store_r.keys():
                if store_r[_key_r][0]==1:
                    changed=True
                    rst_r=set()
                    rst_r.add(_key_r)
                    c_cell_r=store_r[_key_r][1]
                    self.board_map.update({c_cell_r:rst_r})
                    if len(rst_r)==1:
                        self.confirm+=1
                    break
            store_r=self.set_store()
        return changed

    def update_cell_2(self):
        changed=False
        store_c=self.set_store()
        for i in range(9):
            for j in range(9):
                cell_c=(j,i)
                if len(self.board_map[cell_c])==1:
                    continue
                else:
                    key_c=self.board_map[cell_c]
                    for every_key_c in key_c:
                        store_c[every_key_c][0]+=1
                        store_c[every_key_c].append(cell_c)
            for _key_c in store_c.keys():
                if store_c[_key_c][0]==1:
                    changed=True
                    rst_c=set()
                    rst_c.add(_key_c)
                    c_cell_c=store_c[_key_c][1]
                    self.board_map.update({c_cell_c:rst_c})
                    if len(rst_c)==1:
                        self.confirm+=1
                    break
            store_c=self.set_store()
        return changed

    def infer_improved(self):
        # check within cube:
        self.infer_ac3()
        #while not self.is_solves():
        while self.confirm<81:

            if self.update_cell_1():
                self.infer_ac3()
            if self.update_cell_2():
                self.infer_ac3()
            if self.update_cell_0():
                self.infer_ac3()

        return 1

    def com_solve(self):
        explored1=[]
        explored2=[]
        count=0
        for i in range(9):
            for j in range(9):
                cell1=(i,j)
                cell2=(j,i)
                value1=self.board_map[cell1]
                value2=self.board_map[cell2]
                if len(value1)==1:
                    count+=1
                    if list(value1)[0] in explored1:
                        return (False,0)
                    else:
                        explored1.append(list(value1)[0])
                if len(value2)==1:

                    if list(value2)[0] in explored2:
                        return (False,0)
                    else:
                        explored2.append(list(value2)[0])
            explored1=[]
            explored2=[]
        explored3=[]
        for i in range(3):
            for j in range(3):
                for ci in range(3):
                    for cj in range(3):
                        cell3=(i*3+ci,j*3+cj)
                        value3= self.board_map[cell3]
                        if len(value3)==1:

                            if list(value3)[0] in explored3:
                                return (False,0)
                            else:
                                explored3.append(list(value3)[0])
                explored3=[]
        return (True,count)




    def pre_deal(self):
        improve_finish= True
        self.infer_ac3()
        while improve_finish:
            a=0
            if self.update_cell_0():
                self.infer_ac3()
                a+=1
            if self.update_cell_1():
                self.infer_ac3()
                a+=1
            if self.update_cell_2():
                self.infer_ac3()
                a += 1
            if a == 0:
                improve_finish = False


    def helper(self,que):

        self.pre_deal()
        s = self.com_solve()
        if s == (True,81):
            return self

        if not self.com_solve()[0]:
            return False

        for i in range(9):
            for j in range(9):
                cell=(i,j)

                if len(self.board_map[cell])>1:
                    f2 = set()
                    fi_set = set()
                    cc=0
                    for _ii in self.board_map[cell]:
                        if not cc:
                            fi_set.add(_ii)
                        else:
                            f2.add(_ii)
                        cc+=1

                 
                    future_board ={i2:self.board_map[i2] for i2 in self.board_map}
                    future_board.update({cell: f2})
            
                    self.board_map.update({cell: fi_set})
             
                    que.append(future_board)
                    result = self.helper(que)
       
                    if result:
                        return True
                        # que0.append(current)
                        # return que0

                    while not result:
                        self.board_map=que.pop()
                        result = self.helper(que)
                        if result:
                             return True
                        #obj=que.pop()
                        #result= obj.helper(que,que0)
                        #if result:
                        #    que0.append(obj)
                        #    return que0


    def infer_with_guessing(self):
        que=[]

        self.helper(que)
        return 1


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
20hours
"""

feedback_question_2 = """
reduce the time.no
"""

feedback_question_3 = """
I like recursion, it is hard to think...
"""