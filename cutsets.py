def __top_process(tree, result):
    if tree[0][1] == "And":
        result.append(tree[0][2])
    elif tree[0][1] == "Or":
        for child in tree[0][2]:
            result.append([child])

def __and_process(tree, i, result):
    j = 0
    while True:
        for q in range(len(result[j])):
            if result[j][q] == tree[i][0]:
                new_elem = result[j].copy()
                new_elem.remove(result[j][q])
                for child in tree[i][2]:
                    new_elem.append(child)
                if __is_contradictory(new_elem):
                    result[j] = []
                    break
                result[j] = list(set(new_elem))
                break

            elif '!' in result[j][q] and result[j][q].split('!')[1] == tree[i][0]:
                new_elem = result[j].copy()
                new_elem.remove(result[j][q])
                success = 0
                for z in range(len(tree[i][2])):
                    new_elem.append(__flip(tree[i][2][z]))
                    if __is_contradictory(new_elem):
                        new_elem = result[j].copy()
                        new_elem.remove(result[j][q])
                        continue
                    success += 1
                    result.insert(j + success, list(set(new_elem)))
                    new_elem = result[j].copy()
                    new_elem.remove(result[j][q])
                result.remove(result[j])
                j += success - 1
                break
        j += 1
        if j == len(result):
            break

def __or_process(tree, i, result):
    j = 0
    while True:
        for q in range(len(result[j])):
            if result[j][q] == tree[i][0]:
                new_elem = result[j].copy()
                new_elem.remove(result[j][q])
                success = 0
                for z in range(len(tree[i][2])):
                    new_elem.append(tree[i][2][z])
                    if __is_contradictory(new_elem):
                        new_elem = result[j].copy()
                        new_elem.remove(result[j][q])
                        continue
                    success += 1
                    result.insert(j + success, list(set(new_elem)))
                    new_elem = result[j].copy()
                    new_elem.remove(result[j][q])
                result.remove(result[j])
                j += success - 1
                break

            elif '!' in result[j][q] and result[j][q].split('!')[1] == tree[i][0]:
                new_elem = result[j].copy()
                new_elem.remove(result[j][q])
                for child in tree[i][2]:
                    new_elem.append(__flip(child))
                if __is_contradictory(new_elem):
                    result[j] = []
                    break
                result[j] = list(set(new_elem))
                break
        j += 1
        if j == len(result):
            break

def __flip(value):
    if '!' in value:
        return value.split('!')[1]
    return '!' + value

def __is_contradictory(cs):
    is_repeat = False
    for j in range(len(cs) - 1):
        for i in range(j + 1, len(cs)):
            if cs[j][0] == '!' and cs[j].split('!')[1] == cs[i] or \
                    cs[j][0] != '!' and cs[i][0] == '!' and \
                    cs[j] == cs[i].split('!')[1]:
                is_repeat = True
    return is_repeat

def mocus(tree):
    print('ДЕРЕВО!!')
    print(tree)
    print('ОТВЕТ!!')
    result = []
    for i in range(len(tree)):
        if i == 0:
            __top_process(tree, result)
        elif tree[i][1] == "And":
            __and_process(tree, i, result)
        else:
            __or_process(tree, i, result)
    return result