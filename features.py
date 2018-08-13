from time import time
from concurrent.futures import ProcessPoolExecutor
def gcd(pair):
    a,b = pair
    low = min(a,b)
    for i in range(low,0,-1):
        if a %i==0 and b%i==0:
            return i

if __name__=='__main__':
    numbers = [(1727727,2324243),(72637332,23424324324),
               (1526232,234342323443),(2773332,2322332)]
    pool = ProcessPoolExecutor(max_workers=8)
    start = time()
    results = list(pool.map(gcd,numbers))
    end = time()
    print('%.3f' %(end-start))
