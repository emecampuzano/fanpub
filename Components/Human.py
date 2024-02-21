import random
from time import sleep as wait

# Eventually, I'll add a class that simulates human behaviour to avoid
# being detected by the website. For now, It's just this.

def randomWait():
    '''
    Waits
    '''
    randomTime = random.randint(4,6)
    randomTime = randomTime / 10
    wait(randomTime)