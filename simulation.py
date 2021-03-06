import optparse
import time
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from riskBattle import battle

def statLocation(x_min, x_max, y_min, y_max):
    x_stat = x_min + (x_max - x_min) / 8.0
    y_stat = y_max - (y_max - y_min) / 5.0
    return x_stat, y_stat

def log(t0, message):
    t1 = time.time()
    dt = str(timedelta(seconds=t1-t0))
    print "{0}\t{1}".format(dt, message)

# use even maxArmies and iterations so that valeus for remains and wins can be zero
def simulation(maxArmies, iterations, diceSides):
    number_battles = maxArmies ** 2 * iterations
    print "Number of battles in simulation: {0}".format(number_battles)
    print "Attacking armies from 2 to {0}".format(maxArmies + 1)
    print "Defending armies from 1 to {0}".format(maxArmies)
    print "Iterations per attacking / defending combination: {0}".format(iterations)
    t0 = time.time()
    attackerCutoff = 1
    attackDice = 3
    defenseDice = 2
    verbose = 0
    counter = 0
    resultList = []
    attackerList = list(i for i in xrange(2, maxArmies + 2))
    defenderList = list(i for i in xrange(1, maxArmies + 1))
    for attackers in attackerList:
        for defenders in defenderList:
            for iteration in xrange(1, iterations + 1):
                if counter % 10000 == 0:
                    log(t0, "Executing battle {0}".format(counter))
                result = battle(attackers, defenders, attackerCutoff, attackDice, defenseDice, diceSides, verbose)
                result["iteration"] = iteration
                #print result
                resultList.append(result)
                counter += 1

    bin_edges = [] # x and y bin edges
    bin_edges.append(list(0.5 + i for i in xrange(maxArmies + 1)))
    bin_edges.append(list(0.5 + i for i in xrange(1, maxArmies + 2)))

    fig, ax = plt.subplots()
    
    wins_x = []
    wins_y = []
    wins_weight = []
    remains_x = []
    remains_y = []
    remains_weight = []
    zeroWins_x = []
    zeroWins_y = []
    zeroRemains_x = []
    zeroRemains_y = []
    sumWins = 0
    sumRemains = 0
    log(t0, "Calculating net wins and net remaining armies.")
    for result in resultList:
        iteration = result["iteration"]
        x = result["initial_defenders"]
        y = result["initial_attackers"]
        wins = result["attackers_win"] - result["defenders_win"]
        remains = float(result["remaining_attackers"] - result["remaining_defenders"]) / float(iterations)
        sumWins += wins
        sumRemains += remains
        
        if iteration == iterations:
            if sumWins == 0:
                zeroWins_x.append(x)
                zeroWins_y.append(y)
            if abs(sumRemains) < 1.0:
                zeroRemains_x.append(x)
                zeroRemains_y.append(y)
            sumWins = 0
            sumRemains = 0

        wins_x.append(x)
        wins_y.append(y)
        wins_weight.append(wins)
        
        remains_x.append(x)
        remains_y.append(y)
        remains_weight.append(remains)

    log(t0, "Creating plots.")
    dir_name = "plots/"

    # Histograms
    histograms = []
    histo = {}
    histo["x_data"] = wins_x
    histo["y_data"] = wins_y
    histo["weights"] = wins_weight
    histo["title"] = "Net Wins for Attacker (Positive) and\nDefender (Negative) using {0}-sided Dice".format(diceSides)
    histo["file_name"] = "{0}netWins_d{1}_max{2}_iterations{3}".format(dir_name, diceSides, maxArmies, iterations)
    histograms.append(histo)
    histo = {}
    histo["x_data"] = remains_x
    histo["y_data"] = remains_y
    histo["weights"] = remains_weight
    histo["title"] = "Average Net Remaining Armies for Attacker (Positive) and\nDefender (Negative) using {0}-sided Dice".format(diceSides)
    histo["file_name"] = "{0}netRemains_d{1}_max{2}_iterations{3}".format(dir_name, diceSides, maxArmies, iterations)
    histograms.append(histo)
    
    for h in histograms:
        plt.hist2d(h["x_data"], h["y_data"], weights=h["weights"], bins=bin_edges)
        plt.colorbar()
        plt.title(h["title"])
        plt.xlabel("Initial Number of Defending Armies")
        plt.ylabel("Initial Number of Attacking Armies")
        plt.savefig("%s.pdf" % h["file_name"])
        plt.savefig("%s.png" % h["file_name"])
        plt.clf()

    topRight = maxArmies + 5

    # Scatter Plots
    scatters = []
    scat = {}
    scat["name"] = "wins"
    scat["x_data"] = zeroWins_x
    scat["y_data"] = zeroWins_y
    scat["title"] = "Zero Net Wins for Attacker (Positive) and\nDefender (Negative) using {0}-sided Dice".format(diceSides)
    scat["file_name"] = "{0}zeroWins_d{1}_max{2}_iterations{3}".format(dir_name, diceSides, maxArmies, iterations)
    scatters.append(scat)
    scat = {}
    scat["name"] = "remains"
    scat["x_data"] = zeroRemains_x
    scat["y_data"] = zeroRemains_y
    scat["title"] = "Zero Net Remains for Attacker (Positive) and\nDefender (Negative) using {0}-sided Dice".format(diceSides)
    scat["file_name"] = "{0}zeroRemains_d{1}_max{2}_iterations{3}".format(dir_name, diceSides, maxArmies, iterations)
    scatters.append(scat)
    
    for s in scatters:
        plt.plot(s["x_data"], s["y_data"], 'o', c="xkcd:cerulean", alpha=0.8)
        
        # Linear Fit for Zero Wins or Remains
        if s["x_data"] and s["y_data"]:
            z = np.polyfit(s["x_data"], s["y_data"], 1)
            f = np.poly1d(z)
            f_string = str(f)
            f_string = f_string.split("\n")[-1]
            f_string = "f(x) = {0}".format(f_string)
            print "Fit for zero {0}: {1}".format(s["name"], f_string)
            # calculate new x's and y's using fit function
            x_new = np.linspace(0, topRight, 100)
            y_new = f(x_new)
            x_stat, y_stat = statLocation(0, topRight, 0, topRight)
            plt.plot(x_new, y_new, '--', c="xkcd:kelly green", alpha=0.8)
            plt.text(x_stat, y_stat, f_string)
        else:
            print "No zero {0} found.".format(s["name"])
        
        axes = plt.gca()
        axes.set_xlim([0, topRight])
        axes.set_ylim([0, topRight])

        plt.title(s["title"])
        plt.xlabel("Initial Number of Defending Armies")
        plt.ylabel("Initial Number of Attacking Armies")
        plt.savefig("%s.pdf" % s["file_name"])
        plt.savefig("%s.png" % s["file_name"])
        plt.clf()

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option("-d", "--diceSides",  dest='diceSides',  action='store', default=6,  help="Number of sides on dice used for rolling.")
    parser.add_option("-m", "--maxArmies",  dest='maxArmies',  action='store', default=20, help="Maximum number of attacking / defending armies for simulation.")
    parser.add_option("-i", "--iterations", dest='iterations', action='store', default=20, help="Number of iterations for each attacking / defending army combination for simulation.")
    options, args = parser.parse_args()
    
    diceSides  = int(options.diceSides)
    maxArmies  = int(options.maxArmies)
    iterations = int(options.iterations)
    simulation(maxArmies, iterations, diceSides)


