from Data_Structures.basic_structures import LinkedList, Queue

class DAG:
    def __init__(self, fname):
        with open(fname) as edge_file:
            lines = edge_file.readlines()
            lines = [line.strip("\n") for line in lines]
            self.amt_vertices = int(lines[0])
            self.max_flows = []
            self.current_flows = []
            self.adj_list = [LinkedList() for i in range(self.amt_vertices)]
            for i in range(self.amt_vertices):
                self.max_flows.append([0 for i in range(self.amt_vertices)])
                self.current_flows.append([0 for i in range(self.amt_vertices)])
            for line in lines[1:]:
                line = [int(i) for i in line.split(" ")]
                self.mk_edge(line[0], line[1])
                self.max_flows[line[0]][line[1]] = line[2]

    def mk_edge(self, begin, end):
        self.adj_list[begin].append(end)

    def reset_current_flows(self):
        self.current_flows = []
        for i in range(self.amt_vertices):
            self.current_flows.append([0 for i in range(self.amt_vertices)])

    def augment_current_flows(self, path, amt):
        for i in range(1, len(path)):
            self.current_flows[path[i-1]][path[i]] += amt

    def bfs(self, start, sink):
        edgeTo = [0 for i in range(self.amt_vertices)]
        marked = [False for i in range(self.amt_vertices)]
        q = Queue()
        q.add(start)
        marked[start] = True
        while len(q) != 0:
            dq = q.remove()
            adjacency_list = self.adj_list[dq]
            for i in range(len(adjacency_list)):
                curr = adjacency_list[i]
                if not marked[curr]:
                    maximum =  self.max_flows[dq][curr]
                    minimum = self.current_flows[dq][curr]
                    diff = maximum - minimum
                    if diff > 0:
                        q.add(curr)
                        edgeTo[curr] = dq
                        marked[dq] = True
        return edgeTo

    def path_to(self, edgeTo, n):
        path = LinkedList()
        path.prepend(n)
        while edgeTo[n] != 0:
            path.prepend(edgeTo[n])
            n = edgeTo[n]
        path.prepend(0)
        return path

    def get_bottleneck_capacity(self, path):
        prev = path[0]
        minimum = 1000000
        for i in range(1, len(path)):
            curr = path[i]
            diff = self.max_flows[prev][curr] - self.current_flows[prev][curr]
            if minimum >= diff:
                minimum = diff
            prev = curr
        return minimum

    def edmonds_karp(self, start, sink):
        self.reset_current_flows()
        max_flow = 0
        while True:
            edgeTo = self.bfs(start, sink)
            path = self.path_to(edgeTo, sink)
            if len(path) == 2:
                return max_flow
            bottleneck =  self.get_bottleneck_capacity(path)
            max_flow += bottleneck
            self.augment_current_flows(path, bottleneck)

    def __str__(self):
        ret_val = ""
        for i in range(len(self.adj_list)):
            for j in range(len(self.adj_list[i])):
                ret_val += str(i) + "->"
                ret_val += str(self.adj_list[i][j]) + ": "
                ret_val += str(self.max_flows[i][self.adj_list[i][j]])
                ret_val += "\n"
        ret_val = ret_val[:len(ret_val)-1]
        return ret_val


new_dag = DAG("pyDag.txt")
#https://www.youtube.com/watch?v=w3Nl2XA0pxA&t=465s
assert new_dag.edmonds_karp(0, 5) == 26
