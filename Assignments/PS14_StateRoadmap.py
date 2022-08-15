class StateRoadmap:
    def find_shortest_dist(self, input_matrix):
        distances = input_matrix

        N = len(input_matrix)

        for k in range(N):
            for i in range(N):
                for j in range(N):
                    if i == j:
                        distances[i][j] = 0
                    else:
                        distances[i][j] = min(distances[i][j],   distances[i][k] + distances[k][j])
        return distances



if __name__ == '__main__':
    with open('inputPS14.txt', 'r') as input_file:
        input_matrix = []
        set_nodes = set()
        dict_nodes = {}
        n = 0
        while True:
            line = input_file.readline().split('/')
            if not line or len(line) < 3:
                break
            X, Y, dist = [int(l.strip()) for l in line]
            set_nodes.add(X)
            set_nodes.add(Y)
            if not dict_nodes.get(X):
                dict_nodes[X] = [n]
                n += 1
            dict_nodes[X].append((Y,dist))


        #print(set_nodes)
        #print(dict_nodes)
        MAX = 1e12
        input_matrix = [[MAX for i in range(len(set_nodes))] for j in range(len(set_nodes))]
        #print(input_matrix)

        for i, idx in enumerate(dict_nodes):
            for node in dict_nodes[idx]:
                if isinstance(node,int):
                    index = node
                else:
                    input_matrix[index][dict_nodes[node[0]][0]] = node[1]

        distances = StateRoadmap().find_shortest_dist(input_matrix)
        with open('outputPS14.txt', 'w') as output_file:
            for distance in distances:
                distance = [str(x) for x in distance]
                output_file.write(','.join(distance)+'\n')

