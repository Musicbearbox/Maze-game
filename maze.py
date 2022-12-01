from ast import Pass
from multiprocessing.sharedctypes import Value
from operator import truediv
import pstats
from tkinter.messagebox import NO
import pygame,sys,time,random
from heapdict import heapdict
from config import Config


config = Config()
config.row = 39  
#row number 
config.col = 71 
#col number
config.color_block = 0,0,0
#block color rgb



config.init()

#init pygame
pygame.init()
screen = pygame.display.set_mode((config.width,config.height))
pygame.display.set_caption('maze game')
screen.fill("white")

#blocks
blockList = []
#block queue
Q = []
  
#path node
class Section: 
    def __init__(self,row,col) -> None:
        self.visited = False
        self.options = [0,1,2,3]   #up down left right
        self.row = row
        self.col = col
        self.status = 'section'
        #self.neigbours = []
    
    def checkMove(self):
        if(self.row<=1):
            self.removeOptions(0)
        if(self.col<=1):
            self.removeOptions(2)
        if(self.row>=config.row-2):
            self.removeOptions(1)
        if(self.col>=config.col-2):
            self.removeOptions(3)
       
    def addWalls(self,Q):
        self.checkMove()
        if(len(self.options)>0):
            move = random.choice(self.options)
            #add four walls
            for each in self.options:
                if(each == 0):
                    wall = blockList[self.row-1][self.col]
                    to = blockList[self.row-config.step][self.col]
                    wall.setDir(self,to)
                    
                elif(each == 1):
                    wall = blockList[self.row+1][self.col]
                    to = blockList[self.row+config.step][self.col]
                    wall.setDir(self,to)
                    
                elif(each == 2):
                    wall = blockList[self.row][self.col-1]
                    to = blockList[self.row][self.col-config.step]
                    wall.setDir(self,to)
                   
                else:
                    wall = blockList[self.row][self.col+1]
                    to = blockList[self.row][self.col+config.step]
                    wall.setDir(self,to)
                if(move == each):
                    lastWall = wall
                    continue
                Q.append(wall)
            Q.append(lastWall) #add lastOne   
            return True
        else:
            return False
 
    def removeOptions(self,option):
        if option in self.options:
            self.options.remove(option)

#black wall
class Wall:
    def __init__(self) -> None:
        self.isBroken = False
        self.status = 'wall'
    
    def toBreak(self):
        if self.fromSection.visited == False or self.toSection.visited == False:
            self.isBroken = True    
            self.fromSection.visited = True
            self.toSection.visited = True
            return True
        return False

    def setDir(self,fromSection,toSection):
        self.fromSection = fromSection
        self.toSection = toSection

#controllable role
class Role:
    def __init__(self,config) -> None:
        self.path = "./image/2.jpeg"
        self.image = pygame.image.load(self.path)
        self.col = 1
        self.row = 1
        self.step = config.eachSize
        self.x = self.col*self.step
        self.y = self.row*self.step
        self.dialog_button = False
        self.config = config
        
        screen.blit(self.image,(self.x,self.y))
        #add end
        pygame.draw.rect(screen,(61,145,64),((config.col-2)*self.step,(config.row-2)*self.step,self.step,self.step))


    def move(self,dire):
        if dire == 0:
            #up
            col = self.col
            row = self.row-1
        if dire == 1:
            #down
            col = self.col
            row = self.row+1
        if dire == 2:
            #left
            col = self.col-1
            row = self.row
        if dire == 3:
            #right
            col = self.col+1
            row = self.row
        if(self.moveCheck(row,col)):
            #check is pass
            pygame.draw.rect(screen,(255,255,255),(self.x,self.y,self.step,self.step))
            #block old one
            self.col = col
            self.row = row
            self.x = self.col*self.step
            self.y = self.row*self.step
            screen.blit(self.image,(self.x,self.y))
            # self.dialog()
            if self.endCheck():
                self.dialog()

    def autoMove(self,points):
        l = len(points)
        for i  in range(l):
            each = points.pop()
            col = each.x
            row = each.y
            self.col = col
            self.row = row
            self.x = self.col*self.step
            self.y = self.row*self.step
            screen.blit(self.image,(self.x,self.y))

    def moveCheck(self,row,col):
        if row< 1 or row > (config.row-1) or col<1 or col>(config.col-1):
            return False
        newPosition = blockList[row][col]
        if(newPosition.status == 'wall' and newPosition.isBroken == False):
            return False
        return True

    def endCheck(self):
        if(self.col==config.col-2 and self.row==config.row-2):
            return True
        else:
            return False
    def stop(self):
        if(self.dialog_button):
            self.dialog_button.unbind()
            self.dialog_button=False
        pygame.draw.rect(screen,(255,255,255),(self.x,self.y,self.step,self.step))
    
    def dialog(self):
        screen.fill((0,0,0),(0,0,self.config.width,self.config.height))
        self.dialog_button = Button('congratulation! restart')
        self.dialog_button.draw_button()
        self.dialog_button.actiion()

