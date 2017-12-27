from riskBattle import battle
import matplotlib.pyplot as plt

def simulation():
    attackerList = list(i for i in xrange(2,21))
    defenderList = list(i for i in xrange(1,21))
    attackerCutoff = 1
    attackDice = 3
    defenseDice = 2
    verbose = 0
    iterations = 100
    resultList = []
    for attackers in attackerList:
        for defenders in defenderList:
            for iteration in xrange(1, iterations + 1):
                results = battle(attackers, defenders, attackerCutoff, attackDice, defenseDice, verbose)
                results["iteration"] = iteration
                #print results
                resultList.append(results)

    number_battles = len(resultList)
    print "Number of battles: {0}".format(number_battles)

if __name__ == "__main__":
    simulation()


