from tkinter import Tk, Label, Canvas, messagebox
import numpy as np
import random
import time

start_time = time.time()

class Sudoku_solver(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        frame = Sudoku_grid(self)
        frame.pack()


class Sudoku_grid(Canvas):
    def __init__(self,parent):
        Canvas.__init__(self,parent, width=497, height=497)
        self.parent = parent

        self.sudoku = Sudoku()
        self.sudoku.generate()

        self.create_line(166,0,166,500,width=5)
        self.create_line(166*2,0,166*2,500,width=5)
        self.create_line(0,166,500,166,width=5)
        self.create_line(0,166*2,500,166*2,width=5)

        self.positions = [[0 for i in range(9)] for j in range(9)]
        self.numbers = [[0 for i in range(9)] for j in range(9)]

        self.bg = 'white'
        self.marker_c = 'yellow'
        self.fixed_c = 'black'
        self.dynamic_c = 'brown'

        for k in range(3):
            for l in range(3):
                for i in range(3):
                    for j in range(3):
                        self.positions[k*3+i][l*3+j] = (167*k+i*55, 167*l+j*55, 167*k+(i+1)*55, 167*l+(j+1)*55)
                        a = self.positions[k*3+i][l*3+j]
                        self.create_rectangle(a[0],a[1],a[2],a[3],fill=self.bg)

        for i in range(9):
            for j in range(9):
                if self.sudoku.sudoku[i][j] != 0:
                    self.numbers[i][j] = Label(self,text=self.sudoku.sudoku[i][j],fg=self.fixed_c,font=('ariel',26),background=self.bg)
                    self.numbers[i][j].place(x=self.positions[i][j][0]+15,y=self.positions[i][j][1]+7)

        # print(np.matrix(self.sudoku.sudoku))

        self.focus_set()
        self.bind('<Key>',lambda event: self.write(event))
        self.bind('<Left>',lambda event: self.left())
        self.bind('<Right>',lambda event: self.right())
        self.bind('<Up>',lambda event: self.up())
        self.bind('<Down>',lambda event: self.down())
        self.bind('<BackSpace>',lambda event: self.delete())
        self.bind('<Button-1>',lambda event: self.click(event))

        self.marker = [[0,0],[0,0]]
        self.refresh()

    def refresh(self):
        y = self.positions[self.marker[0][0]][self.marker[0][1]]
        self.create_rectangle(y[0],y[1],y[2],y[3],fill=self.bg)
        x = self.positions[self.marker[1][0]][self.marker[1][1]]
        self.create_rectangle(x[0],x[1],x[2],x[3],fill=self.marker_c)

        if self.numbers[self.marker[0][0]][self.marker[0][1]] != 0:
            self.numbers[self.marker[0][0]][self.marker[0][1]]['background'] = self.bg
        if self.numbers[self.marker[1][0]][self.marker[1][1]] != 0:
            self.numbers[self.marker[1][0]][self.marker[1][1]]['background'] = self.marker_c
        # if self.marker == [[7,8],[8,8]]:
            # print(np.matrix(self.sudoku.sudoku))
            # self.sudoku.solve()
            # print(np.matrix(self.sudoku.sudoku))

    def write(self,event):
        a = self.marker[1][0]
        b = self.marker[1][1]
        if event.char.isnumeric() and event.char != '0':
            if self.numbers[a][b] != 0:
                if self.numbers[a][b]['fg'] != self.fixed_c:
                    if event.char == self.numbers[a][b]['text']:
                        self.delete()
                    else:
                        self.numbers[a][b].destroy()
                        self.numbers[a][b] = Label(self,text=event.char,fg=self.dynamic_c,font=('ariel',26),background=self.marker_c)
                        self.numbers[a][b].place(x=self.positions[a][b][0]+15,y=self.positions[a][b][1]+7)
                        self.sudoku.sudoku[a][b] = self.numbers[a][b]['text']
            else:
                self.numbers[a][b] = Label(self,text=event.char,fg=self.dynamic_c,font=('ariel',26),background=self.marker_c)
                self.numbers[a][b].place(x=self.positions[a][b][0]+15,y=self.positions[a][b][1]+7)
                self.sudoku.sudoku[a][b] = self.numbers[a][b]['text']
            self.checkwin()

        elif event.char == 'w':
            self.up()
        elif event.char == 's':
            self.down()
        elif event.char == 'a':
            self.left()
        elif event.char == 'd':
            self.right()
        else:
            pass

    def left(self):
        x = (self.marker[1][0],self.marker[1][1])
        self.marker[0] = [x[0],x[1]]
        self.marker[1][0]-= 1 if self.marker[1][0]-1 in range(9) else 0
        self.refresh()
    def right(self):
        x = (self.marker[1][0],self.marker[1][1])
        self.marker[0] = [x[0],x[1]]
        self.marker[1][0]+=1 if self.marker[1][0]+1 in range(9) else 0
        self.refresh()
    def up(self):
        x = (self.marker[1][0],self.marker[1][1])
        self.marker[0] = [x[0],x[1]]
        self.marker[1][1]-=1 if self.marker[1][1]-1 in range(9) else 0
        self.refresh()
    def down(self):
        x = (self.marker[1][0],self.marker[1][1])
        self.marker[0] = [x[0],x[1]]
        self.marker[1][1]+=1 if self.marker[1][1]+1 in range(9) else 0
        self.refresh()

    def click(self,event):
        x = (self.marker[1][0],self.marker[1][1])
        self.marker[0] = [x[0],x[1]]
        a,b = event.x//167,event.y//167
        c,d = event.x%167,event.y%167
        self.marker[1] = [a*3+c//55,b*3+d//55]
        self.refresh()

    def delete(self):
        if self.numbers[self.marker[1][0]][self.marker[1][1]] != 0 and self.numbers[self.marker[1][0]][self.marker[1][1]]['fg'] != self.fixed_c:
            self.numbers[self.marker[1][0]][self.marker[1][1]].destroy()
            self.numbers[self.marker[1][0]][self.marker[1][1]] = 0
            self.sudoku.sudoku[self.marker[1][0]][self.marker[1][1]] = 0

    def checkwin(self):
        flag = 1
        for i in range(9):
            if 0 in self.numbers[i]:
                flag = 0
                break
        if flag:
            flag = 1 if self.sudoku.checkwin() else 0
        if flag:
            messagebox.showinfo('yay','You Win')

class Sudoku():
    def __init__(self):
        self.yes = 0
        self.sudoku = [[0 for i in range(9)] for j in range(9)]
        '''self.sudoku = [
            [0,0,0,2,6,0,7,0,1],
            [6,0,0,0,7,0,0,9,0],
            [1,9,0,0,0,4,5,0,0],
            [8,2,0,1,0,0,0,4,0],
            [0,0,4,6,0,2,9,0,0],
            [0,5,0,0,0,3,0,2,8],
            [0,0,9,3,0,0,0,0,4],
            [0,0,0,0,0,0,0,3,6],
            [7,0,3,0,1,8,0,0,0]
        ]'''

    def check(self,r,c,n):
        for i in range(9):
            if self.sudoku[i][c] == n and i != r:
                return False
        for i in range(9):
            if self.sudoku[r][i] == n and i != c:
                return False
        for i in range(3):
            for j in range(3):
                if (r//3)*3+i != r and (c//3)*3+j != c:
                    if self.sudoku[(r//3)*3+i][(c//3)*3+j] == n:
                        return False
        return True

    def solve(self):
        def insolve():
            for i in range(9):
                for j in range(9):
                    if self.sudoku[i][j] == 0:
                        for k in range(1,10):
                            if self.check(i,j,k):
                                self.sudoku[i][j] = k
                                insolve()
                                print(i,j)
                                self.sudoku[i][j] = 0
                        return
            1/0

        try:
            insolve()
        except:
            return

    def generate_full(self):
        a = 16
        while a>0:
            q = random.randint(0,8)
            w = random.randint(0,8)
            e = random.randint(1,9)
            if self.check(q,w,e) and self.sudoku[q][w] == 0:
                self.sudoku[q][w] = e
                a -= 1
        self.solve()

    def generate(self):
        self.generate_full()
        q = 10
        while q>0:
            a = random.randint(0,8)
            b = random.randint(0,8)
            if self.sudoku[a][b] != 0:
                self.sudoku[a][b] = 0
                q-=1

    def checkwin(self):
        a = 1
        for i in range(9):
            for j in range(9):
                if not self.check(i,j,self.sudoku[i][j]):
                    a = 0
        return a


if __name__ == '__main__':
    a = Sudoku_solver()
    a.mainloop()
    print('---{} seconds---'.format(time.time()-start_time))

