class RichCommunity:
    def __init__(self,community_size, wealth_list):
        self.community_size = community_size
        self.wealth_list = wealth_list

        self.prepare_summation_matrix()

    def prepare_summation_matrix(self):
        n = len(self.wealth_list)
        self.dp = [-1 for i in range(n)]

    def find_max_wealth(self):

       if len(wealth_list) < self.community_size:
           return max(wealth_list)

       size = min (len(wealth_list), self.community_size)

       while self.unvisited_left():
           rem_index_list = [i for i,x in enumerate(self.dp) if x == -1]
           size = min(len(rem_index_list), self.community_size)
           j = rem_index_list[0]
           for k in range(j,j+size):
               if k not in rem_index_list:
                   for n in range(j,k):
                        self.dp[rem_index_list[n]] = max(self.wealth_list[j:k])
                   break
           max_w = max(self.wealth_list[j:k+1])
           idx = list(range(j,k+1))
           for m in range(size):
               if k+m >= len(self.wealth_list) or k+m not in rem_index_list:
                   break
               max_w_new = max(self.wealth_list[j+m:k+m+1])
               if max_w_new > max_w:
                   max_w = max_w_new
                   idx = list(range(j+m, k+m+1))
           for i in idx:
               self.dp[i] = max_w
           #print(self.dp)

       return sum(self.dp)


    def unvisited_left(self):
        return -1 in self.dp


    #
    # def find_max_wealth(self, community_size, wealth_list):
    #     max_wealth = 0
    #     if len(wealth_list) <= community_size:
    #         return max(wealth_list) * len(wealth_list)
    #
    #     max_index = wealth_list.index(max(wealth_list))
    #
    #     if max_index < community_size:
    #         max_wealth += wealth_list[max_index] * community_size + self.find_max_wealth(community_size,
    #                                                                                wealth_list[community_size:])
    #     elif max_index >= len(wealth_list) - community_size:
    #         max_wealth += wealth_list[max_index] * community_size + self.find_max_wealth(community_size,
    #                                                                                 wealth_list[:-community_size])
    #     else:
    #
    #         max_wealth += wealth_list[max_index] * community_size + \
    #                       self.find_max_wealth(community_size,
    #                                            wealth_list[:max_index - community_size // 2] + wealth_list[
    #                                                                                            max_index + community_size // 2:])
    #
    #     return max_wealth



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

            max_wealth_list.append(RichCommunity(community_size, wealth_list).find_max_wealth())
    with open('outputPS5.txt', 'w') as output_file:
        for w in max_wealth_list:
            output_file.write(f'{w}\n')

