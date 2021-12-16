from utility_functions import graph_data
from ast import literal_eval
import matplotlib.pyplot as plt
import pandas as pd


def value_stats(target: str, scale: int, path_prefix: str, verbose: bool = False):
    data = graph_data(target, f'{path_prefix}../')
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    if verbose:
        print(data)
        print(data.info())

    # Value by Color
    colors = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'ColorLess': 0, 'Land': 0}
    for row in data.iterrows():
        card_colors = row[1]['colors']
        card_value = row[1]['value']
        if card_colors is None:
            card_colors = literal_eval(row[1]['color_identity'])
        else:
            card_colors = literal_eval(row[1]['colors'])
        if len(card_colors) != 0:
            for key in colors:
                if key in card_colors:
                    colors[key] += card_value / len(card_colors)
        elif 'Land' in row[1]['type_line']:
            colors['Land'] += card_value
        else:
            colors['ColorLess'] += card_value
    if verbose:
        print(f'\n{data["value"].sum()}')
        print(sum(colors.values()))

    # Contribution to Value by Price Group
    price_groups = {1: 0, 2.5: 0, 5: 0, 10: 0, 20: 0, 50: 0}
    no_max = 0
    for row in data.iterrows():
        card_value = row[1]['value']
        claimed = False
        for key in price_groups:
            if not claimed and card_value < key:
                price_groups[key] += card_value
                claimed = True
        if not claimed:
            no_max += card_value
    if verbose:
        print(sum(price_groups.values()) + no_max)

    # Value by Card Type
    card_types = {'Creature': 0, 'Land': 0, 'Enchantment': 0, 'Sorcery': 0, 'Instant': 0, 'Artifact': 0, 'Planeswalker': 0}
    for row in data.iterrows():
        accepted = [key for key in card_types if key in row[1]['type_line']]
        for item in accepted:
            card_types[item] += (row[1]['value'] / len(accepted))
    if verbose:
        print(sum(card_types.values()))

    fig = plt.figure(figsize=(6.4 * scale, 4.8 * scale))
    plt.title('Value by Color', fontdict={'size': 24, 'family': 'Papyrus'})
    plt.bar(range(len(colors)), colors.values(), color=['White', 'Blue', 'Black', 'Red', 'Green', 'Gray', 'Purple'], edgecolor='black')
    plt.xticks(ticks=range(len(colors)), labels=['White', 'Blue', 'Black', 'Red', 'Green', 'Colorless', 'Land'])
    plt.ylabel('Combined Value')
    plt.savefig(f'{path_prefix}/PNG/{target}/value_by_color.png')
    plt.close()

    fig = plt.figure(figsize=(6.4 * scale, 4.8 * scale))
    plt.title('Distribution of Card Prices', fontdict={'size': 24, 'family': 'Papyrus'})
    plt.hist(data['value'], edgecolor='black')
    plt.ylabel('Count')
    plt.xlabel('Card Value')
    plt.savefig(f'{path_prefix}/PNG/{target}/distribution_of_price.png')
    plt.close()

    fig = plt.figure(figsize=(6.4 * scale, 4.8 * scale))
    plt.title('Contribution to Value by Price Group', fontdict={'size': 24, 'family': 'Papyrus'})
    plt.bar(range(len(price_groups) + 1), list(price_groups.values()) + [no_max], align='edge', width=1, edgecolor='black')
    plt.xticks(ticks=range(len(price_groups) + 2), labels=[0] + list(price_groups) + ['No Max'])
    plt.xlabel('Price Group')
    plt.ylabel('Combined Value')
    plt.savefig(f'{path_prefix}/PNG/{target}/value_by_price_group.png')
    plt.close()

    fig = plt.figure(figsize=(6.4 * scale, 4.8 * scale))
    plt.title('Value by Card Type', fontdict={'size': 24, 'family': 'Papyrus'})
    plt.bar(range(len(card_types)), card_types.values(), edgecolor='black')
    plt.xticks(ticks=range(len(card_types)), labels=card_types.keys(), rotation=-15)
    plt.ylabel('Combined Value')
    plt.savefig(f'{path_prefix}/PNG/{target}/value_by_type.png')
    plt.close()


if __name__ == '__main__':
    value_stats('collection_1', 1, '')
