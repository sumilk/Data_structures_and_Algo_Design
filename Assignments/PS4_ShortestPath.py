
class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i][0] < self.queue[min][0]:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()


def shortest_path(graph, start):
    """Visit all nodes and calculate the shortest paths to each from start"""
    queue = PriorityQueue()
    queue.insert((0, start))
    distances = {start: 0}
    visited = set()
    path = {}

    while not queue.isEmpty():
        _, node = queue.delete()  # (distance, node), ignore distance
        if node in visited:
            continue
        visited.add(node)
        dist = distances[node]
        if not path.get(node):
            path[node] = [start]

        for neighbour, neighbour_dist in graph[node].items():
            if neighbour in visited:
                continue
            neighbour_dist += dist
            # path[node].add(neighbour)
            if neighbour_dist < distances.get(neighbour, float('inf')):
                queue.insert((neighbour_dist, neighbour))
                distances[neighbour] = neighbour_dist
                path[neighbour] = path[node] + [neighbour]

    #print(path)

    return distances, path

def convert_to_string(path):
    """
    formats the shartest path list into string for output file

    :param path: input list of shartest
    :return: string of shortest path
    """

    return '['+'-'.join(path)+']'

def calculate_time(distance, speed):
    """
    calculates the time in minutes to cover distance with given speed
    :param distance: distance to be covered
    :param speed: speed
    :return: time in minutes
    """

    time = str(distance/speed * 60)

    time_min = time.split('.')[0]
    time_sec = round(float(time.split('.')[0])/100*60)
    return time_min + ':' + str(time_sec)


def format_value(a):
    """
    formats the numeric input value to integer if the decimal part is zero,
    else returns the rounded decimal value

    :param a: the input numeric value:
    :return: the formatted value
    """
    a = str(a)
    value_after_decimal = a.split('.')[1]
    value_after_decimal = int(value_after_decimal)

    if value_after_decimal == 0:
        return a.split('.')[0]
    else:
        return round(float(a), 4)


if __name__ == '__main__':

    with open('inputPS4.txt', 'r') as input_file:
        graph = {}
        while (True):
            line = input_file.readline().split('/')
            if not line or len(line) < 3:
                break
            # print(line)
            node1 = line[0].strip()
            node2 = line[1].strip()
            dist = float(line[2].strip())
            if graph.get(node1) is None:
                graph[node1] = {}
            if graph.get(node2) is None:
                graph[node2] = {}
            graph[node1][node2] = dist
            graph[node2][node1] = dist

        start_node = line[0].split(':')[1].strip()
        end_node = input_file.readline().split(':')[1].strip()
        speed = float(input_file.readline().split(':')[1].strip())

        #print(graph)
        #print(shortest_path(graph, start_node))
        distances, path = shortest_path(graph, start_node)

        with open('outputPS4.txt', 'w') as output_file:

            output_file.write(f'Shortest route from the Hospital A (Node {start_node}) to reach the Hospital B (Node {end_node}) is\n')
            output_file.write(convert_to_string(path[end_node]))
            output_file.write(f'\nand it has minimum travel distance {format_value(distances[end_node])}km\n')
            time = calculate_time(distances[end_node], speed)
            output_file.write(f'it will take {time} minutes for the ambulance to reach the Hospital B at a speed of {format_value(speed)} kmph.')
