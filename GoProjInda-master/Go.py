from tkinter import *
import math
#tar bort klickbar knapp lägger en sten ner


class Boardbutton:
    def __init__(self,xcoord,ycoord,state,canv):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.state = state
        self.freedom = "free"
        self.canv = canv
        self.dependlist = []
        self.x =  round(float(self.xcoord)/20)- 1
        self.y =  round(float(self.ycoord)/20)- 1
        self.objekt = canv.create_oval(self.xcoord-5,self.ycoord-5,self.xcoord+5,self.ycoord+5,activefil = "red",tags="button"+str(self.x)+str(self.y))
        canv.tag_bind("button"+str(self.x)+str(self.y), '<ButtonPress-1>',placeStoneKlick )
        
        
    def changeState(self,state):
        # state kan var "button" "white" eller "black"
        self.state = state
        canv.delete(self.objekt)
        if state == "button":
            self.objekt = canv.create_oval(self.xcoord-5,self.ycoord-5,self.xcoord+5,self.ycoord+5,activefil = "red",tags="button"+str(self.x)+str(self.y))
        else:
            self.objekt = canv.create_oval(self.xcoord-5,self.ycoord-5,self.xcoord+5,self.ycoord+5,fil = state,tags="stone"+str(self.x)+str(self.y))   

#tar rekursivt fram en group
#genom att hitta de platser i matrisen
#som har samma state och nuddar varandra, rekursivt
    def getGroup(self, lista):
        lista.append(self)
        for x in self.directions:
            if x != None:
                if not x in lista:
                    if x.state == self.state:
                        x.getGroup(lista)
        return lista


    def freedomgroupcheck(self):
        #
        print("loopar fgc")
        deplist = []
        if self.freedom == "free":
            return True
        for x in self.directions:
            if x != None:
                if not x.state == self.state:
                    break
                if x.freedom == "dependent":
                    self.dependentlist.append(x)
                if x.freedom == "free":
                    return True
                else:
                    pass
        for x in self.dependentlist:
            deplist = self.dependentlist
            #self.dependentlist = []
            if (x.freedomgroupcheck()):
                return True
        x.dependentlist = deplist
        return False

#settar directionlista med pekare till de intilligande positionerna i matrisen
    def createdirections(self):
        
        global boardList
        if self.y < 1:
            up = None
        else:
            up = boardList[self.y-1][self.x]
        if self.y+2 > len(boardList):
            down = None
        else:
            down = boardList[self.y+1][self.x]
        if self.x < 1:
            left = None
        else:
            left = boardList[self.y][self.x-1]
        if self.x+2 > len(boardList):
            right = None
        else:
            right = boardList[self.y][self.x+1]
        self.directions = [up,down,left,right]

#settar frihet hos en sten beroende av de intilliggande positionerna
    def setfreedom(self):
        self.dependentlist = []
        
        for i in self.directions:
            if i != None:
                if i.state == "button":
                    #print("knapp som e fri:",i.x,i.y,i.state)
                    #print("freedom blir free")
                    self.freedom = "free"
                    return
        for i in self.directions:
            if i != None:
                if i.state == self.state:
                    #print(i.state,"ikna0",self.state,"selfstat")
                    #print("knapp som e beroend av:",i.x,i.y,i.state)
                    #print("freedom blir dependent")
                    self.freedom = "dependent"
                    self.dependentlist.append(i)
                    return
        #print("freedom blir unfree")
        self.freedom = "unfree"
        return
    

def switchTurn(turn):
    if turn == "black":
        turn = "white"
    else:
        turn = "black"
    return turn


