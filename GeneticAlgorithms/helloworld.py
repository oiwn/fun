"""
Simple experement with Genetic Algorithms
Hello world via bunch of evolving strings.

theory http://en.wikipedia.org/wiki/Genetic_algorithm
"""
import sys
import time
import string
import random
import logging

from optparse import OptionParser

__version__ = "1.0"

logger = logging.getLogger('helloworld')

# form genetic codes
GENES = "".join(map(lambda x, y: x+y, string.ascii_uppercase, string.ascii_lowercase)) + \
        string.punctuation + " "

# goal string C.O.
GOAL = "Hello world! Genetic Algorithm ver."

def fitness(dnk, goal):
    """
    calculates how close is dnk to GOAL <<< this called "fitness function"
    f = 0 if conditions are satisfied
    """
    f = 0
    for index, gene in enumerate(dnk):
        if gene != goal[index]:
            f -= 1
    return f

def sample_wr(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result


class GeneticCode:
    def __init__(self, dnk="", goal=GOAL):
        if dnk == "":
            self.dnk = "".join(sample_wr(GENES, len(goal)))
        else:
            self.dnk = dnk
        self.goal = goal

    def get(self):
        return self.dnk

    def fitness(self):
        return fitness(self.dnk, self.goal)
    
    def mutate(self, turns=5):
        """
        mutate dnk sequence "on place"
        turns - how much elements will be changed
        """
        _dnk = list(self.dnk)
        for item in range(turns):
            rnd_elem_index = random.randint(0, len(_dnk)-1)
            if _dnk[rnd_elem_index] == self.goal[rnd_elem_index]:
                pass
            else:
                _dnk[rnd_elem_index] = random.choice(GENES)
        self.dnk = "".join(_dnk)

    def replicate(self, another_dnk):
        """
        breed 2 dnk sequences
        cut one, cut two and mix it together
        return offspring dnk string
        """
        part = random.randint(0, len(self.dnk)-1)
        return "".join(self.dnk[0:part] + another_dnk.get()[part:])


class GenePool():
    pool_size = 100
    
    def __init__(self, goal=GOAL):
        self.pool = [GeneticCode(goal=goal) for item in range(self.pool_size)]
        self.goal = goal

    def _print(self):
        for item in self.pool:
            print item.get() + " - " + str(item.fitness())

    def get_random(self):
        "Get random element from pool"
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
            new_gc = GeneticCode(dnk=new_life, goal=self.goal)
            self.pool.append(new_gc)

    def evolution(self, turns=1000):
        """Evalute pool"""
        iterations = 0
        while (iterations < turns) and (self.pool[0].get() != self.goal):
            for index, item in enumerate(self.pool):
                self.pool[index].mutate()
            self.darvin()
            logger.info(self.pool[0].get())
            time.sleep(0.1)
            iterations += 1
            
        return iterations


def main():
    usage = '%s [options] [text]' % sys.argv[0]
    parser = OptionParser(usage)
    parser.add_option('-l', '--log', default='-',
                      help='redirect logs to file')
    opts, args = parser.parse_args()

    if opts.log == '-':
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    else:
        logging.basicConfig(filename="helloworld.log", level=logging.INFO)

    if args:
        text = args[0]
    else:
        text = GOAL

    gp = GenePool(goal=text)
    #gp._print()
    steps = gp.evolution()
    logger.info("Steps: %d" % steps)
    

start_time = time.time()
main()
print
print "Estimatied time:\t%s" % (time.time() - start_time)
