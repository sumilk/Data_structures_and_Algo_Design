class MaxHeap:
    """
    A Max Heap Implementation to store and select items
    based on Greedy Method
    """

    def __init__(self, maxsize):

        self.maxsize = maxsize
        self.size = 0
        self.Heap = [(0,0,0)] * (self.maxsize + 1)
        self.Heap[0] = (0,0,1e12)
        self.FRONT = 1


    def parent(self, pos):
        return pos // 2


    def leftChild(self, pos):
        return 2 * pos


    def rightChild(self, pos):
        return (2 * pos) + 1


    def isLeaf(self, pos):
        if pos > (self.size // 2) and pos <= self.size:
            return True
        return False


    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = (self.Heap[spos],
                                            self.Heap[fpos])


    def maxHeapify(self, pos):

        # If the node is a non-leaf node and smaller
        # than any of its child
        if not self.isLeaf(pos):
            if (self.Heap[pos][2] < self.Heap[self.leftChild(pos)][2] or
                    self.Heap[pos][2] < self.Heap[self.rightChild(pos)][2]):

                # Swap with the left child and heapify
                # the left child                
                if (self.Heap[self.leftChild(pos)][2] >
                        self.Heap[self.rightChild(pos)][2]):
                    
                        self.swap(pos, self.leftChild(pos))
                        self.maxHeapify(self.leftChild(pos))

                # Swap with the right child and heapify
                # the right child
                else:
                        self.swap(pos, self.rightChild(pos))
                        self.maxHeapify(self.rightChild(pos))


    def insert(self, element):

        if self.size >= self.maxsize:
            print('Heap is full')
        self.size += 1
        self.Heap[self.size] = element

        current = self.size

        while (self.Heap[current][2] >
               self.Heap[self.parent(current)][2]):

            self.swap(current, self.parent(current))
            current = self.parent(current)


    def Print(self):

        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.Heap[i]) +
                  " LEFT CHILD : " + str(self.Heap[2 * i]) +
                  " RIGHT CHILD : " + str(self.Heap[2 * i + 1]))


    def extractMax(self):

        if self.size ==0:
            print('Heap is empty')

        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.Heap[self.size] = (0,0,0)
        self.size -= 1
        self.maxHeapify(self.FRONT)

        return popped

class AmmunitionSelection:

    def __init__(self, max_weight, ammo_heap):
        self.max_weight = max_weight
        self.ammo_heap = ammo_heap

    def optimize(self):
        """
        uses Greedy Method to select ammunitions to carry
        in what ratio to maximize the damage

        :return: total damage and ammonition ratios
        """
        weight = 0
        total_damage = 0


        ammunition_ratio_dict = {}

        while weight < max_weight:

            a = self.ammo_heap.extractMax()  # Greedy Choice

            ammo_wt = a[1]

            wt = min(ammo_wt, self.max_weight - weight)
            weight += wt
            ratio = wt/ammo_wt
            total_damage += wt * a[2]
            ammunition_ratio_dict[a[0]] = ratio
        return total_damage, ammunition_ratio_dict


def format_numeric(a):

    a = str(a)
    v1 = a.split('.')[1]
    v1 = int(v1)

    if v1 == 0:
        return a.split('.')[0]
    else:
        return round(float(a), 2)

if __name__ == "__main__":

    str_output = ''

    with open('inputPS9.txt', 'r') as input_file:
        total_weapons = int(input_file.readline().split(':')[1].strip())
        max_weight = float(input_file.readline().split(':')[1].strip())

        ammo_heap = MaxHeap(2 * total_weapons + 2)

        ammo_list = []


        for i in range(total_weapons):
            line = input_file.readline().split('/')
            ammo = line[0].strip()
            weight = float(line[1].strip())
            damage_per_kg = float(line[2].strip())/weight
            ammo_heap.insert((ammo, weight, damage_per_kg))
            ammo_list.append(ammo)

        total_damage, ammunition_ratio_dict = AmmunitionSelection(max_weight, ammo_heap).optimize()

    with open('outputPS9.txt', 'w') as output_file:

        output_file.write(f'Total Damage: {format_numeric(total_damage)}\n')
        output_file.write('Ammunition Packs Selection Ratio::\n')
        for ammo in ammo_list:
            if ammunition_ratio_dict.get(ammo):
                output_file.write(f'{ammo}: {format_numeric(ammunition_ratio_dict.get(ammo))}\n')
            else:
                output_file.write(f'{ammo}: 0\n')


