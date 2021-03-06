"""
sorting.py

Contains all sorting functions used to sort nets in a specific order.
Includes:   - sort_length
            - random_sort
            - sort_middle_first
            - sort_gate
            - sort_exp_intersections
"""
from copy import deepcopy
import random
import operator


def sort_length(nets, descending=False):
    """
    Sorts net object instances on their distance
    between start- and end coordinates.
    """
    return (sorted(nets.values(),
            key=operator.attrgetter('minimal_length'),
            reverse=descending))


def random_sort(nets, descending="None"):
    """Sorts net object instances in a random order."""

    # Load the net values and randomly shuffle its order
    value_list = list(nets.values())
    random.shuffle(value_list)

    return value_list


def sort_middle_first(nets, descending=False):
    """
    Sorts net object instances on their position in the grid;
    in the middle or on the outside.
    """

    # Find the size of the grid and compute its middle
    a_net = list(nets.values())[0]
    size = a_net.grid.size[:2]

    middle_x = round(size[0]/2)
    middle_y = round(size[1]/2)

    for net in nets.values():
        delta_middle_start = abs(middle_x - net.start[0]) + abs(middle_y - net.start[1])
        delta_middle_end = abs(middle_x - net.end[0]) + abs(middle_y - net.end[1])
        total_distance_middle = delta_middle_start + delta_middle_end

        net.total_distance_middle = total_distance_middle

    # Sort the nets
    return (sorted(nets.values(),
            key=operator.attrgetter('total_distance_middle'),
            reverse=descending))


def sort_gate(nets, descending=True):
    """
    Sorts net object instances on how many connections a gate has
    with other gates.
    """

    # Retrieve the grid from the first net
    grid = list(nets.values())[0].grid

    # Create dicts for storing occupation of the gates and the number of neighbors of the nets
    gate_occupation = {}
    net_neighbors = {}

    # Set gate occupation to zero for all gate coordinates
    for gate in grid.gates.values():
        gate_occupation[gate.coordinates] = 0

    # Count occurrences of gate coordinates
    for net in nets.values():
        net_neighbors[net] = 0
        gate_occupation[net.start] += 1
        gate_occupation[net.end] += 1

    # Count the number of neighbors of each net
    for net in nets.values():
        net_neighbors[net] += gate_occupation[net.start] + gate_occupation[net.end] - 2

    # Return sorted list
    return sorted(net_neighbors, key=net_neighbors.get, reverse=descending)


def sort_exp_intersections(nets, descending=False):
    """
    Sorts net object instances based on how many intersections are expected per net.
    """

    # For every net object copy the start- and end coordinates
    for key in nets:
        net = nets[key]

        # Go over all other nets and compute the dot product with itself and the others one by one
        other_nets = deepcopy(nets)
        other_nets.pop(key)

        for other_net in other_nets.values():

            # p0 = (y3 - y2)(x3 - x0) - (x3 - x2)(y3 - y0)
            p0 = (other_net.end[1] - other_net.start[1]) * (other_net.end[0] - net.start[0]) - \
                 (other_net.end[0] - other_net.start[0]) * (other_net.end[1] - net.start[1])

            # p1 = (y3 - y2)(x3 - x1) - (x3 - x2)(y3 - y1)
            p1 = (other_net.end[1] - other_net.start[1]) * (other_net.end[0] - net.end[0]) - \
                 (other_net.end[0] - other_net.start[0]) * (other_net.end[1] - net.end[1])

            # p2 = (y1 - y0)(x1 - x2) - (x1 - x0)(y1 - y2)
            p2 = (net.end[1] - net.start[1]) * (net.end[0] - other_net.start[0]) - \
                 (net.end[0] - net.start[0]) * (net.end[1] - other_net.start[1])

            # p3 = (y1 - y0)(x1 - x3) - (x1 - x0)(y1 - y3)
            p3 = (net.end[1] - net.start[1]) * (net.end[0] - other_net.end[0]) - \
                 (net.end[0] - net.start[0]) * (net.end[1] - other_net.end[1])

            # Check for expected intersections
            if (p0 * p1 < 0) and (p2 * p3 < 0):
                net.exp_intersections += 1

    # Return sorted list
    return (sorted(nets.values(),
            key=operator.attrgetter('exp_intersections'),
            reverse=descending))
