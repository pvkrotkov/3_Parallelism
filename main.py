from multiprocessing import Process, Pool, Queue
import time
from random import randint



#make 2 matrices and put them to queue
def matrix_generator(size, q):
    while True:
        a = [[randint(1, 100)for j in range(size)] for i in range(size)]
        b = [[randint(1, 100)for j in range(size)] for i in range(size)]
        c = [a, b]
        for i in c:
            q.put(i)
        time.sleep(4)

#func for calculating matrices values
def func_for_calc(index, A, B, size):
    i, j = index
    res = 0
    for k in range(size):
        res += A[i][k] * B[k][j]
    return res

#create pool for matrix processing and open new files
def for_pool(size, q):
    with Pool(processes=2) as pool:
        count = 1
        while not q.empty():
            m1 = q.get()
            m2 = q.get()
            a = [m1, m2]
            m3 = [[]for i in range(size)]
            for index, i in enumerate(a):
                inp = open(f'{count}in{index+1}.txt', 'w')
                for j in i:
                    inp.write(' '.join(map(str, j))+'\n')
                inp.close()
            with open(f'{count}temp.txt', 'w') as temp:
                for i in range(size):
                    for j in range(size):
                        result = pool.apply_async(
                            func_for_calc, ((i, j), m1, m2, size))
                        res = result.get()
                        temp.write(str(res)+' ')
                        m3[i].append(res)
                    temp.write('\n')
            r = open(f'{count}result.txt', 'w')
            for i in m3:
                r.write(' '.join(map(str, i))+'\n')
            r.close()
            count += 1
            time.sleep(4)

#main part 
if __name__ == '__main__':
    size = 10
    q = Queue()
    proc_generator = Process(target=matrix_generator, args=(size, q))
    proc_pool = Process(target=for_pool, args=(size, q))
    proc_generator.daemon = True
    proc_generator.start()
    proc_pool.start()
    if input('"q" for exit: ') == 'q':
        raise SystemExit