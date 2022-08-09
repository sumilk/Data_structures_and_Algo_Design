
class RestaurantIngredients:
    def __init__(self, packet_list):
        self.packet_list = packet_list

    def process(self):
        """
        uses Greedy Method to find out the number of balanced dishes
        that can be made using given packets of saly and pepper

        :return: the list of dish counts that can be prepared
        """
        dish_count_list = []
        for packets in packet_list:
            dish_count = 0
            s_count = 0
            p_count = 0
            for i in packets:
                if i == 'S':
                    s_count += 1
                else:
                    p_count += 1
                if (s_count == p_count):
                    dish_count += 1
            dish_count_list.append(dish_count)
        return dish_count_list

if __name__ == '__main__':
    packet_list = []
    with open('inputPS6.txt', 'r') as input_file:
        while (True):
            packets = input_file.readline().strip()
            if (not packets):
                break
            packet_list.append(packets)
    dish_count_list = RestaurantIngredients(packet_list).process()

    with open('outputPS6.txt', 'w') as output_file:
        for dish_count in dish_count_list:
            output_file.write(f'{str(dish_count)}\n')
