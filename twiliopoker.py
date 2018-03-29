import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import os
import sys
import json
import math
from twilio.rest import Client

def textme(to, message='no message'):
    #assumes you have a text file in the same directory called "keys.txt" that has all the relevant stuff in a json-dumped dictionary
    file = open('keys.txt', 'r') 
    k=json.loads(file.read())
    file.close()
    account_sid = k['account_sid']
    auth_token = k['auth_token']
    from_ = k['from_']
    client = Client(account_sid, auth_token)
    client.messages.create(to=to, from_=from_, body=message)
    


def numbertocard(x):
    if x%4==1:
        name=" of Clubs"
    if x%4==2:
        name=" of Diamonds"
    if x%4==3:
        name=" of Hearts"
    if x%4==0:
        name=" of Spades"
    f=[1, 2, 3, 4]
    if x in f:
        name="2"+name
        return name
    if x in [x+4 for x in f]:
        name="3"+name
        return name
    if x in [x+8 for x in f]:
        name="4"+name
        return name
    if x in [x+12 for x in f]:
        name="5"+name
        return name
    if x in [x+16 for x in f]:
        name="6"+name
        return name
    if x in [x+20 for x in f]:
        name="7"+name
        return name
    if x in [x+24 for x in f]:
        name="8"+name
        return name
    if x in [x+28 for x in f]:
        name="9"+name
        return name
    if x in [x+32 for x in f]:
        name="10"+name
        return name
    if x in [x+36 for x in f]:
        name="Jack"+name
        return name
    if x in [x+40 for x in f]:
        name="Queen"+name
        return name
    if x in [x+44 for x in f]:
        name="King"+name
        return name
    if x in [x+48 for x in f]:
        name="Ace"+name
        return name
    print("error: bad input to numbertocard: "+str(x))

def showcardimages(listofcards):
    l=len(listofcards)
    rows=math.ceil(l/5)
    plt.rcParams["figure.figsize"]=[14,4*rows]
    for i in range(0,l):
        plt.subplot(rows, 5, i+1)
        plt.axis('off')
        img=mpimg.imread('PNGcards/'+str(listofcards[i])+'.png')
        plt.imshow(img)
    plt.show()

def cleanup(handnumber, players, hands, deck, flop, turn, river):
    #overwrite secondtolast with last
    if os.path.isfile('lasthand.txt'):
        file = open('lasthand.txt', 'r') 
        k=json.loads(file.read())
        file.close()
        file = open('secondtolasthand.txt','w') 
        file.write(json.dumps(k))
        file.close() 
    #save current data to last
    handdict = dict([('handnumber', handnumber), 
             ('players', players), 
             ('hands', hands),
             ('deck', deck),
             ('flop', flop),
             ('turn', turn),
             ('river', river)])
    file = open('lasthand.txt','w') 
    file.write(json.dumps(handdict))
    file.close() 
    return

def revealspecifiedholecards(players, hands, flop, turn, river):
    a=''
    while a!='b':
        print('Players in hand:')
        print(players)
        print('Name of player to reveal hole cards, or b for back:')
        a=input()
        if a in players:
            showcardimages(flop+[turn, river]+hands[a])

def prefloproutine(handnumber, players, hands, deck):
    a=''
    while a != 'f':
        print('Hand #'+str(handnumber)+'. Hole cards have been dealt. Action?')
        print('f = flop, e = end hand, s = reveal specified hole cards')
        a=input()
        if a=='e':
            cleanup(handnumber, players, hands, deck, '', '', '')
            return 
        if a=='s':
            revealspecifiedholecards(players, hands, [53, 53, 53], 53, 53)
    flop=deck[0:3]
    deck=deck[3:]
    floproutine(handnumber, players, hands, deck, flop)

def floproutine(handnumber, players, hands, deck, flop):
    showcardimages(flop)
    a=''
    while a != 't':
        print('Hand #'+str(handnumber)+'. Flop has been dealt. Action?')
        print('t = turn, e = end hand, s = reveal specified hole cards')
        a=input()
        if a=='u':
            deck=flop+deck
            random.shuffle(deck)
            prefloproutine(handnumber, players, hands, deck)
            return
        if a=='e':
            cleanup(handnumber, players, hands, deck, flop, '', '')
            return 
        if a=='s':
            revealspecifiedholecards(players, hands, flop, 53, 53)
    turn=deck[0]
    deck=deck[1:]
    turnroutine(handnumber, players, hands, deck, flop, turn)    
    
