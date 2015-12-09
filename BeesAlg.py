import random
import math

'''
    Bees Algorithm updated in 2009 by Pham et al
'''
class Patch:
    def __init__(self, scout, distance, dimensions):
        self.ngh = 1.0
        self.distance = distance
        self.dimensions = dimensions
        self.optima = scout
        self.stagnant = 0

    def shrink(self):
        self.ngh *= .8

    def abandon(self, newloc):
        self.ngh = 1.0
        self.optima = newloc
        self.stagnant = 0

    def search(self, function, count):
        workers = [[random.uniform(self.ngh*(self.optima[i]-self.distance), self.ngh*(self.optima[i]+self.distance))
                    for i in range(self.dimensions)] for j in range(count)]
        evaluation = [[function(x),x] for x in workers]
        evaluation.sort(reverse=True)
        if function(self.optima) < evaluation[0][0]:
            self.optima = evaluation[0][1]
            self.stagnant = 0
        else:
            self.stagnant += 1
            self.shrink()


class BeesAlg09:
    def __init__(self, population, sites, eliteSites, nsp, nep, ngh, stlim, interval, function, dimensions):
        self.population = population
        self.sites = sites
        self.eliteSites = eliteSites
        self.nsp = nsp
        self.nep = nep
        self.ngh = ngh
        self.stlim = stlim
        self.interval = interval
        self.function = function
        self.dimensions = dimensions
        self.patches = [Patch([random.uniform(interval[0],interval[1]) for j in range(dimensions)], ngh, dimensions) for i in range(self.population)]
        self.optima = None

    def evaluate(self):
        self.patches.sort(key=lambda x: self.function(x.optima), reverse=True)
        if self.optima == None or self.optima < self.patches[0].optima:
            self.optima = self.patches[0].optima


    def localSearch(self):
        for x in self.patches[:self.eliteSites]:
            x.search(self.function, self.nep)
            if x.stagnant >= self.stlim:
                x.abandon([random.uniform(self.interval[0],self.interval[1]) for i in range(self.dimensions)])
        for x in self.patches[self.eliteSites: self.sites]:
            x.search(self.function, self.nsp)
            if x.stagnant >= self.stlim:
                x.abandon([random.uniform(self.interval[0],self.interval[1]) for i in range(self.dimensions)])

    def globalSearch(self):
        for x in self.patches[self.sites:]:
            x.abandon([random.uniform(self.interval[0],self.interval[1]) for i in range(self.dimensions)])


'''
    Bees Algorithm proposed in 2005 by Pham et al
'''
class BeesAlg05:
    def __init__(self, population, sites, eliteSites, nsp, nep, radius):
        self.population = population
        self.sites = sites
        self.eliteSites = eliteSites
        self.nsp = nsp
        self.nep = nep
        self.radius = radius
        self.scouts = []
        self.siteList = None

    def populateScouts(self, interval, nv):
        self.scouts += [[random.uniform(interval[0], interval[1]) for j in range(nv)]
                        for i in range(self.population - len(self.scouts))]

    def recruit(self, nv):
        for x in self.siteList[:self.eliteSites]:
            for i in range(self.nep):
                x.append([random.uniform(x[0][j]-self.radius, x[0][j]+self.radius) for j in range(nv)])
        for x in self.siteList[self.eliteSites:]:
            for i in range(self.nsp):
                x.append([random.uniform(x[0][j]-self.radius, x[0][j]+self.radius) for j in range(nv)])

    def evaluate(self, function):
        evaluation = [[function(x),x] for x in self.scouts]
        evaluation.sort(reverse=True)
        self.siteList = [[evaluation[i][1]] for i in range(self.sites)]

    def evalSites(self, function):
        self.scouts = []
        for i in range(len(self.siteList)):
            evaluation = [[function(x),x] for x in self.siteList[i]]
            evaluation.sort(reverse=True)
            self.scouts += [evaluation[0][1]]

