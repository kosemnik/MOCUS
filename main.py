import fault_tree
import random
import time


if __name__ == '__main__':
    for i in range(1000):
        tree = fault_tree.Tree(5)

        mocus = tree.get_cutsets_mocus()
        new_cutset = tree.get_cutset_new()

        if new_cutset in mocus:
            print('YES')
        else:
            print('NO')