def turnroutine(handnumber, players, hands, deck, flop, turn):
    showcardimages(flop+[turn])
    a=''
    while a != 'r':
        print('Hand #'+str(handnumber)+'. Turn has been dealt. Action?')
        print('r = river, e = end hand, s = reveal specified hole cards')
        a=input()
        if a=='u':
            deck=[turn]+deck
            random.shuffle(deck)
            floproutine(handnumber, players, hands, deck, flop)
            return
        if a=='e':
            cleanup(handnumber, players, hands, deck, flop, turn, '')
            return 
        if a=='s':
            revealspecifiedholecards(players, hands, flop, turn, 53)
    river=deck[0]
    deck=deck[1:]
    riverroutine(handnumber, players, hands, deck, flop, turn, river) 

def riverroutine(handnumber, players, hands, deck, flop, turn, river):
    showcardimages(flop+[turn]+[river])
    deck2=deck
    a=''
    while True:
        print('Hand #'+str(handnumber)+'. River has been dealt. Action?')
        print('e = end hand, s = reveal specified hole cards')
        a=input()
        if a=='u':
            deck=[river]+deck
            random.shuffle(deck)
            turnroutine(handnumber, players, hands, deck, flop, turn)
            return
        if a=='e':
            cleanup(handnumber, players, hands, deck, flop, turn, river)
            return 
        if a=='s':
            revealspecifiedholecards(players, hands, flop, turn, river)
        if a=='x':
            showcardimages([deck2[0]])
            deck2=deck2[1:]

            
def twiliopoker(args):
    if args[0]=='resume':
        file = open(str(args[1])+'.txt', 'r') 
        k=json.loads(file.read())
        file.close()
        if k['flop']=='':
            prefloproutine(k['handnumber'],k['players'],k['hands'],k['deck'])
        elif k['turn']=='':
            floproutine(k['handnumber'],k['players'],k['hands'],k['deck'],k['flop'])
        elif k['river']=='':
            turnroutine(k['handnumber'],k['players'],k['hands'],k['deck'],k['flop'],k['turn'])
        else:
            riverroutine(k['handnumber'],k['players'],k['hands'],k['deck'],k['flop'],k['turn'],k['river'])
        return
    deck=list(range(1,53))
    random.shuffle(deck)
    #load last hand number
    #set handnumber to last hand number + 1
    #if last hand doesn't exist, set handnumber=1
    if os.path.isfile('lasthand.txt'):
        file = open('lasthand.txt', 'r') 
        k=json.loads(file.read())
        file.close()
        handnumber=k['handnumber']+1
    else:
        handnumber=1
    if args[0]=='training':
        hand=deck[0:2]
        deck=deck[2:]
        hands={}
        hands['training']=hand
        showcardimages(hand)
        prefloproutine(handnumber, ['training'], hands, deck)
        return
    #check for twilio account details file
    if not os.path.isfile('keys.txt'):
        print('error: no Twilio keys found')
        return
    #check for phone directory file      
    if not os.path.isfile('phonebook.txt'):
        print('error: no phonebook found')
        return
    players=list(set(args)) #This removes duplicate players
    #load phone directory
    file = open('phonebook.txt', 'r') 
    phonebook=json.loads(file.read())
    #check every player is in the phonebook
    for player in players:
        if player not in phonebook:
            print('error: '+player+' not in phonebook')
            return
    hands={}
    for player in players:
        hands[player]=deck[0:2]
        deck=deck[2:]
    #text everyone the hand number and their cards
    for player in players:
        message="Hand #"+str(handnumber)+": "+numbertocard(hands[player][0])+" and "+numbertocard(hands[player][1])
        textme(phonebook[player], message)
    prefloproutine(handnumber, players, hands, deck)
    
if __name__ == "__main__":
	args=sys.argv[1:]
	twiliopoker(args)