import csv

from map.models import Nodes, Edges

def run():
    fhand = open('map/load.csv')
    reader = csv.reader(fhand)

    Nodes.objects.all().delete()
    Edges.objects.all().delete()

    for row in reader:
        print(row)
        n1, created = Nodes.objects.get_or_create(node=row[0])
        n2, created = Nodes.objects.get_or_create(node=row[1])
        print(type(int(row[3])))
        edge = Edges(node1 = n1, node2 = n2, edge = row[2], distance = int(row[3]))
        edge.save()