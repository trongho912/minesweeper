# Bàn cờ gồm 3 đối tượng: 
from email.policy import default
import os
class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    PURPLE = '\033[45m'
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
            case default:
                return self.ENDC

            
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
        for y in range(0,self.len):
            for x in range(0,self.len):
                cell=self.checkCell(x,y)
                if cell.isNum:
                    print("["+self.color.render(cell.index)+str(cell.index)+self.color.render('RESET')+"]", end="")
                else:
                    print("["+cell.flag+"]", end="")
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
    def checkEnoughFlag(self,x,y):
        count=0
        for ele in self.blockAround(x,y):
            if isinstance(ele,Block) and ele.flag=='?':
                count+=1

        cell= self.checkCell(x,y)
        if isinstance(cell,Num) and cell.index==count:
            return True
        else:
            return False

    def renderNumListAround(self,x,y):
        list=[]
        for num in self.numList:
            if (num.x==x+1 and num.y==y) or (num.x==x-1 and num.y==y) or (num.x==x and num.y==y+1) or (num.x==x+1 and num.y==y-1) or (num.x==x+1 and num.y==y+1) or (num.x==x+1 and num.y==y-1) or (num.x==x-1 and num.y==y+1) or (num.x==x-1 and num.y==y-1):
                list.append(num)
        return list


    def empBlock(self,x,y):
        # check tất cả ô num xung quanh
        # Nếu thỏa hết => chuyển về empty Block
        list=self.renderNumListAround(x,y)
        for num in list:
            if self.checkEnoughFlag(num.x,num.y):
                return
            else:
                continue
        
        cellBlock = self.checkCell(x,y)
        if isinstance(cellBlock,Block) and cellBlock.flag!='?':
            cellBlock.flag=" "
        else:
            return
        
    # Kiểm tra ô block có thể đặt cờ dc hay không
    def checkFlag(self,x,y):
        list=self.renderNumListAround(x,y)
        check=True
        for num in list:
            if self.checkEnoughFlag(num.x,num.y):
                check=False
                break
            else:
                continue
        return check

    # List nhung nuoc di hop le
    def renderMoveValid(self):
        list=[]
        for block in self.blockList:
            if block.flag=="#" and self.checkFlag(block.x,block.y):
                list.append(block)
        # Tìm những ô num nằm gần ô block
        # Xét những ô num đã valid hay chưa
        # Nếu tất cả chưa valid thì có thể thêm cờ vào
        return list

    # Tạo ra 1 board mới khi thực hiện 1 nước đi hợp lệ
    def duplicateBoard(self):
        newBoard= Board(self.len)
        newBoard.numList=list(map(lambda num:num.duplicateCellNum(),self.numList))
        newBoard.blockList=list(map(lambda block:block.duplicateCellBlock(),self.blockList))
        return newBoard

    def checkIsGoal(self):
        pass

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
        self.isBoom=False
        self.isNoBoom=False
        self.isNum=False
        self.flag='#'
        self.canFlag=True
        super().__init__(x, y)
    
    # Copy ra 1 o block moi
    def duplicateCellBlock(self):
        block=Block(self.x,self.y)
        block.flag=self.flag
        block.isNum=self.isNum
        block.isNoBoom=self.isNoBoom
        block.canFlag=self.canFlag
        return block

def main():
    initBoard=[
        [1,1,'w','w','w'],
        ['w','w',3,'w',2],
        ['w',1,1,1,'w'],
        [1,1,'w',1,'w'],
        ['w',1,1,'w','w']

    ]
    lenBoard=len(initBoard)
    board=Board(lenBoard)
    for x in range(0,lenBoard):
        for y in range(0,lenBoard):
            if initBoard[x][y]!='w':
                board.addNumList(x,y,initBoard[x][y])
            else:
                board.addBlockList(x,y)

    board.printBoard()
    print(len(board.renderMoveValid()))
    # for ele in board.numList:
    #     print(ele)


main()
