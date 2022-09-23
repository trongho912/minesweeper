import os
from pickle import NEWOBJ
import getboard
import inquirer

class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    PURPLE = '\033[35m'
    LIGHTGREY = '\033[37m'
    DARKGREY = '\033[90m'
    PINK = '\033[96m'
    CWHITE2  = '\33[97m'
    ENDC = '\033[m'
    def render(self,index):
        match index:
            case 0:
                return self.CYAN
            case 1:
                return self.BLUE
            case 2:
                return self.GREEN
            case 3:
                return self.RED
            case 4:
                return self.YELLOW
            case 5:
                return self.PURPLE
            case 6:
                return self.LIGHTGREY
            case 7:
                return self.DARKGREY
            case 8: 
                return self.PINK
            case default:
                return self.CWHITE2
from re import T


class Board:
    def __init__(self,len):
        self.len=len
        self.numList=[]
        self.blockList=[]
        self.color=Color()
    
    # Thêm ô có số
    def addNumList(self,x,y,index):
        self.numList.append(Num(x,y,index))        

    # Thêm ô trống
    def addBlockList(self,x,y):
        self.blockList.append(Block(x,y))   
    
    # Trả về cell ở vị trí x , y
    def checkCell(self,x,y):
        if x in range(0, self.len) and y in range(0,self.len):
            for num in self.numList:
                if num.x==x and num.y==y:
                    return num

            for block in self.blockList:
                if block.x==x and block.y==y:
                    return block
        
        return None
            

    def printBoard(self):
        print('\n')
        for x in range(0,self.len):
            for y in range(0,self.len):
                cell=self.checkCell(x,y)
                if cell.isNum:
                    print(self.color.render(cell.index)+"["+str(cell.index)+"]"+self.color.render('RESET'), end=" ")
                else:
                    print("["+cell.flag+"]", end=" ")
            print('\n')


    def listMoveValid(self):
        pass

    # Tao 1 list cac o xung quanh [x+-1, y+-1]
    def blockAround(self,x,y):
        up=self.checkCell(x+1,y)
        down=self.checkCell(x-1,y)
        left=self.checkCell(x,y+1)
        right=self.checkCell(x,y-1)
        upLeft=self.checkCell(x+1,y+1)
        upRight=self.checkCell(x+1,y-1)
        downRight=self.checkCell(x-1,y-1)
        downLeft=self.checkCell(x-1,y+1)
        list = [up,down,left,right,upLeft,upRight,downRight,downLeft]
        rs=[]
        for ele in list:
            if ele is None:
                continue
            else:
                rs.append(ele)
        return rs
        
    # Kiem tra xung quanh ô số đã đủ cờ hay chưa
    # True la da du. False la chua
    def checkNumOfFlags(self,x,y):
        count=0
        for ele in self.blockAround(x,y):
            if isinstance(ele,Block) and ele.flag=='?':
                count+=1
        return count
    
    def checkNumOfBlocks(self,x,y):
        count=0
        for ele in self.blockAround(x,y):
            if isinstance(ele,Block) and ele.flag=='#':
                count+=1
        return count

    # Tạo ra 1 board mới khi thực hiện 1 nước đi hợp lệ
    def duplicateBoard(self):
        newBoard= Board(self.len)
        newBoard.numList=list(map(lambda num:num.duplicateCellNum(),self.numList))
        newBoard.blockList=list(map(lambda block:block.duplicateCellBlock(),self.blockList))
        return newBoard

    # def checkIsGoal(self):
    #     pass
    
    def process(self):
        newBoard = self.duplicateBoard()
        list=newBoard.numList
        while list:
            for num in list:
                countFlag=self.checkNumOfFlags(num.x, num.y)
                countBlock=self.checkNumOfBlocks(num.x, num.y)
                if(num.index == countFlag):
                    for block in self.blockAround(num.x, num.y):
                        if isinstance(block,Block) and block.flag=="#":
                            block.flag=" "
                    # self.printBoard()
                    list.remove(num)
                    continue
                elif(num.index == (countBlock + countFlag)):
                    for block in self.blockAround(num.x, num.y):
                        if isinstance(block,Block) and block.flag=="#":
                            block.flag="?"
                    # self.printBoard()   
                    list.remove(num) 
                    continue    
        self.printBoard()
    # GIẢI THUẠT
    # Đối với trường hợp Easy mode  (Hard mode chưa nghĩ ra :> )
    # Kiểm tra từng phần tử trong numList
    # Gặp ô num nào thỏa 1 trong 2 điều kiện 
    # 1. Số Flag ở các block xung quanh = với index => các block còn lại chưa có flag = '?' xung quanh ô num này được đánh flag = ' '
    # 2. số Flag + số Block = index => đánh dấu các block thành flag='?'

class Location:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Num(Location):
    def __init__(self, x, y, index):
        self.index=index
        self.isNum=True
        self.isValid=False
        super().__init__(x, y)
    
    # Copy ra 1 o num moi
    def duplicateCellNum(self):
        return Num(self.x,self.y,self.index)

