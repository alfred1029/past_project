import random
import copy
def initCard():
    count = 0
    while True:
        initialCard = random.sample(range(52),52)   # random 52 unique digits in 1-52
        initCardList = []                           # stores randomized deck with information
        for card in initialCard:
            convertSuit = {0:"D",1:"C",2:"H",3:"S"} #♦♣♥♠
            suit = convertSuit[card // 13]          
            rank = card % 13 + 1
            opened = False                          # whether the card has been opened
            initCardList.append([suit, rank, opened])
        #print(sum([initCardList[i][1] for i in range(24,52)]),count)
        count += 1
        if sum([initCardList[i][1] for i in range(24,52)]) in range(196,205):   # 196 is median, range 112-280
            break   
    #print(initCardList)
    columns = []
    deck = initCardList[:24]
    initCardList = initCardList[24:]            # remove deck cards
    columns.append(deck)                        # column 0 is deck
    for column in range(1,8):
        columns.append(initCardList[:column])
        initCardList = initCardList[column:] 
    for column in range(1,8):
        columns[column][-1][-1] = True
    #print(columns)
    piles = [0,0,0,0]                           # piles
    return columns,piles

def generateGUI(columns,piles,score,move_count):
    color = 34
    dim = 157
    print(f'\u001b[7m{"#"*21}\u001b[0m\u001b[48;5;226m SCORE: {score:>4} MOVES: {move_count:>3} \u001b[0m\u001b[7m{"#"*21}\u001b[0m')
    DeckImage = ["╭╌╌╌╌╮","┊🃏🃏┊","┊🃏🃏┊","┊🃏🃏┊","╰╌╌╌╌╯"]
    pilesImage = ["\033[91m╭╌╌╌╌╮\033[0m","\033[91m┊    ┊\033[0m","\033[91m┊    ┊\u001b[48;5;34m","\033[91m┊    ┊\u001b[48;5;34m","\033[91m╰╌╌╌╌╯\u001b[0m","╭╌╌╌╌╮","┊    ┊","┊    ┊\u001b[0m","┊    ┊\u001b[0m","╰╌╌╌╌╯"]*2
    print(f"\u001b[48;5;{color}m ╰╌╌╌╌╯  " + "╰╌╌╌╌╯ "*7 + " ╰╌╌╌╌╯ \u001b[0m")
    columns2 = copy.deepcopy(columns[1:])
    for col in columns2:
        for cards in col:
            cards.append(0)                      # card printed how many lines counter
    deck = []
    for i in range(len(columns[0])):
        if columns[0][::-1][i][2] == True:
            deck.append(copy.deepcopy(columns[0][::-1][i]))
    for cards in deck:
        cards.append(0)
    convertSyms = {"D":"♦","C":"♣","H":"♥","S":"♠"}
    convertRank = ["","A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
    convertSuit = {0:"D",1:"C",2:"H",3:"S"}
    pilesPrinted = 0
    deckPrinted = 0
    shrinkMode = 17
    deckLimit = 0
    red = ""
    for card in deck:
        if card[2]:
            deckLimit += 1
    if deckLimit != 0:  deckLimit = deckLimit*2+2
    printedLines = 0
    for lines in range(20):         # for every card(a list), there are four values: suit, rank, opened, printed
        if len(DeckImage) > 0:
            print(f"\u001b[48;5;{color}m \u001b[0m"+DeckImage.pop(0),end=f"\u001b[48;5;{color}m  \u001b[0m")
        elif len(deck) > 0:
            for i in range(len(deck)):
                if deck[i][0] in "DH" and deck[i][2]:
                    print("\033[91m",end="")
                    red = "\033[91m"
                else:
                    print("\033[0m",end="")
                    red = ""
                if deck[i][3] == 5:
                    if deck[-1][3] == 5:
                        print(f"\u001b[48;5;{color}m       ",end=f"\u001b[48;5;{color}m  \u001b[0m")
                        break
                    continue
                if deck[i][3] == 0:
                    print(f"\u001b[48;5;{color}m \u001b[0m{red}╭╌╌╌╌╮",end=f"\u001b[48;5;{color}m  \u001b[0m")
                    deck[i][3] += 1
                    break
                if deck[i][3] == 4:
                    print(f"\u001b[48;5;{color}m \u001b[0m{red}╰╌╌╌╌╯",end=f"\u001b[48;5;{color}m  \u001b[0m")
                    deck[i][3] += 1
                    break
                if deck[i][3] == 1:
                    print(f"\u001b[48;5;{color}m \u001b[0m{red}┊{convertRank[deck[i][1]]:^2} {convertSyms[deck[i][0]]}┊\033[0m",end=f"\u001b[48;5;{color}m  \u001b[0m")
                    deck[i][3] += 1
                    if i+1 != len(deck):
                        deck[i][3] = 5
                    break
                if deck[i][3] >= 2:
                    print(f"\u001b[48;5;{color}m \u001b[0m{red}┊    ┊",end=f"\u001b[48;5;{color}m  \u001b[0m")
                    deck[i][3] += 1
                    break
        else:
            print(f"\u001b[48;5;{color}m       ",end=f"  \u001b[0m")
        for col in columns2:
            if len(col) == 0:
                print(f"\u001b[48;5;{color}m      ",end=f"\u001b[48;5;{color}m ")
            for i in range(len(col)):
                if col[i][0] in "DH" and col[i][2]:
                    print("\u001b[0m\033[91m",end="")
                else:
                    print("\u001b[0m\033[0m",end="")
                if col[i][3] == 5:
                    if col[-1][3] == 5:
                        print(f"\u001b[48;5;{color}m      ",end=f"\u001b[48;5;{color}m ")
                        break
                    continue
                if col[i][3] == 0:
                    if i > 0 and (len(col)*2 - i + 1> shrinkMode):
                        if col[i][2]:
                            print(f"┊\033[4m{convertRank[col[i][1]]:^2} {convertSyms[col[i][0]]}\033[0m{red}┊\033[0m",end=f"\u001b[48;5;{color}m ")
                        else: print(f"\033[0m\u001b[48;5;{dim}m┊\033[4m🃏🃏\033[0m\u001b[48;5;{dim}m┊\u001b[0m",end=f"\u001b[48;5;{color}m ")
                        col[i][3] = 5
                        break
                    if not col[i][2]:
                        print(f"\u001b[48;5;{dim}m╭╌╌╌╌╮\u001b[0m",end=f"\u001b[48;5;{color}m ")
                        col[i][3] += 1
                        break
                    print("╭╌╌╌╌╮",end=f"\u001b[48;5;{color}m ")
                    col[i][3] += 1
                    break
                if col[i][3] == 4:
                    print("╰╌╌╌╌╯",end=f"\u001b[48;5;{color}m ")
                    col[i][3] += 1
                    break
                if col[i][3] == 1:
                    if len(col)*2 - i + 1> shrinkMode:
                        if col[i][2]:
                            print(f"┊\033[4m{convertRank[col[i][1]]:^2} {convertSyms[col[i][0]]}\033[0m{red}┊\033[0m",end=f"\u001b[48;5;{color}m ")
                        else: print(f"\u001b[48;5;{dim}m┊\033[4m🃏🃏\033[0m\u001b[48;5;{dim}m┊\033[0m",end=f"\u001b[48;5;{color}m ")
                        col[i][3] = 5
                        break
                    if col[i][2]:
                        print(f"┊{convertRank[col[i][1]]:^2} {convertSyms[col[i][0]]}┊\033[0m",end=f"\u001b[48;5;{color}m ")
                        col[i][3] += 1
                    else:
                        print(f"\u001b[48;5;{dim}m┊🃏🃏┊\033[0m",end=f"\u001b[48;5;{color}m ")
                        col[i][3] += 1
                    if i+1 != len(col):
                        col[i][3] = 5
                    break
                if col[i][3] >= 2:
                    print("┊    ┊",end=f"\u001b[48;5;{color}m ")
                    col[i][3] += 1
                    break

        print("\033[0m",end="")
        if len(pilesImage) > 0:
            if pilesImage[0] == "┊    ┊":  
                print(f"\u001b[48;5;{color}m \u001b[0m┊{convertRank[piles[pilesPrinted]]:^2} {convertSyms[convertSuit[pilesPrinted]]}┊\u001b[48;5;{color}m ",end="")
                pilesImage.pop(0)
                pilesPrinted += 1               
            elif pilesImage[0] == "\033[91m┊    ┊\033[0m":  
                print(f"\u001b[48;5;{color}m \u001b[0m\033[91m┊{convertRank[piles[pilesPrinted]]:^2} {convertSyms[convertSuit[pilesPrinted]]}┊\u001b[48;5;{color}m \033[0m",end="")
                pilesImage.pop(0)
                pilesPrinted += 1
            else:   print(f"\u001b[48;5;{color}m \u001b[0m" + pilesImage.pop(0) + f"\u001b[48;5;{color}m ",end="")

        print("\033[0m")
    print(f"\u001b[48;5;{color}m ╭╌╌╌╌╮  " + "╭╌╌╌╌╮ "*6 + f"╭╌╌╌╌╮\u001b[48;5;{color}m  " + "╭╌╌╌╌╮ \u001b[0m")
    #print(f'\u001b[48;5;{color}m{"#"*64:^{64}}\u001b[0m')
    print(f'\u001b[7m{"#"*21}\u001b[0m\u001b[37;3;101m SOLITAIRE 1330 PROJECT \u001b[0m\u001b[7m{"#"*21}\u001b[0m')
