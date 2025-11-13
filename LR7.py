def parse_subset_line(line, default_name):
    line = line.strip()
    if ":" in line:
        name, elems_str = line.split(":", 1)
        name = name.strip()
    else:
        name, elems_str = default_name, line
    elems = [x for x in elems_str.strip().split() if x]
    return name if name else default_name, set(elems)

def greedy_set_cover(universe, family_named):
    U = set(universe)
    uncovered = set(U)
    chosen = []
    chosen_names = []
    # Словарь: имя -> множество
    family = {name: set(s) for name, s in family_named}

    while uncovered:
        best_name = None
        best_set = set()
        best_gain = 0
        for name, s in family.items():
            gain = len(s & uncovered)
            if gain > best_gain:
                best_gain = gain
                best_name = name
                best_set = s
        if best_gain == 0:
            # Невозможно покрыть оставшиеся элементы
            return None, None
        chosen.append(best_set)
        chosen_names.append(best_name)
        uncovered -= best_set
        # Чтобы не выбирать одно и то же множество повторно
        family.pop(best_name)

    # Объединение выбранных множеств (должно равняться U)
    covered_union = set().union(*chosen) if chosen else set()
    return chosen_names, covered_union

def main():
    try:
        universe_line = input().strip()
        universe = [x for x in universe_line.split() if x]

        m = int(input().strip())
        family_named = []
        for i in range(m):
            name, elems = parse_subset_line(input(), f"S{i+1}")
            # Ограничим элементы универсумом (игнорируя лишние)
            elems = elems & set(universe)
            family_named.append((name, elems))

        chosen_names, covered_union = greedy_set_cover(universe, family_named)
        if chosen_names is None:
            print("Невозможно покрыть все элементы универсального множества")
            return

        print("Выбранные множества (в порядке выбора):")
        for name in chosen_names:
            print(name)
        print("Покрытые элементы:", " ".join(sorted(covered_union, key=lambda x: (len(x), x))))
        print("Количество выбранных множеств:", len(chosen_names))
        print("Суммарно покрыто элементов:", len(covered_union))
    except Exception as e:
        print("Ошибка ввода:", e)

if __name__ == "__main__":
    main()
#Ввод: 
#1 2 3 4 5 6 7 8 9 10
#5
#S1: 1 2 3
#S2: 2 4 6
#S3: 3 5 7
#S4: 1 4 7 10
#S5: 5 6 8 9


#Вывод: Выбранные множества (в порядке выбора):
#S4
#S5
#S1
#Покрытые элементы: 1 2 3 4 5 6 7 8 9 10
#Количество выбранных множеств: 3
#Суммарно покрыто элементов: 10