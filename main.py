import fault_tree


if __name__ == '__main__':
    tree = fault_tree.Tree(7)

    tree.draw_tree()
    tree.change_tree()
    print(tree.get_cutsets())