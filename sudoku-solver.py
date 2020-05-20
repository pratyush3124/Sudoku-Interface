from tkinter import *
import numpy as np
import random

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
        self.fixed_c = 'brown'
        self.dynamic_c = 'black'

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

    def write(self,event):
        if event.char.isnumeric() and event.char != '0':
            a = self.marker[1][0]
            b = self.marker[1][1]
            if self.numbers[a][b] != 0:
                if self.numbers[a][b]['fg'] != self.fixed_c:
                    self.numbers[a][b].destroy()
                    self.numbers[a][b] = Label(self,text=event.char,fg=self.dynamic_c,font=('ariel',26),background=self.marker_c)
                    self.numbers[a][b].place(x=self.positions[a][b][0]+15,y=self.positions[a][b][1]+7)
            else:
                self.numbers[a][b] = Label(self,text=event.char,fg=self.dynamic_c,font=('ariel',26),background=self.marker_c)
                self.numbers[a][b].place(x=self.positions[a][b][0]+15,y=self.positions[a][b][1]+7)

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


class Sudoku():
    
    def __init__(self):
        self.sudoku = [[0 for i in range(9)] for j in range(9)]
        """self.sudoku = [
            [0,0,0,2,6,0,7,0,1],
            [6,8,0,0,7,0,0,9,0],
            [1,9,0,0,0,4,5,0,0],
            [8,2,0,1,0,0,0,4,0],
            [0,0,4,6,0,2,9,0,0],
            [0,5,0,0,0,3,0,2,8],
            [0,0,9,3,0,0,0,7,4],
            [0,4,0,0,5,0,0,3,6],
            [7,0,3,0,1,8,0,0,0]
        ]"""

    def check(self,r,c,n):
        for i in range(9):
            if self.sudoku[i][c] == n:
                return False
        for i in range(9):
            if self.sudoku[r][i] == n:
                return False
        for i in range(3):
            for j in range(3):
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
                                self.sudoku[i][j] = 0
                        return
            1/0
        
        try:
            insolve()
        except:
            return

    def generate(self):
        for _ in range(50):
            a = random.randint(0,8)
            b = random.randint(0,8)
            c = random.randint(1,9)
            if self.check(a,b,c):
                self.sudoku[a][b] = c
            else:
                pass



if __name__ == '__main__':
    a = Sudoku_solver()
    a.mainloop()
