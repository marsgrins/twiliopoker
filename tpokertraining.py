import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import os
import sys
import json
import math
    


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

            
def tpokertraining():
    q=""
    while q=="":
     deck=list(range(1,53))
     random.shuffle(deck)
     hand=deck[0:2]
     deck=deck[2:]
     flop=deck[0:3]
     deck=deck[3:]
     turn=deck[0]
     deck=deck[1:]
     river=deck[0]
     deck=deck[1:]
     showcardimages(hand)
     showcardimages(flop+[53,53]+hand)
     showcardimages(flop+[turn,53]+hand)
     showcardimages(flop+[turn,river]+hand)
     print("Press enter for another hand, or type q to quit.")
     q=input()


    
if __name__ == "__main__":
	#args=sys.argv[1:]
	tpokertraining()