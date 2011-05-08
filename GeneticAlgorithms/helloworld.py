import time
import string
import random

GENES = "".join(map(lambda x, y: x+y, string.ascii_uppercase, string.ascii_lowercase)) + \
        string.punctuation + " "
GOAL = "Hello world! Genetic algorythms ver."

def fitness(chromosome):
    f = 0
    for index, gene in enumerate(chromosome):
        if gene != GOAL[index]:
            f -= 1
    return f

class GeneticCode:
    def __init__(self, dnk=""):
        if dnk == "":
            self.dnk = "".join(random.sample(GENES, len(GOAL)))
        else:
            self.dnk = dnk

    def get(self):
        return self.dnk

    def fitness(self):
        return fitness(self.dnk)
    
    def mutate(self, turns=5):
        _dnk = [item for item in self.dnk]
        for item in range(turns):
            rnd_elem_index = random.randint(0, len(_dnk)-1)
            if _dnk[rnd_elem_index] == GOAL[rnd_elem_index]:
                pass
            else:
                _dnk[rnd_elem_index] = random.choice(GENES)
        self.dnk = "".join(_dnk)

    def replicate(self, another_dnk):
        part = random.randint(0, len(self.dnk)-1)
        return "".join(self.dnk[0:part] + another_dnk.get()[part:])

class GenePool():
    pool_size = 100
    
    def __init__(self):
        self.pool = [GeneticCode() for item in range(self.pool_size)]

    def _print(self):
        for item in self.pool:
            print item.get() + " - " + str(item.fitness())

    def get_random(self):
        return self.pool[random.randint(0, len(self.pool)-1)]

    def darvin(self, winners=0.1):
        """
        choose only good dnk sequences
        winners - part of population to breed
        """
        all_fitness = [(item.fitness(), item) for item in self.pool]
        new_pool = [item[1] for item in
                    sorted(all_fitness, key=lambda x: x[0], reverse=True)]
        self.pool = new_pool[:int(round(self.pool_size * winners))]

        while len(self.pool) < self.pool_size:
            new_life = self.get_random().replicate(self.get_random())
            new_gc = GeneticCode(dnk=new_life)
            self.pool.append(new_gc)

    def evolution(self, turns=100):
        """Evalute pool"""
        iterations = 0
        while (iterations < turns) and (self.pool[0].get() != GOAL):
            for index, item in enumerate(self.pool):
                self.pool[index].mutate()
            self.darvin()
            print self.pool[0].get()
            time.sleep(0.1)
            iterations += 1
        return iterations

gp = GenePool()
print gp.evolution()
print "=========================="
#gp._print()
