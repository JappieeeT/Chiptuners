import csv
import code.classes.grid as grid
from code.algorithms import hillclimber, representation as rep
from code.algorithms import baseline as base
from code.algorithms import hillclimber as climber
from code.visualize import visualize as vis


def log_simulation(times, print_connections, netlist):
    
    simulations = {}
    chip_nr = int((netlist - 1) / 3)

    with open(f"output/netlist_{netlist}_{times}x.csv", "w", newline="") as csvfile:

        # Set up fieldnames 
        fieldnames = ["simulation", "cost", "attempts"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        costs = []

        # Run n simulations and log each run in a new row
        for i in range(1, times + 1):
            infile = None
            chip = grid.Grid(chip_nr, netlist, infile)
            baseline = base.Baseline(chip, print_connections)
            baseline.run()
            chip.compute_costs()
            costs.append(chip.cost)
            simulations[i] = chip
            writer.writerow({
                    "simulation": i, "cost": chip.cost, "attempts": chip.tot_attempts
                    })
            print(f"Completed simulation {i}: C = {chip.cost}, found on attempt {chip.tot_attempts}")
            chip.to_csv()

        avgCosts = sum(costs)/times
        writer.writerow({
            "simulation": "Avg costs", "cost": avgCosts
        })

def improve(netlist):
    chip_nr = int((netlist - 1) / 3)
    chip = grid.Grid(chip_nr, netlist, "output/output.csv")

    hillclimber = climber.Hillclimber(chip, 10)
    hillclimber.run()


def visualize_three_dimensional(netlist):
    """Text."""

    chip_nr = int((netlist - 1) / 3)
    chip = grid.Grid(chip_nr, netlist, "output/output.csv")
    vis(chip)

if __name__ == "__main__": 

    N = 1

    print_connections = False

    netlist = 4

    log_simulation(N, print_connections, netlist)

    # visualize_three_dimensional(netlist)

    # improve(netlist)
