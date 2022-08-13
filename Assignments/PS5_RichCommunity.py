class RichCommunity:
    def find_max_wealth(self, community_size, wealth_list):
        max_wealth = 0
        if len(wealth_list) <= community_size:
            return max(wealth_list) * len(wealth_list)

        max_index = wealth_list.index(max(wealth_list))

        if max_index < community_size:
            max_wealth += wealth_list[max_index] * community_size + self.find_max_wealth(community_size,
                                                                                   wealth_list[community_size:])
        elif max_index >= len(wealth_list) - community_size:
            max_wealth += wealth_list[max_index] * community_size + self.find_max_wealth(community_size,
                                                                                    wealth_list[:-community_size])
        else:
            len_left = community_size // 2

            max_wealth += wealth_list[max_index] * community_size + \
                          self.find_max_wealth(community_size,
                                               wealth_list[:max_index - community_size // 2] + wealth_list[
                                                                                               max_index + community_size // 2:])

        return max_wealth

if __name__ == '__main__':
    max_wealth_list = []
    with open('inputPS5.txt', 'r') as input_file:
        while True:
            line = input_file.readline()
            if not line or len(line) ==0:
                break
            community_size, wealth_list = line.split('::')
            community_size = int(community_size.strip())
            wealth_list = [int(x.strip()) for x in wealth_list.split()]

            max_wealth_list.append(RichCommunity().find_max_wealth(community_size, wealth_list))
    with open('outputPS5.txt', 'w') as output_file:
        for w in max_wealth_list:
            output_file.write(f'{w}\n')