#game button
class Button():
    def __init__(self,msg,size=[200,80],right_button=False,position=False,font=40) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width = size[0]
        self.height = size[1]
        self.right = right_button
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None,font)
        self.rect = pygame.Rect(0,0,self.width,self.height)
        if(self.right==False):
            self.rect.center = self.screen_rect.center
        else:
            self.rect.topright = self.screen_rect.topright
            if(position!=False):
                self.rect.top = position
            
        self.msg_create(msg)
        self.listen = False

    def msg_create(self,msg):
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        self.screen.blit(self.msg_image,self.msg_image_rect)

    def actiion(self):
        self.listen = True
        
    def unbind(self):
        self.listen = False


#maze generator
class Maze():
    def __init__(self) -> None:
        self.listen = True

    def start(self):
        self.resetMaze()
        self.role = Role(config)
        self.bind()
        buttons.reset()
        
    def stop(self):
        self.unbind()
        self.role.stop()

    def resetMaze(self):
        blockList.clear()
        screen.fill("white")
        Q.clear()
        # init
        for i in range(config.row):
            eachLine = []
            for j in range(config.col):
                if(j%2==0 or i%2==0):
                    eachLine.append(Wall())
                else:
                    eachLine.append(Section(i,j))
            blockList.append(eachLine)
            #add all block

        #breakWall
        start = blockList[1][1]
        start.addWalls(Q)

        #tree
        # visitTree = [(1,1)]

        while len(Q):
            max = len(Q)
            index = random.randint(0, max-1)
            eachWall = Q.pop(index)
            if(eachWall.toBreak()):
                next = eachWall.toSection
                next.addWalls(Q)
            
                
        for i in range(config.row):
            for j in range(config.col):
                if(blockList[i][j].status=='section'):
                    continue
                elif(blockList[i][j].isBroken == True):
                    continue
                else:
                    pygame.draw.rect(screen,config.color_block,(j*config.eachSize,i*config.eachSize,config.eachSize,config.eachSize))
    
    def bind(self):
        self.listen = True
    
    def unbind(self):
        self.listen = False

 #button list   
class buttonList():
    def __init__(self) -> None:
        self.button1 = Button('restart',[100,80],True,False,30)
        self.button2 = Button('autofind',[100,80],True,150,30)
        self.button1.draw_button()
        self.button1.actiion()
        self.button2.draw_button()
        self.button2.rect.top = 100
        self.button2.actiion()
        self.bind()
    def reset(self):
        self.unbind()
        self.button1 = Button('restart',[100,80],True,False,30)
        self.button2 = Button('autofind',[100,80],True,150,30)
        self.button1.draw_button()
        self.button1.actiion()
        self.button2.draw_button()
        self.button2.actiion()
        self.bind()

    def unbind(self):
        self.button1.listen = False
        self.button2.listen = False
    def bind(self):
        self.button1.listen = True
        self.button2.listen = True


#button click actions
class ActionList():
    def __init__(self) -> None:
        self.listen = True
        self.bind()
    
    def bind(self):
        clock = pygame.time.Clock()
        while self.listen:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    pygame.quit()
                    sys.exit()    
                if event.type == pygame.KEYDOWN and (maze.listen==True):
                    if event.key == pygame.K_UP:
                        maze.role.move(0)
                    if event.key == pygame.K_DOWN:
                        maze.role.move(1)
                    if event.key == pygame.K_LEFT:
                        maze.role.move(2)
                    if event.key == pygame.K_RIGHT:
                        maze.role.move(3)
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    mouse_x,mouse_y =  pygame.mouse.get_pos()
                    if(maze.role) and (maze.role.dialog_button!=False) and (maze.role.dialog_button.listen==True):
                        if maze.role.dialog_button.rect.collidepoint(mouse_x,mouse_y):
                            maze.stop()
                            maze.start()
                    if(buttons.button1 and buttons.button1.listen==True):
                        if buttons.button1.rect.collidepoint(mouse_x,mouse_y):
                            maze.stop()
                            maze.start()
                    if(buttons.button2 and buttons.button2.listen==True):
                        if buttons.button2.rect.collidepoint(mouse_x,mouse_y):
                            astar = Astar(maze,[config.col,config.row])
                            ps = astar.find()
                            maze.role.autoMove(ps)
                            buttons.button2.unbind()
                    
                pygame.display.update()

