# coding=utf-8
from math import radians, cos, sin, asin, sqrt
from pyecharts import GeoLines, Style
import json
import string

# read data
capitals = []
f = open('us_state_capitals.json')
datas = json.load(f)
for key, value in datas.items():
    print(value)
    a = [value['capital'], float(value['lat']), float(value['long'])]
    capitals.append(a)


# Calculate distance using latitude and longitude
def haversine(loc1, loc2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1 = capitals[loc1][1]
    lat1 = capitals[loc1][2]
    lon2 = capitals[loc2][1]
    lat2 = capitals[loc2][2]
    # conversion
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine Algorithm for calculating distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # km, Earth radius
    return c * r * 1000


# distance matrix
matrix = [[0 for i in range(50)] for i in range(50)]
for i in range(50):
    for j in range(i):
        matrix[i][j] = matrix[j][i] = haversine(i, j)
for i in range(50):
    matrix[i][i] = -1
print(matrix)


# MST class
class Graph(object):
    def __init__(self, maps):
        self.maps = maps
        self.nodenum = self.get_nodenum()
        self.edgenum = self.get_edgenum()

    def get_nodenum(self):
        return len(self.maps)

    def get_edgenum(self):
        count = 0
        for i in range(self.nodenum):
            for j in range(i):
                if self.maps[i][j] > 0 and self.maps[i][j] < 99999999999:
                    count += 1
        return count

    def prim(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum - 1:
            return res
        res = []
        seleted_node = [0]
        candidate_node = [i for i in range(1, self.nodenum)]

        while len(candidate_node) > 0:
            begin, end, minweight = 0, 0, 99999999
            for i in seleted_node:
                for j in candidate_node:
                    if self.maps[i][j] < minweight:
                        minweight = self.maps[i][j]
                        begin = i
                        end = j
            res.append([begin, end, minweight])
            seleted_node.append(end)
            candidate_node.remove(end)
        return res


# generate HTML file
graph = Graph(matrix)
res = graph.prim()
min_span_tree=[]
for i in res:
    min_span_tree.append([capitals[i[0]][0], capitals[i[1]][0]])
print(min_span_tree)

style = Style(
    title_top="#fff",
    title_pos="center",
    width=1200,
    height=600,
    background_color="#404a59"
)

geolines = GeoLines("USA Minimum Spanning Tree", **style.init_style)
geolines.add(" ", min_span_tree, maptype='美国', is_legend_show=False)
geolines.render("USA Minimum Spanning Tree.html")
