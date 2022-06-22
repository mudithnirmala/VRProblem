from audioop import cross
import random

def writeToFile(N,mat):

    lines = []
    with open('out.txt','a') as file:
        lines.append(str(N)+'\n')
        file.writelines(str(N))

        for i in range(N):
            lines.append(' '.join(map(str,mat[i]))+'\n')
            
        file.writelines(lines)     


writeToFile(3,[[1, 23, 4],[2, "aa", 1],[2, "aa", 1]])


def crossover_2(c1,c2,n):
        a = random.randint(0,n-2)
        b = a + random.randint(int(n/3),int(2*n/3))

        offspring = []

        mid_set = c2[a:b+1]
        print("mid set",mid_set)
        free_des = [1]*(n+1)

        for x in mid_set:
            free_des[x]=0

        for i in range(0,n):
            if(free_des[c1[i]]):
                offspring.append(c1[i])
                free_des[c1[i]]=0
        print(offspring)
        offspring = offspring[:a]+mid_set+ offspring[a:]
        
        print(offspring)

crossover_2([1,2,3,4,5,6,7,8],[6,5,4,3,2,1,8,7],8)