#a-star algorithm
class Astar():
    def __init__(self,maze,endPosition) -> None:
        self.openList = heapdict()
        self.closeList = []
        self.openDict = {}
        self.closeDict = {}
        self.end = False
        self.endX = endPosition[0]
        self.endY = endPosition[1]

        x = maze.role.col
        y = maze.role.row
        self.start = Point(x,y,-1,False,[self.endX,self.endY])
        self.putInOpen(self.start)
        self.path = []

    def find(self):
        stop = False
        while not stop:
            point = self.takeOutOpen()
            if(self.isInClose(point)):
                continue
            #find neighbors
            up_neighbor = Point(point.x,point.y-1,point,self.start,[self.endX,self.endY])
            down_neighbor = Point(point.x,point.y+1,point,self.start,[self.endX,self.endY])
            left_neighbor = Point(point.x-1,point.y,point,self.start,[self.endX,self.endY])
            right_neighbor = Point(point.x+1,point.y,point,self.start,[self.endX,self.endY])
            neighbours = [up_neighbor,down_neighbor,left_neighbor,right_neighbor]
            for each in neighbours:
                if(each.isValid()):
                    if(not self.isInOpen(each)) and (not self.isInClose(each)):
                        #check if this is the end
                        self.putInOpen(each)
                        if(self.isEnd(each)):
                            self.end = each
                            stop = True
                            break

            #point go to close
            self.putInClose(point)
        
        #end process
        self.endProcess(self.end)
        return self.path

    def putInOpen(self,point):
        self.openList[point] = point.f
        key = (point.x,point.y)
        self.openDict[key] = True

    def putInClose(self,point):
        self.closeList.append(point)
        key = (point.x,point.y)
        self.closeDict[key] = True

    def isInOpen(self,point):
        key = (point.x,point.y)
        if(self.openDict.get(key,False)):
            return True
        else:
            return False

    def isInClose(self,point):
        key = (point.x,point.y)
        if(self.closeDict.get(key,False)):
            return True
        else:
            return False

    def takeOutOpen(self):
        pair = self.openList.popitem()
        point = pair[0]
        key = (point.x,point.y)
        del self.openDict[key]
        return point

    def isEnd(self,point):
        # print(self.endX,point.x)
        if point.x == self.endX-2 and point.y == self.endY-2:
            return True
        else:
            return False

    def isBegin(self,point):
        if point.x == self.start.x and point.y == self.start.y:
            return True
        else:
            return False

    def endProcess(self,point):
        if(self.isBegin(point)):
            self.path.append(point)
        else:
            self.path.append(point)
            self.endProcess(point.p)
    
class Point():
    def __init__(self,x,y,p,o,e) -> None:
        self.x = x
        self.y = y
        self.p = p
        self.o = o  #startPoint   False=self
        self.e = e
        self.generateF()

    def generateF(self):
        self.generateG()
        self.generateH()
        self.f = self.g + self.h

    def generateG(self):
        if(self.p == -1):
            self.g = 0
            return
        dx = self.x - self.o.x
        dy = self.y - self.o.y
        self.g = abs( dx+dy )

    def generateH(self):
        ex = self.e[0]-2
        ey = self.e[1]-2
        dx = ex - self.x
        dy = ey - self.y
        self.h = abs(dx+dy)

    def isValid(self):
        if(self.x<=0 or self.y<=0 or self.x >= self.e[0]-1 or self.y >= self.e[1]-1):
            return False
        block = blockList[self.y][self.x]
        if(block.status == 'wall' and block.isBroken == False):
            return False
        
        return True
    
    # def isInList(self,listDict):
    #     key = (self.x,self.y)
    #     if listDict[key]==True:
    #         return True
    #     else:
    #         return False

    
buttons = buttonList()
maze = Maze()
maze.start()
actions = ActionList()