class Block(Location):
    def __init__(self, x, y):
        self.isMine=False
        self.isNoMine=False
        self.isNum=False
        self.flag='#'
        self.canFlag=True
        super().__init__(x, y)
    
    # Copy ra 1 o block moi
    def duplicateCellBlock(self):
        block=Block(self.x,self.y)
        block.flag=self.flag
        block.isNum=self.isNum
        block.isNoMine=self.isNoMine
        block.canFlag=self.canFlag
        return block

def main():
    questions = [
        inquirer.List('level', message="Choose level",
                       choices=['Easy', 'Medium', 'Hard'],
            ),
    ]
    level = inquirer.prompt(questions)
    # print (level)

    if (level['level'] == "Easy"):
        url = "https://www.puzzle-minesweeper.com/minesweeper-5x5-easy/"
    elif (level['level'] == 'Medium'):
        url = "https://www.puzzle-minesweeper.com/minesweeper-10x10-easy/"
    else:
        url = "https://www.puzzle-minesweeper.com/minesweeper-20x20-easy/"
    
    # url = "https://www.puzzle-minesweeper.com/minesweeper-7x7-easy/"
    initBoard=getboard.main(url)
    # 10x10 sample
    # initBoard=[
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w','w','w','w']
    # ]
    # 7x7 sample
    # initBoard=[
    #     ['w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w'],
    #     ['w','w','w','w','w','w','w']
    # ]
    # 5x5
    # initBoard=[
    #     ['w','w','w','w','w'],
    #     ['w','w','w','w','w'],
    #     ['w','w','w','w','w'],
    #     ['w','w','w','w','w'],
    #     ['w','w','w','w','w']
    # ]
    
    lenBoard=len(initBoard)
    board=Board(lenBoard)
    
    for x in range(0,lenBoard):
        for y in range(0,lenBoard):
            if initBoard[x][y]!='w':
                board.addNumList(x,y,initBoard[x][y])
            else:
                board.addBlockList(x,y)

    board.printBoard()
    
    board.process()


main()




# # Importing packages
# import random
# import os
 
# # Printing the Minesweeper Layout
# def print_mines_layout():
 
#     global mine_values
#     global n
 
#     print()
#     print("\t\t\tMINESWEEPER\n")
 
#     st = "   "
#     for i in range(n):
#         st = st + "     " + str(i + 1)
#     print(st)   
 
#     for r in range(n):
#         st = "     "
#         if r == 0:
#             for col in range(n):
#                 st = st + "______" 
#             print(st)
 
#         st = "     "
#         for col in range(n):
#             st = st + "|     "
#         print(st + "|")
         
#         st = "  " + str(r + 1) + "  "
#         for col in range(n):
#             st = st + "|  " + str(mine_values[r][col]) + "  "
#         print(st + "|") 
 
#         st = "     "
#         for col in range(n):
#             st = st + "|_____"
#         print(st + '|')
 
#     print()
  
# # Function for setting up Mines
# def set_mines():
 
#     global numbers
#     global mines_no
#     global n
 
#     # Track of number of mines already set up
#     count = 0
#     while count < mines_no:
 
#         # Random number from all possible grid positions 
#         val = random.randint(0, n*n-1)
 
#         # Generating row and column from the number
#         r = val // n
#         col = val % n
 
#         # Place the mine, if it doesn't already have one
#         if numbers[r][col] != -1:
#             count = count + 1
#             numbers[r][col] = -1
 
# # Function for setting up the other grid values
# def set_values():
 
#     global numbers
#     global n
 
#     # Loop for counting each cell value
#     for r in range(n):
#         for col in range(n):
 
#             # Skip, if it contains a mine
#             if numbers[r][col] == -1:
#                 continue
 
#             # Check up  
#             if r > 0 and numbers[r-1][col] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check down    
#             if r < n-1  and numbers[r+1][col] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check left
#             if col > 0 and numbers[r][col-1] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check right
#             if col < n-1 and numbers[r][col+1] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check top-left    
#             if r > 0 and col > 0 and numbers[r-1][col-1] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check top-right
#             if r > 0 and col < n-1 and numbers[r-1][col+1] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check below-left  
#             if r < n-1 and col > 0 and numbers[r+1][col-1] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
#             # Check below-right
#             if r < n-1 and col < n-1 and numbers[r+1][col+1] == -1:
#                 numbers[r][col] = numbers[r][col] + 1
 
# # Recursive function to display all zero-valued neighbours  
# def neighbours(r, col):
     
#     global mine_values
#     global numbers
#     global vis
 
#     # If the cell already not visited
#     if [r,col] not in vis:
 
#         # Mark the cell visited
#         vis.append([r,col])
 
#         # If the cell is zero-valued
#         if numbers[r][col] == 0:
 
#             # Display it to the user
#             mine_values[r][col] = numbers[r][col]
 
#             # Recursive calls for the neighbouring cells
#             if r > 0:
#                 neighbours(r-1, col)
#             if r < n-1:
#                 neighbours(r+1, col)
#             if col > 0:
#                 neighbours(r, col-1)
#             if col < n-1:
#                 neighbours(r, col+1)    
#             if r > 0 and col > 0:
#                 neighbours(r-1, col-1)
#             if r > 0 and col < n-1:
#                 neighbours(r-1, col+1)
#             if r < n-1 and col > 0:
#                 neighbours(r+1, col-1)
#             if r < n-1 and col < n-1:
#                 neighbours(r+1, col+1)  
 
