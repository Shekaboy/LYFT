from collections import defaultdict 
import sys 
import math

def printingpath(src, dest, path):
		i = dest
		a = []
		while(i != src):
			a.append(i)
			i = path[i]
		a.reverse()
		a.insert(0, src)
		return a

class Heap(): 

	def __init__(self): 
		self.array = [] 
		self.size = 0
		self.pos = [] 

	def newMinHeapNode(self, v, dist): 
		minHeapNode = [v, dist] 
		return minHeapNode 

	def swapMinHeapNode(self,a, b): 
		t = self.array[a] 
		self.array[a] = self.array[b] 
		self.array[b] = t 

	def minHeapify(self, idx): 
		smallest = idx 
		left = 2*idx + 1
		right = 2*idx + 2

		if left < self.size and self.array[left][1] < self.array[smallest][1]: 
			smallest = left 

		if right < self.size and self.array[right][1] < self.array[smallest][1]: 
			smallest = right 

		if smallest != idx: 

			self.pos[ self.array[smallest][0] ] = idx 
			self.pos[ self.array[idx][0] ] = smallest 

			self.swapMinHeapNode(smallest, idx) 

			self.minHeapify(smallest)

	def peek(self):
		temp = self.array[0][0]
		return temp 

	def extractMin(self): 

		if self.isEmpty() == True: 
			return

		root = self.array[0] 

		lastNode = self.array[self.size - 1] 
		self.array[0] = lastNode 

		self.pos[lastNode[0]] = 0
		self.pos[root[0]] = self.size - 1

		self.size -= 1
		self.minHeapify(0) 

		return root 

	def isEmpty(self): 
		return True if self.size == 0 else False

	def decreaseKey(self, v, dist): 


		i = self.pos[v] 

		self.array[math.ceil(i)][1] = dist 

		while i > 0 and self.array[math.ceil(i)][1] < self.array[math.ceil((i - 1) / 2)][1]: 

			self.pos[ self.array[math.ceil(i)][0] ] = (i-1)/2
			self.pos[ self.array[math.ceil((i-1)/2)][0] ] = i 
			self.swapMinHeapNode(math.ceil(i), math.ceil((i - 1)/2) ) 

			i = (i - 1) / 2; 

	def isInMinHeap(self, v): 

		if self.pos[v] < self.size: 
			return True
		return False


def printArr(dist, n): 
	print("Vertex\tDistance from source")
	for i in range(n): 
		print("%d\t\t%d" % (i,dist[i])) 


class Graph(): 

	def __init__(self, V): 
		self.V = V 
		self.graph = defaultdict(list) 

	def addEdge(self, src, dest, weight): 

		newNode = [dest, weight] 
		self.graph[src].insert(0, newNode) 



	def dijkstra(self, src, dest): 

		V = self.V 
		dist = [] 
				
		path = [None] * V
		minHeap = Heap() 

		print(V)
		for v in range(V): 
			dist.append(sys.maxsize) 
			minHeap.array.append( minHeap.newMinHeapNode(v, dist[v]) ) 
			minHeap.pos.append(v) 

		dist[src] = 0
		minHeap.decreaseKey(src, dist[src]) 

		minHeap.size = V; 

		while minHeap.isEmpty() == False: 

			newHeapNode = minHeap.extractMin() 
			u = newHeapNode[0] 

			for pCrawl in self.graph[u]: 

				v = pCrawl[0] 
				if minHeap.isInMinHeap(v) and dist[u] != sys.maxsize and pCrawl[1] + dist[u] < dist[v]: 
						dist[v] = pCrawl[1] + dist[u] 
						path[v] = u
						minHeap.decreaseKey(v, dist[v]) 
		return [dist, path]


	def dijkstrafortwo(self, src1, src2, dest):
		dij1 = self.dijkstra(src1, dest)
		d1 = dij1[0][dest]
		diff1 = dij1[0][src2]
		path1 = dij1[1]
		path1_1 = printingpath(src1, dest, path1)
		dij2 = self.dijkstra(src2, dest)
		d2 = dij2[0][dest]
		naive = diff1 + d2
		diff2 = {}
		for nodes in range(len(path1_1)):
			diff2[path1_1[nodes]] = dij2[0][path1_1[nodes]]
		diff2_final = min(diff2.values())
		optimal = d1 + diff2_final
		path2 = dij2[1]
		path2_1 = printingpath(src2, dest, path2)
		a = dest
		if(naive <= optimal):
			path1_2 = printingpath(src1, src2, path1)
			return [path1_2, path2_1, False]
		else:
			for key in diff2:
				if(diff2_final == diff2[key]):
					a = key
					break
			path2_2 = printingpath(src2, a, path2)
			return [path2_2, path1_1, True]