'''
    functions 1-8 from 'The Bees Algorithm - A Novel Tool for Complex Optimisation Problems'
'''
def deJong(x):
    return 3905.93 - 100 * (x[0]**2-x[1])**2-(1-x[0])**2

def goldsteinPrice(x):
    return -1*((1 + (x[0] + x[1] + 1)**2*(19-14*x[0]+3*x[0]**2-14*x[1]+6*x[0]*x[1]+3*x[1]**2))\
           *(30+(2*x[0]-3*x[1])**2*(18-32*x[0]+12*x[0]**2+48*x[1]-36*x[0]*x[1]+27*x[1]**2)))

def branin(x):
    a = 1
    b = 5.1/4*(7.0/22)**2
    c = 5*7.0/22
    d = 6
    e = 10
    f = 1.0/8*7.0/22
    return -1*(a*(x[1]-b*x[0]**2+c*x[0]-d)**2+e*(1-f)*math.cos(x[0])+e)

def martinGaddy(x):
    return -1*((x[0]-x[1])**2+((x[0]+x[1]-10)/3)**2)

def rosenbrock(x):
    return -1*(100*(x[0]**2-x[1])**2+(1-x[0])**2)

def rosenbrock2(x):
    res = 0
    for i in range(3):
        res += 100*(x[i]**2-x[i+1])**2+(1-x[i])**2
    return -1*res

def hyperSphere(x):
    return -1*(x[0]**2+x[1]**2+x[2]**2+x[3]**2+x[4]**2+x[5]**2)

def griewangk(x):
    sum = 0
    product = 1
    for i in range(10):
        sum += x[i]**2/4000
        product *= math.cos(x[i]/math.sqrt(i+1))
    return 1/(0.1+sum-product+1)

