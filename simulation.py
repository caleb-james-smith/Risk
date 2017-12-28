import optparse
from riskBattle import battle
import matplotlib.pyplot as plt

def simulation(max_armies, iterations):
    attackerCutoff = 1
    attackDice = 3
    defenseDice = 2
    verbose = 0
    resultList = []
    attackerList = list(i for i in xrange(2, max_armies + 2))
    defenderList = list(i for i in xrange(1, max_armies + 1))
    for attackers in attackerList:
        for defenders in defenderList:
            for iteration in xrange(1, iterations + 1):
                result = battle(attackers, defenders, attackerCutoff, attackDice, defenseDice, verbose)
                result["iteration"] = iteration
                #print result
                resultList.append(result)

    number_battles = len(resultList)
    print "Number of battles in simulation: {0}".format(number_battles)
    print "Attacking armies from 2 to {0}".format(max_armies + 1)
    print "Defending armies from 1 to {0}".format(max_armies)
    print "Iterations per attacking / defending combination: {0}".format(iterations)

    bin_edges = [] # x and y bin edges
    bin_edges.append(list(0.5 + i for i in xrange(max_armies + 1)))
    bin_edges.append(list(0.5 + i for i in xrange(1, max_armies + 2)))

    fig, ax = plt.subplots()
    
    wins_x = []
    wins_y = []
    wins_weight = []
    remains_x = []
    remains_y = []
    remains_weight = []
    for result in resultList:
        wins_x.append(result["initial_defenders"])
        wins_y.append(result["initial_attackers"])
        wins_weight.append(result["attackers_win"] - result["defenders_win"])
        remains_x.append(result["initial_defenders"])
        remains_y.append(result["initial_attackers"])
        remains_weight.append( float(result["remaining_attackers"] - result["remaining_defenders"]) / float(iterations) )
    
    plt.hist2d(wins_x, wins_y, weights=wins_weight, bins=bin_edges)
    plt.colorbar()
    
    plt.title("Net Wins for Attacker (Positive) and Defender (Negative)")
    plt.xlabel("Initial Number of Defending Armies")
    plt.ylabel("Initial Number of Attacking Armies")
    plt.savefig("net_wins.pdf")
    plt.savefig("net_wins.png")
    plt.clf()

    plt.hist2d(remains_x, remains_y, weights=remains_weight, bins=bin_edges)
    plt.colorbar()

    plt.title("Average Net Remaining Armies for\nAttacker (Positive) and Defender (Negative)")
    plt.xlabel("Initial Number of Defending Armies")
    plt.ylabel("Initial Number of Attacking Armies")
    plt.savefig("net_remains.pdf")
    plt.savefig("net_remains.png")
    plt.clf()

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option("-m", "--max_armies", dest='max_armies', action='store', default=20, help="Maximum number of attacking / defending armies for simulation.")
    parser.add_option("-i", "--iterations", dest='iterations', action='store', default=20, help="Number of iterations for each attacking / defending army combination for simulation.")
    options, args = parser.parse_args()
    
    print "Running simulation of many battles."
    
    max_armies = int(options.max_armies)
    iterations = int(options.iterations)
    simulation(max_armies, iterations)


