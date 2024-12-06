import random

import pygame
from pygame import *
import pygame as pg
import math

wind=display.set_mode((640,640))
display.set_caption('Chess')
clock=time.Clock()
font.init()

RectList=[]
for i in range(8):
    for n in range(4):
        RectList.append(pygame.Rect((n*160+(i%2)*80,i*80, 80, 80)))


Board=[
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.']]

AttackDict={'B':[[1,1],[-1,-1],[1,-1],[-1,1],1],
            'H':[[1,2],[2,1],[-1,-2],[-2,-1],[-1,2],[-2,1],[1,-2],[2,-1],0],
            'P':[[-1,-1],[1,-1],0],
            'p':[[-1,1],[1,1],0],
            'K':[[1,1],[-1,-1],[1,-1],[-1,1],[0,1],[1,0],[0,-1],[-1,0],0]
            }



def MakeBoard():
    global Board

    startboard = []
    for i in range(8):
        startboard.append([])
        for j in range(8):
            startboard[i].append(j)


    p1 = random.randint(0,7)
    p2 = random.randint(0,3) * 2
    if(p1 % 2 != 0): p2 += 1
    b1 = [p1, p2]
    startboard[p1].pop(p2)

    p3 = random.randint(0,7)
    p4 = random.randint(0,3) * 2
    if(p3 % 2 == 0): p4 += 1
    b2 = [p3, p4]

    startboard[p3].remove(p4)

    K11 = random.randint(0, len(startboard)-1)
    K12 = startboard[K11][random.randint(0, len(startboard[K11])-1)]
    k1 = [K11, K12]

    startboard[K11].remove(K12)

    for i in range(8):
        if not(0 <= i-p1+p2 <= 7): continue
        try: startboard[i].remove(i-p1+p2)
        except: 0
    for i in range(8):
        if not(0 <= -i+p1+p2 <= 7): continue
        try: startboard[i].remove(-i+p1+p2)
        except: 0
    for i in range(-1, 2):
        if not(0 >= p1 + i >= 7): continue
        for j in range(-1, 2):
            if(i==0)and(j==0): continue
            if not(0 >= p2 + j >= 7): continue
            try: startboard[p1 + i].remove(p2+j)
            except: 0
    for i in range(8):
        if not (0 <= i - p3 + p4 <= 7): continue
        try: startboard[i].remove(i - p3 + p4)
        except: 0
    for i in range(8):
        if not (0 <= -i + p3 + p4 <= 7): continue
        try: startboard[i].remove(-i + p3 + p4)
        except: 0
    for i in range(-1, 2):
        if not(0 >= p3 + i >= 7): continue
        for j in range(-1, 2):
            if(i==0)and(j==0): continue
            if not(0 >= p4 + j >= 7): continue
            try: startboard[p3 + i].remove(p4+j)
            except: 0
    for i in range(-1, 2):
        if not(0 >= K11 + i >= 7): continue
        for j in range(-1, 2):
            if(i==0)and(j==0): continue
            if not(0 >= K12 + j >= 7): continue
            try: startboard[K11 + i].remove(K12+j)
            except: 0

    K21 = random.randint(0, len(startboard)-1)
    K22 = startboard[K21][random.randint(0, len(startboard[K11])-1)]
    k2 = [K21, K22]
    startboard[K21].remove(K22)

    for i in [-2, -1, 1, 2]:
        if not(0 >= K11 + i >= 7): continue
        for j in [-2, -1, 1 ,2]:
            if (abs(i) == abs(j)): continue
            if not(0 >= K12 + j >= 7): continue
            try: startboard[K11 + i].remove(K12 + j)
            except: 0
    for i in [-2, -1, 1, 2]:
        if not(0 >= p1 + i >= 7): continue
        for j in [-2, -1, 1 ,2]:
            if (abs(i) == abs(j)): continue
            if not(0 >= p2 + j >= 7): continue
            try: startboard[p1 + i].remove(p2 + j)
            except: 0
    for i in [-2, -1, 1, 2]:
        if not(0 >= p3 + i >= 7): continue
        for j in [-2, -1, 1 ,2]:
            if (abs(i) == abs(j)): continue
            if not(0 >= p3 + j >= 7): continue
            try: startboard[p3 + i].remove(p4 + j)
            except: 0

    h1 = random.randint(0, len(startboard)-1)
    h2 = startboard[h1][random.randint(0, len(startboard[h1])-1)]
    h = [h1, h2]

    Board[b1[0]][b1[1]] = 'B1'
    Board[b2[0]][b2[1]] = 'B1'
    Board[k1[0]][k1[1]] = 'K1'
    Board[k2[0]][k2[1]] = 'K0'
    Board[h[0]][h[1]] = 'H0'


def DrawBg():
    pygame.draw.rect(wind, (181, 136, 99), (0, 0, 640, 640))
    for R in RectList:
        pygame.draw.rect(wind, ((240, 217, 181)), R)

def DrawPieces():
    y=0
    for Brd in Board:
        x=0
        for B in Brd:
            if Board[y][x]!='.':
                wind.blit(transform.scale(pygame.image.load(Board[y][x]+'.png'),(70,70)),(5+x*80,5+y*80))
            x+=1
        y+=1

def CheckShah(B_W): #аргумент B_W принимает значение 0 или 1. 0-Если интересует шах белого короля, 1-если черного
    y=0
    for Brd in Board: #проверка каждой строки
        x=0
        for B in Brd: #проверка каждой клетки строки
            if B!='.': #если клетка не пуста
                if B[1]!=B_W: #если найденая фигура противоположного цвета с проверяемым королём и соответственно может его атаковать
                    
                    for shift in AttackDict[B[0]][0:-1]: #shift-направление аттаки, числа показывающие сдвиг по X и Y
                        pos=[x,y] #позиция найденной фигуры
                        for i in range(AttackDict[B[0]][-1]*6+1): #если аттака во всё поле, то цикл повториться 7 раз, иначе-1 раз.
                            pos[0]+=shift[0]
                            pos[1]+=shift[1]#сместим расматриваемую позицию в соответствии с shift
                            if pos[0]>7 or pos[0]<0 or pos[1]>7 or pos[1]<0: break #если X или Y рассматриваемой позиции выходит за пределы поля, то остановить проверку этого направления атаки
                            if Board[pos[1]][pos[0]]!='.':
                                if Board[pos[1]][pos[0]]!='K'+B_W: break #если поле не пустое и на нём не стоит вражеский король, то остановить проверку этого направления атаки
                                else: return True #если король в клетке всё же есть-вернуть True. Король действительно под шахом
            x+=1
        y+=1
    return False #если шах так и не был обнаружен, вернуть False

def ShowVariants(x,y): #x,y-координаты фигуры для которой нужно определить ходы
    global Variants
    Variants=[] #список вариантов ходов
    B=Board[y][x] #B-фигура для которой нужно определить ходы
    for shift in AttackDict[B[0]][0:-1]:#уже знакомый shift-сдвиг
        pos=[x,y] #а также знакомая позиция фигуры-pos
        for i in range(AttackDict[B[0]][-1]*6+1): #если аттака во всё поле, то цикл повториться 7 раз, иначе-1 раз.
            pos[0]+=shift[0]
            pos[1]+=shift[1]#опять смещаем позицию с помощью shift
            if pos[0]>7 or pos[0]<0 or pos[1]>7 or pos[1]<0: break #если X или Y рассматриваемой позиции выходит за пределы поля, то остановить проверку этого направления
            if Board[pos[1]][pos[0]]!='.': #если клетка не пуста
                if Board[pos[1]][pos[0]][1]!=Board[y][x][1]: Variants.append([pos[0],pos[1]]); break #если клетку занимает вражеская фигура то добавить её как вариант хода и остановить проверку этого направления
                else: break #если же клетку заняла дружеская фигура, то остановить эту линию ходов
            elif B[0]!='p' and B[0]!='P': #если клетка пуста, а рассматриваемая фигура не пешка то добавить её как вариант хода. (Пешка не может атаковать пустую клетку)
                Variants.append([pos[0],pos[1]])
    #Теперь дело за малым-откинуть все ходы, которые ставят своего короля под шах
    
    ForDeletion=[] #список вариантов на удаление
    Board[y][x]='.' #временно уберем рассматриваемую фигуру со стола
    for V in Variants: #переберем все варианты
        remember=Board[V[1]][V[0]] #запоминаем клетку, на которую сейчас поставим фигуру
        Board[V[1]][V[0]]=B #ставим фигуру на это место
        if CheckShah(B[1]): ForDeletion.append(V) #если король под шахом-добавим этот вариант в список на удаление
        Board[V[1]][V[0]]=remember #возвращаем клетку которую запомнили
    Board[y][x]=B #вернём рассматриваемую фигуру на стол
    for Del in ForDeletion: #удалим все недопустимые варианты
        Variants.remove(Del)
    
    if Board[y][x]=='K0': #если рассматриваем ходы для белого короля
        global castlingL0, castlingR0
        if Board[7][0:5]==['R0','.','.','.','K0'] and castlingL0: #если между левой ладьёй и королём пусто, а рокировка с левой ладьёй не запрещена
            Board[7][2],Board[7][3]='K0','K0' #временно поставим два короля в клетки через которые пройдёт король
            if CheckShah('0')==0: #если эти короли не получают шаха, то это значит, что все условия для рокировки есть и можно добавлять ход-рокировку
                Variants.append([2,7])
            Board[7][2],Board[7][3]='.','.' #уберём временных королей
        
        if Board[7][4:8]==['K0','.','.','R0'] and castlingR0: #все тоже самое для рокировки с правой ладьёй
            Board[7][5],Board[7][6]='K0','K0'
            if CheckShah('0')==0:
                Variants.append([6,7])
            Board[7][5],Board[7][6]='.','.'
    if Board[y][x]=='K1':
        global castlingL1, castlingR1
        if Board[0][0:5]==['R1','.','.','.','K1'] and castlingL1:
            Board[0][2],Board[0][3]='K1','K1'
            if CheckShah('1')==0:
                Variants.append([2,0])
            Board[0][2],Board[0][3]='.','.'
        
        if Board[0][4:8]==['K1','.','.','R1'] and castlingR1:
            Board[0][5],Board[0][6]='K1','K1'
            if CheckShah('1')==0:
                Variants.append([6,0])
            Board[0][5],Board[0][6]='.','.'
    

def CheckCheckMate(B_W): #аргумент B_W-как обычно, 0-интерисует мат/пат белых, 1-черных
    global Variants
    y=0
    for Brd in Board: #проверка каждой строки
        x=0
        for B in Brd: #проверка каждого элемента строки
            if B[-1]==B_W: #если найдена фигура нужного цвета то проверить, есть ли для неё хоть один вариант хода. Если да-вернуть 0-мата/пата нет
                ShowVariants(x,y)
                if len(Variants)>0:Variants=[];return 0
            x+=1
        y+=1
    #если дошли до этой строки, то это значит, что ни одна фигура нужного цвета не может сделать ход. Это значит что поставлен мат или пат
    if CheckShah(B_W): Variants=[];return 1 #король под шахом-значит мат, возвращаем 1
    else: Variants=[];return 2 #король не под шахом-пат возвращаем 2
    #обратите внимание что перед тем как вернуть значение, необходимо очистить список Variants, чтобы избежать багов

Variants=[]
MakeBoard()
DrawBg()
DrawPieces()
Turn=0
game=1
check=0
castlingL0,castlingR0=True,True
castlingL1,castlingR1=True,True

while game:
    for e in event.get():
        if e.type==QUIT:
            game=0
        
        if e.type==pg.MOUSEBUTTONDOWN and e.button==1: #если нажата ЛКМ
            x,y=(e.pos) #x,y-положение мыши
            x,y=math.floor(x/80),math.floor(y/80) #поделив x,y на 80 получаем клетку, на которую нажал игрок
            if Board[y][x]!='.': #если она не пуста
                if Board[y][x][1]==str(Turn): #и равна переменной Turn-очередь. Turn меняется каждый ход
                    ShowVariants(x,y) #получаем список доступных ходов
                    remember=[x,y] #запомним клетку на которую нажали
                    for V in Variants:
                        pygame.draw.circle(wind, (200,200,200), (V[0]*80+40, V[1]*80+40), 10) #отрисовка кружочков показывающих, куда можно сходить

        if e.type==pg.MOUSEBUTTONUP and e.button==1 and Turn!=-1 and Turn!=-2: #если ОТжата ЛКМ
            x,y=(e.pos)
            x,y=math.floor(x/80),math.floor(y/80) #получаем клетку в которой находиться мышка
            if Variants.count([x,y]): #если эта клетка есть в списке возможных ходов
                
                Board[y][x]=Board[remember[1]][remember[0]] #заменяем выбранную клетку на ту что запомнили при нажатии
                Board[remember[1]][remember[0]]='.' #клетку с которой ушли оставляем пустой

                if remember==[4,7] and Board[y][x]=='K0':
                    if [x,y]==[2,7]: Board[7][0]='.';Board[7][3]='R0'
                    if [x,y]==[6,7]: Board[7][7]='.';Board[7][5]='R0'
                if remember==[4,0] and Board[y][x]=='K1':
                    if [x,y]==[2,0]: Board[0][0]='.';Board[0][3]='R1'
                    if [x,y]==[6,0]: Board[0][7]='.';Board[0][5]='R1'

                if Board[7][0]!='R0': castlingL0=False #если левая ладья не на месте, запретить делать с ней рокировку
                if Board[7][7]!='R0': castlingR0=False #если правая ладья не на месте, запретить делать с ней рокировку
                if Board[7][4]!='K0': castlingL0=False;castlingR0=False #если король не на месте, запретить делать рокировку впринципе
                if Board[0][0]!='R1': castlingL1=False
                if Board[0][7]!='R1': castlingR1=False
                if Board[0][4]!='K1': castlingL1=False;castlingR1=False
                Turn=1-Turn #очередь меняется с 0 на 1 или наоборот
                #после смены очереди надо проверить наличие мата или пата
                check=CheckCheckMate(str(Turn)) #check примет 1 если объявлен мат, 2-если пат, 0-в ином случае
                if check==1: #если мат
                    DrawBg()#рисуем доску напоследок
                    DrawPieces()
                    if Turn==0:#и в зависимости от того чья очередь, объявляем победителя
                        wind.blit(pygame.font.SysFont(None,30).render('BLACK WON', False,(30, 30, 30)),(260,310))
                    if Turn==1:
                        wind.blit(pygame.font.SysFont(None,30).render('WHITE WON', False,(30, 30, 30)),(260,310))
                if check==2: #если пат то объявляем ничью
                    wind.blit(pygame.font.SysFont(None,30).render('DRAW', False,(30, 30, 30)),(290,310))
                Variants=[]
            if check==0:
                DrawBg()
                DrawPieces()
            Variants=[]
    display.update()
    clock.tick(60)