def functionsBeesAlg05():
    print 'bees alg 05'
    iter = 100
    shrink = 0.99
    #function #1 De Jong
    count = 0
    for i in range(iter):
        bees = BeesAlg05(10, 3, 1, 2, 4, 0.1)
        bees.populateScouts([-2.048,2.048], 2)
        bees.evaluate(deJong)
        while deJong(bees.scouts[0]) < (3905.93-0.001):
            bees.recruit(2)
            bees.evalSites(deJong)
            bees.populateScouts([-2.048,2.048], 2)
            bees.evaluate(deJong)
            bees.radius *= shrink
            count += 1
    print 'Function 1 De Jong mean number of evaluations'
    print count/iter

    #function #2 Goldstein and Price
    count = 0
    for i in range(iter):
        bees = BeesAlg05(20, 3, 1, 1, 13, 0.1)
        bees.populateScouts([-2,2], 2)
        bees.evaluate(goldsteinPrice)
        while goldsteinPrice(bees.scouts[0]) < (-3-0.001):
            bees.recruit(2)
            bees.evalSites(goldsteinPrice)
            bees.populateScouts([-2,2], 2)
            bees.evaluate(goldsteinPrice)
            bees.radius *= shrink
            count += 1
    print 'Function 2 Goldstein and Price mean number of evaluations'
    print count/iter

    #function #3 Branin
    count = 0
    for i in range(iter):
        bees = BeesAlg05(30, 5, 1, 2, 3, 0.5)
        bees.populateScouts([-5,10], 2)
        bees.evaluate(branin)
        while branin(bees.scouts[0]) < (-0.3977272*1.001):
            bees.recruit(2)
            bees.evalSites(branin)
            bees.populateScouts([-5,10], 2)
            bees.evaluate(branin)
            bees.radius *= shrink
            count += 1
    print 'Function 3 Branin mean number of evaluations'
    print count/iter

    #function #4 Martin and Gaddy
    count = 0
    for i in range(iter):
        bees = BeesAlg05(20, 3, 1, 1, 10, 0.5)
        bees.populateScouts([0,10], 2)
        bees.evaluate(martinGaddy)
        while martinGaddy(bees.scouts[0]) < (-0.001):
            bees.recruit(2)
            bees.evalSites(martinGaddy)
            bees.populateScouts([0,10], 2)
            bees.evaluate(martinGaddy)
            bees.radius *= shrink
            count += 1
    print 'Function 4 Martin and Gaddy mean number of evaluations'
    print count/iter

    #function #5a Rosenbrock
    count = 0
    for i in range(iter):
        bees = BeesAlg05(10, 3, 1, 2, 4, 0.1)
        bees.populateScouts([-1.2,1.2], 2)
        bees.evaluate(rosenbrock)
        while rosenbrock(bees.scouts[0]) < (-0.001):
            bees.recruit(2)
            bees.evalSites(rosenbrock)
            bees.populateScouts([-1.2,1.2], 2)
            bees.evaluate(rosenbrock)
            bees.radius *= shrink
            count += 1
    print 'Function 5a Rosenbrock mean number of evaluations'
    print count/iter

    #function #5b Rosenbrock
    count = 0
    for i in range(iter):
        bees = BeesAlg05(6, 3, 1, 1, 4, 0.5)
        bees.populateScouts([-10,10], 2)
        bees.evaluate(rosenbrock)
        while rosenbrock(bees.scouts[0]) < (-0.001):
            bees.recruit(2)
            bees.evalSites(rosenbrock)
            bees.populateScouts([-10,10], 2)
            bees.evaluate(rosenbrock)
            #bees.radius *= shrink
            count += 1
    print 'Function 5b Rosenbrock mean number of evaluations'
    print count/iter

    #function #7 Hyper Sphere
    count = 0
    for i in range(iter):
        bees = BeesAlg05(8, 3, 1, 1, 2, 0.3)
        bees.populateScouts([-5.12,5.12], 6)
        bees.evaluate(hyperSphere)
        while hyperSphere(bees.scouts[0]) < (-0.001):
            bees.recruit(6)
            bees.evalSites(hyperSphere)
            bees.populateScouts([-5.12,5.12], 6)
            bees.evaluate(hyperSphere)
            bees.radius *= shrink
            count += 1
    print 'Function 7 Hyper Sphere mean number of evaluations'
    print count/iter

    #function #6 Rosenbrock
    count = 0
    for i in range(iter):
        bees = BeesAlg05(20, 6, 1, 5, 8, 0.1)
        bees.populateScouts([-1.2,1.2], 4)
        bees.evaluate(rosenbrock2)
        while rosenbrock2(bees.scouts[0]) < (-0.001):
            bees.recruit(4)
            bees.evalSites(rosenbrock2)
            bees.populateScouts([-1.2,1.2], 4)
            bees.evaluate(rosenbrock2)
            bees.radius *= shrink
            count += 1
    print 'Function 6 Rosenbrock mean number of evaluations'
    print count/iter

    #function #8 Griewangk
    count = 0
    for i in range(iter):
        bees = BeesAlg05(10, 3, 2, 4, 7, 5)
        bees.populateScouts([-512,512], 10)
        bees.evaluate(griewangk)
        while griewangk(bees.scouts[0]) < (10-0.001):
            bees.recruit(10)
            bees.evalSites(griewangk)
            bees.populateScouts([-512,512], 10)
            bees.evaluate(griewangk)
            bees.radius *= shrink
            count += 1
    print 'Function 8 Griewangk mean number of evaluations'
    print count/iter


def functionsBeesAlg09():
    print 'bees alg 09'
    #Function #1 De Jong
    count = 0
    bees = BeesAlg09(10, 3, 1, 2, 4, 0.1, 10, [-2.048, 2.048], deJong, 2)
    bees.evaluate()
    while deJong(bees.optima) < (3905.93-0.001):
        bees.localSearch()
        bees.globalSearch()
        bees.evaluate()
        print deJong(bees.optima)
    print count

def main():
    #functionsBeesAlg05()
    functionsBeesAlg09()

if __name__ == '__main__':
    main()