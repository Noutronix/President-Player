
import random as rd 
import matplotlib.pyplot as plt


class computer:
    def __init__(self, cards, pl, rank):
        self.cards = cards
        self.placement = pl
        self.rank = rank


class player:
    def __init__(self, cn: int, pl, rank: float, parent):
        self.card_number = cn
        self.placement = pl
        self.rank = rank
        self.parent = parent
        self.probabilities = []







class game:
    def __init__(self):
        self.cards_left = [x for x in ["3", "4","5" ,"6" ,"7", "8", "9", "10", "j", "q", "k", "a", "2"] for y in range(4)]
        self.cards_left += ["J", "J"]

        self.players = []

        self.winner = None
    


    
    def setup(self):
        cards = input("cards: ") #format: 1-10 for cards, j,q,k,a for face cards and J for joker; comma-separated
        cards = cards.replace(" ", "").split(",")

        self.start = (True if input("first round? ") == "y" else False) #format: y for true and n for false

        pl = int(input("computer turn number: ")) #counting from 0

        

        if self.start == False:
            players = input("players: ").replace(" ", "").split(",") #format: list order is the turn order and number values are the rankings; comma-separated 
            #note: include computer with the players; input starts at 0 for player ranks
            cl = 54%len(players) #extra cards


            for num, r in enumerate(players):
                if num == pl:
                    self.players.append(computer(cards, num, r)) 
                else:
                    self.players.append(player(
                        54//len(players)+(1 if cl > 0 else 0),
                        num, r))
                cl -= 1
        
        else: 
            pnum = int(input("number of players: "))
            cl = 54%pnum

            for num in range(pnum):
                if num == pl:
                    self.com = computer(cards, num, None)
                    self.players.append(self.com)

                else:
                    self.players.append(player(
                        54//pnum+(1 if cl > 0 else 0),
                        num, None))
                cl -= 1

        for i in self.com.cards:
            self.cards_left.remove(i)

    

    def play(self):
        self.setup()
        
        for p in self.players:
            if isinstance(p, player):
                for i in self.cards_left:
                    p.probablilies[i] = p.card_number/self.cards_left

        if self.start == False:
            #include what the computer gave as well
            pl = sorted(self.players, key=lambda x:x.rank)

            if len(self.players) == 3:
                if self.com.rank == 2 or self.com.rank == 0: #bum or pres
                    T = len(self.cards_left)
                    cg = input("card given: ").replace(" ", "").split(",")
                    ct = input("card taken: ").replace(" ", "").split(",")
                    a = [self.com.rank] #computer rank
                    b = [abs(self.com.rank+2-4)] #trading player rank
                   
                    pl[b].probabilities = [[self.cards_left[x], pl[b].card_number/T] for x in range(len(self.cards_left))] 
                    pl[b].probabilities = [i if i[0] != cg else [i[0], 1] for i in pl[b].probabilities] 
                        #all probabilities stay the same except the one the com gives which is 100%

                    pl[1].probabilities = [[self.cards_left[x], pl[1].card_number/T] for x in range(len(self.cards_left))] #neutral
                    pl[a].cards = pl[a].cards[1:].append(ct) #com
                
                else: #neutral
                    T = len(self.cards_left)
                    A = [pl[0].card_number/T for x in range(T)]
                    B = [pl[2].card_number/T for x in range(T)]
                    result = calculate(A, B, T)
                    
                    pl[0].probabilities = [[self.cards_left[x], A[x]+result[x]-result[-x-1]] for x in range(T)]
                    pl[2].probabilities = [[self.cards_left[x], B[x]-result[x]+result[-x-1]] for x in range(T)]         

            elif len(self.players) == 4:
                if self.com.rank == 1 or self.com.rank == 2: #vice president or vice bum
                    
                    a = self.com.rank
                    b = (2 if self.com.rank == 1 else 1)

                    T = len(self.cards_left)
                    cg = input("card given: ").replace(" ", "").split(",")
                    ct = input("card taken: ").replace(" ", "").split(",")
                   
                    pl[b].probabilities = [[self.cards_left[x], pl[b].card_number/T] for x in range(len(self.cards_left))] 
                    pl[b].probabilities = [i if i[0] != cg else [i[0], 1] for i in pl[b].probabilities] 
                        #all probabilities stay the same except the one the com gives which is 100%
                    pl[a].cards = pl[a].cards[1:].append(ct) #com

                    for i in range(2):
                        result = calculate(pl[0].probabilities, pl[3].probabilities, T)
                        pl[0].probabilities = [pl[0].probabilities[x]+result[x]-result[-x-1] for x in range(T)]
                        pl[3].probabilities = [pl[3].probabilities[x]-result[x]+result[-x-1] for x in range(T)] 
                    pl[0].probabilities = [[self.cards_left[x], pl[0].probabilities[x]] for x in range(T)]
                    pl[3].probabilities = [[self.cards_left[x], pl[3].probabilities[x]] for x in range(T)]
                        
            
            elif len(self.players) >= 5:
                pass
            
            #assessments

            for num in range(len(self.cards_left)):
                if sum([x.probabilities[1] for x in self.players if isinstance(x, player)]) != 1:
                    raise ValueError

            for pl in self.players:
                if i != self.com:
                    for num in range(len(self.cards_left)-1):
                        if pl.probabilities[num][1] < pl.probabilities[num+1][1]:
                            raise ValueError

            
            
    



            


        while self.winner == None:
            for p in self.players:
                turn = input() #format: card * number of cards (ex: AA for two aces, 9 for one 9)

def calculate(A, B, T):
    #A and B are probability values for all cards; T is the number of cards
    if  len(A) > 0 and len(B) > 0 and T > 0:
        R = 1-(A[0]+B[0])
        results = [(A[0]+R)*x for x in calculate(A[1:], B[1:], T-1)]
        return [B[0]]+results
    else:
        return [0 for i in range(T)]

    

game().play()




        