def placeStoneKlick(event):
    global boardList
    global turn
    global turnlist
    x =  round(float(event.x)/20)- 1
    y =  round(float(event.y)/20)- 1
    reverturnlist = turnlist
    newturnlist = [[0,"blank"],[0,"blank"],[0,"blank"]]
    newturnlist[0] = [boardList[y][x],turn]
    newturnlist[1] = turnlist[0]
    newturnlist[2] = turnlist[1]
    turnlist = newturnlist 
    if turnlist[0] != turnlist[2]:
        if True:
            if turn == "white":
                boardList[y][x].changeState("white")
            else:
                boardList[y][x].changeState("black")
            i = y
            j = x
            # kod upprepning 3 gånger eftersom #update utan det man klickade på, update med det man klickade på och sedan uppdate allt
            breaker = False
            for i in range(len(boardList)):
                for j in range(len(boardList[i])):
                    if i != y or j != x:
                        boardList[i][j].setfreedom()
                        #print(boardList[8][8].state,boardList[8][8].freedom)
                        if boardList[i][j].freedom == "unfree":
                            boardList[i][j].changeState("button")
                        if boardList[i][j].freedom == "dependent":
                            lst = boardList[i][j].getGroup([])
                            grpfree = False
                            for q in lst:
                                if q.freedom == "free":
                                    grpfree = True
                            if grpfree == False:
                                for q in lst:
                                    if q == boardList[y][x]:
                                        boardList[y][x].changeState("button")
                                        breaker = True
                                        break
                                if breaker == True:
                                    break
                                for q in lst:
                                    q.changeState("button")
            i = y
            j = x
            boardList[i][j].setfreedom()
                #print(boardList[8][8].state,boardList[8][8].freedom)
            if boardList[i][j].freedom == "unfree":
                boardList[i][j].changeState("button")
            if boardList[i][j].freedom == "dependent":
                lst = boardList[i][j].getGroup([])
                grpfree = False
                for q in lst:
                    if q.freedom == "free":
                        grpfree = True
                if grpfree == False:
                        for q in lst:
                            if q == boardList[y][x]:
                                boardList[y][x].changeState("button")
                                breaker = True
                                break
                        for q in lst:
                            q.changeState("button")
                        
            for i in range(len(boardList)):
                for j in range(len(boardList[i])):
                    if True:
                        boardList[i][j].setfreedom()
                        #print(boardList[8][8].state,boardList[8][8].freedom)
                        if boardList[i][j].freedom == "unfree":
                            boardList[i][j].changeState("button")
                        if boardList[i][j].freedom == "dependent":
                            lst = boardList[i][j].getGroup([])
                            grpfree = False
                            for q in lst:
                                if q.freedom == "free":
                                    grpfree = True
                            if grpfree == False:
                                for q in lst:
                                    if q == boardList[y][x]:
                                        boardList[y][x].changeState("button")
                                        breaker = True
                                        break
                                if breaker == True:
                                    break
                                for q in lst:
                                    q.changeState("button")



        #print("bolean:",boardList[y][x].freedomgroupcheck())
        #print(boardList[y][x].freedom)
        #print(boardList[7][8].freedom,78)
        #print(boardList[8][8].freedom,88)
        boardList[i][j].setfreedom()
        if boardList[i][j].freedom == "unfree":
            boardList[i][j].changeState("button")
        if not boardList[y][x].state == "button":
            turn = switchTurn(turn)
    else:
        turnlist = reverturnlist
    global score
    score = countscore()
    #print(score)
    
        

#Tar fram score med funktionen getgroup() enligt kinesiska regler
#svarta och vita grupper adderas till respektive spelares score
#tomma knappar grupperas också och om de
#endast nuddar en spelares stenar adderas de till dennes score
def countscore():
    global boardList
    blackpoints = 0
    whitepoints = 5.5
    countedbuttons = []
    for i in range(len(boardList)):
        for j in range(len(boardList[i])):
            if boardList[i][j].state == "black":
                blackpoints += 1
            if boardList[i][j].state == "white":
                whitepoints += 1
            if boardList[i][j].state == "button":
                if not boardList[i][j] in countedbuttons:
                    belongsto = []
                    grptouches = []
                    buttongroup = boardList[i][j].getGroup([])
                    for l in buttongroup:
                        countedbuttons.append(l)
                    for btn in buttongroup:
                        for direc in btn.directions:
                            if direc != None:
                                grptouches.append(direc)
                    for position in grptouches:
                        if position.state == "black":
                            belongsto.append("black")
                        if position.state == "white":
                            belongsto.append("white")
                    if "white" in belongsto and "black" in belongsto:
                        pass
                    elif "white" in belongsto:
                        for k in range(len(buttongroup)):
                            whitepoints += 1
                    elif "black" in belongsto:
                        for k in range(len(buttongroup)):
                            blackpoints += 1
    return ("Black score: "+str(blackpoints)+" White score: "+str(whitepoints))
 





