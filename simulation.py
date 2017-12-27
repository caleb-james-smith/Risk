from riskBattle import battle
import matplotlib.pyplot as plt

def simulation():
    attackerList = list(i for i in xrange(2,21))
    defenderList = list(i for i in xrange(1,21))
    attackerCutoff = 1
    attackDice = 3
    defenseDice = 2
    verbose = 0
    for attackers in attackerList:
        for defenders in defenderList:
            results = battle(attackers, defenders, attackerCutoff, attackDice, defenseDice, verbose)
            print results

if __name__ == "__main__":
    simulation()


