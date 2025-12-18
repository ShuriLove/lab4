ITEMS = [
    {'name': 'Винтовка',   'code': 'r', 'size': 3, 'value': 25},
    {'name': 'Пистолет',   'code': 'p', 'size': 2, 'value': 15},
    {'name': 'Боекомплект','code': 'a', 'size': 2, 'value': 15},
    {'name': 'Аптечка',    'code': 'm', 'size': 2, 'value': 20},
    {'name': 'Ингалятор',  'code': 'i', 'size': 1, 'value': 5},
    {'name': 'Нож',        'code': 'k', 'size': 1, 'value': 15},
    {'name': 'Топор',      'code': 'x', 'size': 3, 'value': 20},
    {'name': 'Оберег',     'code': 't', 'size': 1, 'value': 25},
    {'name': 'Фляжка',     'code': 'f', 'size': 1, 'value': 15},
    {'name': 'Антидот',    'code': 'd', 'size': 1, 'value': 10},
    {'name': 'Еда',        'code': 's', 'size': 2, 'value': 20},
    {'name': 'Арбалет',    'code': 'c', 'size': 2, 'value': 20},
]

INDEX_INHALER = next(i for i, it in enumerate(ITEMS) if it['code'] == 'i')
INDEX_ANTIDOTE = next(i for i, it in enumerate(ITEMS) if it['code'] == 'd')


def search_best_load(cells, disease, start_score):
    n = len(ITEMS)
    best_score = None
    best_mask = 0
    best_size = 0
    good_sets = []

    for mask in range(1 << n):
        total_size = 0
        total_value = 0

        for i in range(n):
            if mask & (1 << i):
                total_size += ITEMS[i]['size']
                total_value += ITEMS[i]['value']

        if total_size > cells:
            continue

        if disease == 'asthma' and not (mask & (1 << INDEX_INHALER)):
            continue
        if disease == 'paranoia' and not (mask & (1 << INDEX_ANTIDOTE)):
            continue

        final_score = start_score + total_value

        if final_score > 0:
            good_sets.append((final_score, mask, total_size))

        if best_score is None or final_score > best_score:
            best_score = final_score
            best_mask = mask
            best_size = total_size

    return best_score, best_mask, best_size, good_sets


def mask_to_items(mask):
    result = []
    for i, it in enumerate(ITEMS):
        if mask & (1 << i):
            result.append(it)
    return result


def print_inventory_grid(width, height, chosen_items):
    cells = []
    for it in chosen_items:
        cells.extend([it['code']] * it['size'])

    total_cells = width * height
    if len(cells) > total_cells:
        raise ValueError('Слишком много предметов для такого инвентаря')

    if len(cells) < total_cells:
        cells.extend(['.'] * (total_cells - len(cells)))

    print('Инвентарь:')
    for row in range(height):
        row_cells = cells[row * width : (row + 1) * width]
        print('[' + ']['.join(row_cells) + ']')
    print()


def main():
    width, height = 3, 3       
    disease = 'none'           
    start_score = 10          
    cells = width * height

    best_score, best_mask, best_size, good_sets = search_best_load(
        cells, disease, start_score
    )
    best_items = mask_to_items(best_mask)

    print('\nОсновная задача\n')
    print(f'Всего ячеек: {cells}')
    print(f'Стартовый счёт: {start_score}')
    print('Лучший набор предметов:')
    for it in best_items:
        print(f'- {it['name']} ({it['code']}), размер {it['size']}, очков {it['value']}')
    print(f'Занято ячеек: {best_size} из {cells}')
    print(f'Итоговые очки выживания: {best_score}\n')

    print_inventory_grid(width, height, best_items)

    print('Всего допустимых комбинаций (итоговый счёт > 0):', len(good_sets))
    good_sets.sort(reverse=True)

    print('\nПервые 20 комбинаций:')
    for final, mask, used in good_sets[:20]:
        items_here = mask_to_items(mask)
        codes = [it['code'] for it in items_here]
        print(f'Очки: {final:3d}, ячеек: {used}, вещи: {''.join(codes)}')

    cells7 = 7
    best_score7, best_mask7, best_size7, _ = search_best_load(
        cells7, disease, start_score
    )

    print('\nДоп. задача: рюкзак на 7 ячеек\n')
    if best_score7 is None:
        print('Решений нет: ни один набор не даёт положительный итоговый счёт.')
    else:
        items7 = mask_to_items(best_mask7)
        print(f'Лучший итоговый счёт: {best_score7}')
        print(f'Занято ячеек: {best_size7} из {cells7}')
        print('Набор предметов:')
        for it in items7:
            print(f'- {it['name']} ({it['code']}), размер {it['size']}, очков {it['value']}')

        print()
        print_inventory_grid(7, 1, items7)


if __name__ == '__main__':
    main()
