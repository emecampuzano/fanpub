import random
from time import sleep as wait

def randomWait():
    '''
    Waits
    '''
    randomTime = random.randint(4,6)
    randomTime = randomTime / 10
    wait(randomTime)