# encoding: utf-8
import sys
import random
import math

def generate(nodescount, maxcap, minX, maxX, minY, maxY):
    # return the generated data as a string
    data = 'params:\n'
    data += '  capacity %f\n' % maxcap
    data += 'nodes:\n'
    for i in range(nodescount):
        demand = random.uniform(0.0, maxcap)
        x = random.uniform(minX, maxX)
        y = random.uniform(minY, maxY)
        # On node label printing, the number of leading zeros is according to the amount of digits of the number of the nodes count, to adjust equal string length
        data += ('  node%0' + str(math.ceil(math.log(nodescount + 1) / math.log(10))) + 'd\t\t%.3f\t\t%.3f\t\t%.3f\n') % (i+1, demand, x, y)
    return data

# nodescount = int(sys.argv[1])
# maxcap = float(sys.argv[2])
# minX = float(sys.argv[3])
# maxX = float(sys.argv[4])
# minY = float(sys.argv[5])
# maxY = float(sys.argv[6])

# with open('in.txt', 'w') as f:
#     f.write('params:\n')
#     f.write('  capacity %f\n' % maxcap)
#     f.write('nodes:\n')
#     for i in range(nodescount):
#         demand = random.uniform(0.0, maxcap)
#         x = random.uniform(minX, maxX)
#         y = random.uniform(minY, maxY)
#         # On node label printing, the number of leading zeros is according to the amount of digits of the number of the nodes count, to adjust equal string length
#         f.write(('  node%0' + str(math.ceil(math.log(nodescount + 1) / math.log(10))) + 'd\t\t%.3f\t\t%.3f\t\t%.3f\n') % (i+1, demand, x, y))