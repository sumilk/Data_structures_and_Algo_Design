class BudgetAllocation:
    def optimize(self, available_budget, budget_list, value_list, n_missions):

        """
        Dynamic Programming  based approach that
        uses 0-1 knapsack method  to optimize budget allocation
        This method uses Memoization Technique.
        This method is basically an extension to the recursive approach so that we can overcome the problem of calculating redundant
        cases and thus increased complexity. We can solve this problem by simply creating a 2-D array that can store a particular state
        (n, available_budget) if we get it the first time. Now if we come across the same state (n, available_budget) again instead of calculating it in exponential
        complexity we can directly return its result stored in the table in constant time. This method gives an edge over the recursive approach in this aspect.

        :param available_budget: available budget
        :param budget_list: budget list for missions
        :param value_list: value list for missions
        :param n_missions: no of missions

        :return: optimized budget allocation
        """
        # Base Conditions
        if n_missions == 0 or available_budget == 0:
            return 0
        if t[n_missions][available_budget] != -1:
            return t[n_missions][available_budget]



        # exclude nth mission if budget is greater than available budget
        if budget_list[n_missions-1] > available_budget:
            t[n_missions][available_budget]  = self.optimize(available_budget, budget_list, value_list, n_missions-1)
        else:
            # return the maximum of two cases:
            # (1) nth mission included
            # (2) not included
            t[n_missions][available_budget] = max(
                value_list[n_missions - 1] + self.optimize(available_budget - budget_list[n_missions - 1], budget_list, value_list, n_missions - 1),
                self.optimize(available_budget, budget_list, value_list, n_missions - 1))

        return t[n_missions][available_budget]

    def get_missions(self, available_budget, final_budget, budget_list, value_list, n_missions):
        """
        returns missions to be included

        :param available_budget: available budget
        :param final_budget: final budget
        :param budget_list: budget list for missions
        :param value_list: value list for missions
        :param n_missions: no of missions

        :return:missions to be included and remaining budget
        """
        missions = []
        res, budget_remaining = final_budget, available_budget

        for i in range(n_missions, 0, -1):
            if res <= 0:
                break
            if res == t[i - 1][budget_remaining]:
                continue
            else:
                missions.append(i)
                res = res - value_list[i - 1]
                budget_remaining -= budget_list[i - 1]
                missions.reverse()

        return missions, budget_remaining



if __name__ == "__main__":

    available_budget = 100

    mission_names, budget_list, value_list = [], [], []

    with open('inputPS8.txt', 'r') as input_file:
        while(True):
            line = input_file.readline().split('/')
            if not line or len(line) < 3:
                break
            mission_names.append(line[0].strip())
            budget_list.append(int(line[1].strip()))
            value_list.append(int(line[2].strip()))
    n_missions = len(budget_list)

    # We initialize the matrix with -1 at first.
    t = [[-1 for i in range(available_budget + 1)] for j in range(n_missions + 1)]


    ba = BudgetAllocation()

    final_budget = ba.optimize(available_budget, budget_list, value_list, n_missions)

    missions, budget_remaining = ba.get_missions(available_budget, final_budget, budget_list, value_list, n_missions)

    with open('outputPS8.txt', 'w') as output_file:
        output_file.write(f'The missions that should be funded: {str(missions)}\n')

        output_file.write(f'Total value: {t[n_missions][available_budget]}\n')

        output_file.write(f'Budget remaining: {budget_remaining}')

