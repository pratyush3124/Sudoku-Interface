from tkinter import *
import numpy as np
import random

class Sudoku_solver(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        frame = Sudoku_grid(self)
        frame.grid(row = 0, column = 0)


class Sudoku_grid(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent

        self.sudoku = Sudoku()
        self.sudoku.generate()

        self.boxes = [[0 for i in range(3)] for j in range(3)]
        self.cells = [[0 for i in range(9)] for j in range(9)]
        font = ('Ariel',22,'bold')
        for i in range(3):
            for j in range(3):
                self.boxes[i][j] = Label(self,text=' ', font=font, background='white', bd=4, relief='ridge',height = 6,width = 12)
                self.boxes[i][j].grid(row = i,column = j)

        for i in range(9):
            for j in range(9):
                string = ''

                if i%3 > 1:
                    string += 'S'
                if i%3 < 1:
                    string += 'N'
                if j%3 > 1:
                    string += 'E'
                if j%3 < 1:
                    string += 'W'

                t = self.sudoku.sudoku[i][j] if self.sudoku.sudoku[i][j] != 0 else ''
                self.cells[i][j] = Label(self, text=t, font=font, background='white', bd=1, relief='ridge', height=2, width=4)
                self.cells[i][j].grid(row = i//3,column = j//3,sticky = string)
                self.cells[i][j].bind('<Button-1>',lambda event,r=i,c=j: self.click(r,c))
        
        self.focus_set()
        self.bind('<Key>',lambda event: self.write(event))
        self.bind('<Left>',lambda event: self.left())
        self.bind('<Right>',lambda event: self.right())
        self.bind('<Up>',lambda event: self.up())
        self.bind('<Down>',lambda event: self.down())
        self.bind('<BackSpace>',lambda event: self.delete())

        self.marker = [0,0]
        self.refresh()

    def refresh(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j]['background'] = 'white'        
        self.cells[self.marker[0]][self.marker[1]]['background'] = 'yellow'

    def write(self,event):
        if event.char.isnumeric():
            self.cells[self.marker[0]][self.marker[1]]['text'] = event.char if event.char!='0' else None
        elif event.char == 'w':
            self.up()
        elif event.char == 's':
            self.down()
        elif event.char == 'a':
            self.left()
        elif event.char == 'd':
            self.right()

    def left(self):
        self.marker[1]-= 1 if self.marker[1]-1 in range(9) else 0
        self.refresh()
    def right(self):
        self.marker[1]+=1 if self.marker[1]+1 in range(9) else 0
        self.refresh()
    def up(self):
        self.marker[0]-=1 if self.marker[0]-1 in range(9) else 0
        self.refresh()
    def down(self):
        self.marker[0]+=1 if self.marker[0]+1 in range(9) else 0
        self.refresh()

    def click(self,r,c):
        self.marker = [r,c]
        self.refresh()

    def delete(self):
        self.cells[self.marker[0]][self.marker[1]]['text'] = ' '


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

    # def solvable(self):
        # for i in range(9):
            # for j in range(9):
                # if self.sudoku[i][j] == 0:
                    # if check(i,j,sudoku[i][j]):

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
