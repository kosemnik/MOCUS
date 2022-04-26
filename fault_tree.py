import cutsets
import random
import math
from itertools import *
import pydot
import os
from typing import Dict
import itertools


class Tree():
    def __init__(self, event_count):
        self.tree = Tree.tree_generation(event_count)
        while not self.tree:
            self.tree = Tree.tree_generation(event_count)

    def tree_generation(event_count):
        result = []

        basic_events, events = [], []
        for code in range(65, 91):
            basic_events.append('base' + chr(code))
            events.append(chr(code))
        used_events_parent, used_events = [], []

        count = 0
        while count != event_count:
            '''
            Здесь проверка на возможность расширения дерева. 
            Вдруг генерация дала все листья базовые, т.е. без возможности расширения
            '''
            if len(result) > 0:
                is_break = True
                for result_elem in result:
                    for children in result_elem[2]:
                        if len(children) != 5 and "base" not in children and children not in used_events_parent:
                            is_break = False
                if is_break:
                    return False

            parent = Tree.__get_parent(count, result, used_events_parent)
            if parent is None:
                continue
            count += 1
            event, children_count = Tree.__get_type()
            children = Tree.__get_children(children_count, basic_events, events, event_count, used_events)

            result.append((parent, event, children))

        return result

    def __get_parent(count, result, used_events_parent):
        if count == 0:
            parent = "TOP"
        else:
            number1 = random.randint(0, len(result) - 1)
            number2 = random.randint(0, len(result[number1][2]) - 1)
            parent = result[number1][2][number2]
            if "base" in parent or parent in used_events_parent:
                return
            used_events_parent.append(parent)
        return parent

    def __get_type():
        event_number = random.randint(0, 2)  # Здесь выбираем тип вентиля
        children_count = random.randint(2, 5)
        if event_number == 0:
            event = "And"
        elif event_number == 1:
            event = "Or"
        else:
            n = random.randint(2, 5)
            k = str(random.randint(1, n - 1))
            event = (k + 'of' + str(n))
            children_count = n
        return event, children_count

    def __get_children(children_count, basic_events, events, event_count, used_events):
        children, j = [], 0  # Здесь выбираем потомков
        while j != children_count:
            gate_number = random.randint(0, 1)  # Тип потомка (базовое / не базовое)
            if gate_number == 0:
                child = basic_events[random.randint(0, 25)]
                while child in children:
                    child = basic_events[random.randint(0, 25)]
                children.append(child)
            else:
                gate = events[random.randint(0, 25)]
                if gate in used_events:
                    for q in range(1, event_count + 1):
                        if gate * q not in used_events:
                            gate = q * gate
                            break
                used_events.append(gate)
                children.append(gate)
            j += 1
        return children

    def change_tree(self):  # Обрабатываем дерево, меняя вентили n по k для Мокуса
        self.dict = {}
        i = 0
        while True:
            if "of" in self.tree[i][1]:
                new = self.get_combinations(self.tree[i])
                self.tree[i] = (new[0], 'Or', new[2])
                for j in range(len(new[2])):
                    self.tree.insert(i + j + 1, (new[2][j], "And", self.dict[new[2][j]]))
            i += 1
            if i == len(self.tree):
                break

    def get_combinations(self, event):  # Здесь мы приводим вентиль n по k к дизъюнктивной форме с отрицаниями
        k, n = int(event[1].split('of')[0]), int(event[1].split('of')[1])
        count = int(math.factorial(n) / math.factorial(n - k) / math.factorial(k))

        combination_gates = []
        for gate in event[2]:
            combination_gates.append(gate)
            combination_gates.append('!' + gate)

        real_combination = []
        for combination in combinations(combination_gates, n):
            count_not_gate = 0  # Убираем комбинации, в которых не задействовано нужное колво событий
            for j in combination:
                if str(j)[0] == '!':
                    count_not_gate += 1
            if count_not_gate != n - k:
                continue

            is_repeat = False  # Убираем комбинации где одновременно требуется выполнение события и его невыполнение
            for j in range(len(combination) - 1):
                for i in range(j + 1, len(combination)):
                    if combination[j][0] == '!' and combination[j].split('!')[1] == combination[i] or \
                            combination[j][0] != '!' and combination[i][0] == '!' and \
                            combination[j] == combination[i].split('!')[1]:
                        is_repeat = True
            if is_repeat:
                continue
            real_combination.append(combination)

        keys = []
        for i in range(count):
            self.dict[event[0] + str(i)] = real_combination[i]
            keys.append(event[0] + str(i))

        event = (event[0], 'Or', keys)
        return event

    def draw_tree(self):
        g = pydot.Dot(graph_type='digraph')
        for i in range(len(self.tree)):
            for children in range(len(self.tree[i][2])):
                first = self.tree[i][0] + '\n' + self.tree[i][1]
                second = self.tree[i][2][children]
                for q in range(i, len(self.tree)):
                    if self.tree[i][2][children] == self.tree[q][0]:
                        second = second + '\n' + self.tree[q][1]
                g.add_edge(pydot.Edge(first, second))
        g.write_png("result.png")
        os.startfile("result.png")

    def get_cutsets(self):
        return self.result_interpretation(cutsets.mocus(self.tree))

    def result_interpretation(self, cs):
        for i in range(len(cs)):    # Убираем промежуточные события для вентилей k по n
            for j in range(len(cs[i])):
                if cs[i][j] in self.dict:
                    for elem in self.dict[cs[i][j]]:
                        cs[i].append(elem)
                    cs[i].pop(j)

        for i in range(len(cs)):    # Убираем из вариантов события с отрицанием
            for j in range(len(cs[i]) - 1, -1, -1):
                if cs[i][j][0] == '!':
                    cs[i].pop(j)

        for i in range(len(cs)):    # Здесь еще подправлю логику
            cs[i] = list(set(cs[i]))
        result = []
        for i in cs:
            if not i:
                continue
            can_add = True
            for j in result:
                if set(j) <= set(i):
                    can_add = False
            if can_add:
                result.append(i)
        result.sort(key=len)

        return result