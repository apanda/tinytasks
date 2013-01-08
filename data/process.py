import sys
from numpy import std, mean
if len(sys.argv) < 2:
    print "%s file"%(sys.argv[0])
points = {}
f = open(sys.argv[1])
for l in f:
    parts = map(int, l.strip().split(','))
    if parts[0] not in points:
        points[parts[0]] = []
    points[parts[0]].append(parts[1])

for k in sorted(points.keys()):
    print "%d,%f,%f"%(k, mean(points[k])/1000.0, std(points[k])/1000.0)

