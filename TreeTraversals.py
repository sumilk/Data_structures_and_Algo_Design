
import pip
try:
    from binarytree import Node
except ModuleNotFoundError:
    pip.main(['install', "binarytree"])
    from binarytree import Node

class TreeUtil:

    @classmethod
    def _construct_tree_from_preorder(cls, pre_order, low, high):
        
        # Base Case
        if (low > high):
            return None

        root = Node(pre_order[cls.preIndex])
        cls.preIndex += 1

        if low == high:
            return root

        r_root = -1

        for i in range(low, high + 1):
            if (pre_order[i] > root.value):
                r_root = i
                break

        if r_root == -1:
            r_root = cls.preIndex + (high - low)

        root.left = cls._construct_tree_from_preorder(pre_order, cls.preIndex, r_root - 1)

        root.right = cls._construct_tree_from_preorder(pre_order, r_root, high)

        return root


    @classmethod
    def construct_tree_from_preorder(cls, pre_order):
        size = len(pre_order)
        cls.preIndex = 0
        return cls._construct_tree_from_preorder(pre_order, 0, size - 1)


    @classmethod
    def _construct_tree_from_in_post(cls, in_order, post_order, inStrt, inEnd, pIndex):

        # Base case
        if (inStrt > inEnd):
            return None

        node = Node(post_order[pIndex[0]])
        pIndex[0] -= 1

        if (inStrt == inEnd):
            return node

        iIndex = cls.search_in_order(in_order, inStrt, inEnd, node.value)

        node.right = TreeUtil._construct_tree_from_in_post(in_order, post_order, iIndex + 1,
                                                           inEnd, pIndex)
        node.left = TreeUtil._construct_tree_from_in_post(in_order, post_order, inStrt,
                                                          iIndex - 1, pIndex)

        return node


    @classmethod
    def construct_tree_from_in_post(cls, in_order, post_order):
        pIndex = [len(in_order) - 1]
        return TreeUtil._construct_tree_from_in_post(in_order, post_order, 0, len(in_order) - 1, pIndex)

    @classmethod
    def _construct_tree_from_in_pre(cls, in_order, pre_order, inStrt, inEnd):

        if (inStrt > inEnd):
            return None

        node = Node(pre_order[cls.preIndex])
        cls.preIndex += 1

        if inStrt == inEnd:
            return node

        inIndex = cls.search_in_order(in_order, inStrt, inEnd, node.value)

        node.left = cls._construct_tree_from_in_pre(in_order, pre_order, inStrt, inIndex - 1)
        node.right = cls._construct_tree_from_in_pre(in_order, pre_order, inIndex + 1, inEnd)

        return node

    @classmethod
    def construct_tree_from_in_pre(cls, in_order, pre_order):
        cls.preIndex = 0
        return cls._construct_tree_from_in_pre(in_order, pre_order, 0, len(in_order) - 1)


    @classmethod
    def _construct_tree_from_pre_post(cls, pre_order, post_order, l, h, size):

        # Base case
        if (cls.preIndex >= size or l > h):
            return None

        root = Node(pre_order[cls.preIndex])
        cls.preIndex += 1

        if (l == h or cls.preIndex >= size):
            return root

        i = l
        while i <= h:
            if (pre_order[cls.preIndex] == post_order[i]):
                break
            i += 1

        if (i <= h):
            root.left = cls._construct_tree_from_pre_post(pre_order, post_order, l, i, size)
            root.right = cls._construct_tree_from_pre_post(pre_order, post_order, i + 1, h - 1, size)

        return root


    @classmethod
    def construct_tree_from_pre_post(cls, pre_order, post_order):

        size = len(pre_order)

        cls.preIndex = 0

        return cls._construct_tree_from_pre_post(pre_order, post_order, 0,
                                                 size - 1, size)


    @staticmethod
    def search_in_order(arr, strt, end, value):
        i = 0
        for i in range(strt, end + 1):
            if (arr[i] == value):
                break
        return i

    @staticmethod
    def print_in_order(root):
        if root is None:
            return
        TreeUtil.print_in_order(root.left)
        print(root.value, end=' ')
        TreeUtil.print_in_order(root.right)

    @staticmethod
    def print_pre_order(root):
        if root is None:
            return
        print(root.value, end=' ')
        TreeUtil.print_pre_order(root.left)
        TreeUtil.print_pre_order(root.right)

    @staticmethod
    def print_post_order(root):
        if root is None:
            return

        TreeUtil.print_post_order(root.left)
        TreeUtil.print_post_order(root.right)
        print(root.value, end=' ')



if __name__ == '__main__':
    # pre_order = ['F', 'B', 'A', 'D', 'C', 'E', 'G', 'I', 'H']
    #
    # root = TreeUtil.construct_tree_from_preorder(pre_order)
    #
    # print(root)
    # TreeUtil.print_in_order(root)
    # print('\n')
    # TreeUtil.print_pre_order(root)
    # print('\n')
    # TreeUtil.print_post_order(root)


    # in_order = [4, 8, 2, 5, 1, 6, 3, 7]
    # post_order = [8, 4, 5, 2, 6, 7, 3, 1]
    #
    # root = TreeUtil.construct_tree_from_in_post(in_order, post_order)
    #
    # print(root)


    # in_order = ['D', 'B', 'E', 'A', 'F', 'C']
    # pre_order = ['A', 'B', 'D', 'E', 'C', 'F']
    # root = TreeUtil.construct_tree_from_in_pre(in_order, pre_order)
    #
    # print(root)

    pre_order = [1, 2, 4, 8, 9, 5, 3, 6, 7]
    post_order = [8, 9, 4, 5, 2, 6, 7, 3, 1]

    root = TreeUtil.construct_tree_from_pre_post(pre_order, post_order)
    print(root)

