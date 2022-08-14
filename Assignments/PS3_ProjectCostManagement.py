class ProjectCostManagement:
    def optimize(self, available_budget, cost_list, roi_list, n_projects):

        """
        Dynamic Programming  based approach that
        uses 0-1 knapsack method  to optimize budget allocation
        This method uses Memoization Technique.
        This method is basically an extension to the recursive approach so that we can overcome the problem of calculating redundant
        cases and thus increased complexity. We can solve this problem by simply creating a 2-D array that can store a particular state
        (n, available_budget) if we get it the first time. Now if we come across the same state (n, available_budget) again instead of calculating it in exponential
        complexity we can directly return its result stored in the table in constant time. This method gives an edge over the recursive approach in this aspect.

        :param available_budget: available budget
        :param cost_list: cost list for projects
        :param roi_list: value list for projects
        :param n_projects: no of projects

        :return: optimized budget allocation
        """
        # Base Conditions
        if n_projects == 0 or available_budget == 0:
            return 0
        if t[n_projects][available_budget] != -1:
            return t[n_projects][available_budget]



        # exclude nth mission if budget is greater than available budget
        if cost_list[n_projects-1] > available_budget:
            t[n_projects][available_budget]  = self.optimize(available_budget, cost_list, roi_list, n_projects-1)
        else:
            # return the maximum of two cases:
            # (1) nth mission included
            # (2) not included
            t[n_projects][available_budget] = max(
                roi_list[n_projects - 1] + self.optimize(available_budget - cost_list[n_projects - 1], cost_list, roi_list, n_projects - 1),
                self.optimize(available_budget, cost_list, roi_list, n_projects - 1))

        return t[n_projects][available_budget]

    def get_projects(self, available_budget, final_budget, cost_list, roi_list, n_projects):
        """
        returns projects to be included

        :param available_budget: available budget
        :param final_budget: final budget
        :param cost_list: cost list for projects
        :param roi_list: roi list for projects
        :param n_projects: no of projects

        :return:projects to be included and remaining budget
        """
        projects = []
        res, budget_remaining = final_budget, available_budget

        for i in range(n_projects, 0, -1):
            if res <= 0:
                break
            if res == t[i - 1][budget_remaining]:
                continue
            else:
                projects.append(i)
                res = res - roi_list[i - 1]
                budget_remaining -= cost_list[i - 1]
                projects.reverse()

        return projects, budget_remaining



if __name__ == "__main__":

    available_budget = 150

    project_names, cost_list, roi_list = [], [], []

    with open('inputPS3.txt', 'r') as input_file:
        while(True):
            line = input_file.readline().split('/')
            if not line or len(line) < 3:
                break
            project_names.append(line[0].strip())
            cost_list.append(int(line[1].strip()))
            roi_list.append(int(line[2].strip()))
    n_projects = len(cost_list)

    # We initialize the matrix with -1 at first.
    t = [[-1 for i in range(available_budget + 1)] for j in range(n_projects + 1)]


    pcm = ProjectCostManagement()

    final_budget = pcm.optimize(available_budget, cost_list, roi_list, n_projects)

    projects, budget_remaining = pcm.get_projects(available_budget, final_budget, cost_list, roi_list, n_projects)

    with open('outputPS3.txt', 'w') as output_file:
        output_file.write(f'The projects that should be funded: {str(projects)}\n')

        output_file.write(f'Total ROI: {t[n_projects][available_budget]}\n')

        output_file.write(f'Fund remaining: {budget_remaining}')