def passa(event):
    global turn
    turn = switchTurn(turn)
def done(event):
    global root
    global score
    root.destroy()
    score = str(score)
    master = Tk()
        
    button = Button(master,text ="********final score********\n\n"+score+"\n\n********final score********"  )
    button.pack()

    master.mainloop()
            

def createnet(width,height,canv):
    text = canv.create_text(15,8, text = "pass",tags ="passtext",activefil = "blue")
    text = canv.create_text(width,8, text = "done",tags ="done",activefil = "blue") 
    canv.tag_bind(("passtext"), '<ButtonPress-1>',passa)
    canv.tag_bind(("done"), '<ButtonPress-1>',done)
    #skapar hela canvasens linjer och klickbara cirklar
    #lägger alla cirklars obj i en lista, 
    linelist = []
    buttonlist = []
    i = 0
    n = 0
    row = 0
    col = 0
    #loop för att skapa alla rows dvs lodrätta linjer
    while n < height :
        obj = canv.create_line(20, n+20, width, n+20, width=2, tags="row"+str(row))
        row = row + 1
        linelist.append(obj)
        i = i +1
        n = n + 20
    n = 0
    #loop för att skapa alla col asså alla vågrätta linjer
    while n < width :
        obj = canv.create_line(n+20, 20, n+20, height, width=2, tags="col"+str(col))
        col = col + 1
        linelist.append(obj)
        i = i +1
        n = n + 20
    row = 0
    col = 0
    xn = 0
    yn = 0
    #loop för att skappa alla cirklar
    while yn < height :
        col = col + 1
        i = i +1
        yn = yn + 20
        xn = 0
        miniList = []
        while xn < width :
            xn = xn + 20
            obj = Boardbutton(xn,yn,"button",canv)
            row = row + 1
            miniList.append(obj)
            i = i +1
        buttonlist.append(miniList)

    button = Button(canv,text ="pass", command=passa)
    return [linelist,buttonlist]


def ok():
    global master
    global var
    global size
    size = var.get()
    master.destroy()
    if size == "9x9":
        size = (9)
    if size == "13x13":
        size = (13)
    if size == "19x19":
        size = (19)


def meny():
    global master
    global var
    global size

    master = Tk()

    var = StringVar(master)
    var.set("9x9") # initial value

    option = OptionMenu(master, var, "9x9", "13x13", "19x19")
    option.pack()
        
    button = Button(master,text ="choose size", command=ok)
    button.pack()

    master.mainloop()

    
    return size
    
        
def main():
    global root
    size = meny()
    root = Tk()
    global boardList
    global canv
    global turn
    global turnlist
    turnlist = [[0,"blank"],[0,"blank"],[0,"blank"]]
    turn = "black"
    # 180/20 = 9 asså får man ett 9x9 rutnär
    # för tex 11x11 rutnät sätt width och heigth till 240
    # obs canv height och width måste vara 20 större för att de ska se bra ut



    width = size * 20
    height = size * 20
    he = height + 20
    wid = width + 20
    canv = Canvas(root, width=wid, height=he)
    twoLists = createnet(width,height,canv)
    boardList = twoLists[1]
    for x in boardList:
        for y in x:
            y.createdirections()
            
    canv.pack()
    root.mainloop()


if __name__ == '__main__':
    main()