#         # If the cell is not zero-valued            
#         if numbers[r][col] != 0:
#                 mine_values[r][col] = numbers[r][col]
 
# # Function for clearing the terminal
# def clear():
#     os.system("clear")      
 
# # Function to display the instructions
# def instructions():
#     print("Instructions:")
#     print("1. Enter row and column number to select a cell, Example \"2 3\"")
#     print("2. In order to flag a mine, enter F after row and column numbers, Example \"2 3 F\"")
 
# # Function to check for completion of the game
# def check_over():
#     global mine_values
#     global n
#     global mines_no
 
#     # Count of all numbered values
#     count = 0
 
#     # Loop for checking each cell in the grid
#     for r in range(n):
#         for col in range(n):
 
#             # If cell not empty or flagged
#             if mine_values[r][col] != ' ' and mine_values[r][col] != 'F':
#                 count = count + 1
     
#     # Count comparison          
#     if count == n * n - mines_no:
#         return True
#     else:
#         return False
 
# # Display all the mine locations                    
# def show_mines():
#     global mine_values
#     global numbers
#     global n
 
#     for r in range(n):
#         for col in range(n):
#             if numbers[r][col] == -1:
#                 mine_values[r][col] = 'M'
 
 
# if __name__ == "__main__":
 
#     # Size of grid
#     n = 9
#     # Number of mines
#     mines_no = random.randint(3,9) 
 
#     # The actual values of the grid
#     numbers = [[0 for y in range(n)] for x in range(n)] 
#     # The apparent values of the grid
#     mine_values = [[' ' for y in range(n)] for x in range(n)]
#     # The positions that have been flagged
#     flags = []
 
#     # Set the mines
#     set_mines()
 
#     # Set the values
#     set_values()
 
#     # Display the instructions
#     instructions()
 
#     # Variable for maintaining Game Loop
#     over = False
         
#     # The GAME LOOP 
#     while not over:
#         print_mines_layout()
 
#         # Input from the user
#         inp = input("Enter row number followed by space and column number = ").split()
         
#         # Standard input
#         if len(inp) == 2:
 
#             # Try block to handle errant input
#             try: 
#                 val = list(map(int, inp))
#             except ValueError:
#                 clear()
#                 print("Wrong input!")
#                 instructions()
#                 continue
 
#         # Flag input
#         elif len(inp) == 3:
#             if inp[2] != 'F' and inp[2] != 'f':
#                 clear()
#                 print("Wrong Input!")
#                 instructions()
#                 continue
 
#             # Try block to handle errant input  
#             try:
#                 val = list(map(int, inp[:2]))
#             except ValueError:
#                 clear()
#                 print("Wrong input!")
#                 instructions()
#                 continue
 
#             # Sanity checks 
#             if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
#                 clear()
#                 print("Wrong input!")
#                 instructions()
#                 continue
 
#             # Get row and column numbers
#             r = val[0]-1
#             col = val[1]-1 
 
#             # If cell already been flagged
#             if [r, col] in flags:
#                 clear()
#                 print("Flag already set")
#                 continue
 
#             # If cell already been displayed
#             if mine_values[r][col] != ' ':
#                 clear()
#                 print("Value already known")
#                 continue
 
#             # Check the number for flags    
#             if len(flags) < mines_no:
#                 clear()
#                 print("Flag set")
 
#                 # Adding flag to the list
#                 flags.append([r, col])
                 
#                 # Set the flag for display
#                 mine_values[r][col] = 'F'
#                 continue
#             else:
#                 clear()
#                 print("Flags finished")
#                 continue    
 
#         else: 
#             clear()
#             print("Wrong input!")   
#             instructions()
#             continue
             
 
#         # Sanity checks
#         if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
#             clear()
#             print("Wrong Input!")
#             instructions()
#             continue
             
#         # Get row and column number
#         r = val[0]-1
#         col = val[1]-1
 
#         # Unflag the cell if already flagged
#         if [r, col] in flags:
#             flags.remove([r, col])
 
#         # If landing on a mine --- GAME OVER    
#         if numbers[r][col] == -1:
#             mine_values[r][col] = 'M'
#             show_mines()
#             print_mines_layout()
#             print("Landed on a mine. GAME OVER!!!!!")
#             over = True
#             continue
 
#         # If landing on a cell with 0 mines in neighboring cells
#         elif numbers[r][col] == 0:
#             vis = []
#             mine_values[r][col] = '0'
#             neighbours(r, col)
 
#         # If selecting a cell with atleast 1 mine in neighboring cells  
#         else:   
#             mine_values[r][col] = numbers[r][col]
 
#         # Check for game completion 
#         if(check_over()):
#             show_mines()
#             print_mines_layout()
#             print("Congratulations!!! YOU WIN")
#             over = True
#             continue
#         clear() 