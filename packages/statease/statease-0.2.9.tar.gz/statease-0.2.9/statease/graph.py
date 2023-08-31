from collections import namedtuple

class Graph:
  def __init__(self, payload):
    self.points = []
    for p in payload.get('points', []):
      point = namedtuple('Point', iter(p.keys()))(**p)
      self.points.append(point)

    self.limits = []
    for l in payload.get('limits', []):
      limit = namedtuple('Limit', iter(l.keys()))(**l)
      self.limits.append(limit)

  def __str__(self):
    return " ".join(["{},{}".format(p.x, p.y) for p in self.points])
