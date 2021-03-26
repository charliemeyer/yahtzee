import random
import itertools


def get_subsets(length):
    subsets = []
    l = range(length)
    for i in range(0, length + 1):
        subsets += itertools.combinations(l, i)
    return subsets


yahtzee_subsets = get_subsets(5)


def roll():
    return random.randint(1, 6)


def get_numbered(num):
    return lambda dice: sum([i for i in dice if i == num])


def true(roll):
    return True


def get_freqs(dice):
    freqs = {}
    for d in dice:
        if d in freqs:
            freqs[d] += 1
        else:
            freqs[d] = 1
    return freqs


def has(num):
    def has_dice(dice):
        freqs = get_freqs(dice)
        for k in freqs:
            if freqs[k] >= num:
                return True
        return False

    return has_dice


def sum_dice(dice):
    return sum(dice)


def is_full_house(dice):
    freqs = get_freqs(dice)
    has_three = False
    has_two = False
    for k in freqs:
        has_three = has_three or freqs[k] == 3
        has_two = has_two or freqs[k] == 2
    return has_three and has_two


def straight(num):
    def straight_dice(dice):
        sorted_dice = sorted(dice)
        max_straight = 0
        straight = 1
        for i in range(len(dice) - 1):
            if (dice[i + 1] - dice[i]) == 1:
                straight += 1
            else:
                if straight > max_straight:
                    max_straight = straight
                straight = 1
        if straight > max_straight:
            max_straight = straight
        return max_straight >= num
    return straight_dice


strategies = {
    "one": {
        "elligible": true,
        "score": get_numbered(1),
        "max": 5
    },
    "two": {
        "elligible": true,
        "score": get_numbered(2),
        "max": 10
    },
    "three": {
        "elligible": true,
        "score": get_numbered(3),
        "max": 15
    },
    "four": {
        "elligible": true,
        "score": get_numbered(4),
        "max": 20
    },
    "five": {
        "elligible": true,
        "score": get_numbered(5),
        "max": 25
    },
    "six": {
        "elligible": true,
        "score": get_numbered(6),
        "max": 30
    },
    "four_of_a_kind": {
        "elligible": has(4),
        "score": sum_dice,
        "max": 36
    },
    "three_of_a_kind": {
        "elligible": has(3),
        "score": sum_dice,
        "max": 36
    },
    "full_house": {
        "elligible": is_full_house,
        "score": lambda dice: 25,
        "max": 25
    },
    "small_straight": {
        "elligible": straight(4),
        "score": lambda dice: 30,
        "max": 30
    },
    "large_straight": {
        "elligible": straight(5),
        "score": lambda dice: 40,
        "max": 40
    },
    "chance": {
        "elligible": true,
        "score": sum_dice,
        "max": 30
    },
    "yahtzee": {
        "elligible": has(5),
        "score": lambda dice: 50,
        "max": 50,
    }
}

# todo: test total score
bonus_yahtzee_order = ["one", "two", "three", "four", "five", "six", "four_of_a_kind",
                       "three_of_a_kind", "full_house", "small_straight", "large_straight", "chance", "yahtzee"]


def run_tests():
    assert(has(2)([1, 2, 3, 4, 5]) == False)
    assert(has(2)([1, 1, 3, 4, 5]) == True)
    assert(has(3)([1, 1, 3, 4, 5]) == False)
    assert(has(3)([1, 1, 1, 4, 5]) == True)
    assert(has(4)([1, 1, 1, 4, 5]) == False)
    assert(has(4)([1, 1, 1, 1, 5]) == True)
    assert(has(5)([1, 1, 1, 1, 5]) == False)
    assert(has(5)([1, 1, 1, 1, 1]) == True)
    assert(is_full_house([1, 1, 3, 3, 2]) == False)
    assert(is_full_house([1, 1, 3, 3, 3]) == True)
    assert(straight(4)([1, 1, 3, 4, 6]) == False)
    assert(straight(4)([1, 2, 3, 4, 6]) == True)
    assert(straight(5)([1, 2, 3, 4, 6]) == False)
    assert(straight(5)([1, 2, 3, 4, 5]) == True)
    assert(get_score("one", [1, 2, 3, 4, 5]) == 1)
    assert(get_score("one", [1, 2, 1, 4, 1]) == 3)
    assert(get_score("one", [2, 2, 2, 4, 2]) == 0)
    assert(get_score("two", [1, 2, 3, 4, 5]) == 2)
    assert(get_score("two", [1, 3, 1, 4, 1]) == 0)
    assert(get_score("two", [2, 2, 2, 4, 2]) == 8)
    assert(get_score("three", [1, 2, 3, 4, 5]) == 3)
    assert(get_score("three", [1, 2, 1, 4, 1]) == 0)
    assert(get_score("three", [2, 3, 3, 4, 3]) == 9)
    assert(get_score("four", [1, 2, 3, 4, 5]) == 4)
    assert(get_score("four", [1, 2, 1, 3, 1]) == 0)
    assert(get_score("four", [2, 3, 4, 4, 3]) == 8)
    assert(get_score("five", [1, 2, 3, 4, 5]) == 5)
    assert(get_score("five", [1, 2, 1, 4, 1]) == 0)
    assert(get_score("five", [5, 5, 5, 5, 5]) == 25)
    assert(get_score("six", [1, 2, 3, 4, 6]) == 6)
    assert(get_score("six", [1, 2, 1, 4, 1]) == 0)
    assert(get_score("six", [6, 3, 3, 4, 6]) == 12)
    assert(get_score("three_of_a_kind", [1, 2, 3, 4, 5]) == 0)
    assert(get_score("three_of_a_kind", [1, 1, 2, 2, 2]) == 8)
    assert(get_score("three_of_a_kind", [2, 2, 2, 6, 5]) == 17)
    assert(get_score("four_of_a_kind", [1, 2, 3, 4, 5]) == 0)
    assert(get_score("four_of_a_kind", [1, 2, 3, 4, 5]) == 0)
    assert(get_score("four_of_a_kind", [1, 2, 3, 4, 5]) == 0)
    assert(get_score("full_house", [1, 1, 2, 2, 2]) == 25)
    assert(get_score("full_house", [6, 6, 6, 5, 4]) == 0)
    assert(get_score("full_house", [6, 4, 6, 4, 6]) == 25)
    assert(get_score("small_straight", [1, 2, 3, 4, 5]) == 30)
    assert(get_score("small_straight", [1, 2, 2, 4, 5]) == 0)
    assert(get_score("small_straight", [3, 2, 3, 4, 6]) == 0)
    assert(get_score("large_straight", [1, 2, 3, 4, 5]) == 40)
    assert(get_score("large_straight", [2, 2, 3, 4, 5]) == 0)
    assert(get_score("large_straight", [1, 2, 3, 3, 5]) == 0)
    assert(get_score("chance", [1, 2, 3, 4, 5]) == 15)
    assert(get_score("chance", [6, 6, 6, 6, 6]) == 30)
    assert(get_score("chance", [1, 2, 1, 4, 1]) == 9)
    assert(get_score("yahtzee", [1, 2, 3, 4, 5]) == 0)
    assert(get_score("yahtzee", [1, 1, 1, 1, 5]) == 0)
    assert(get_score("yahtzee", [1, 1, 1, 1, 1]) == 50)


def get_score(strategy_name, dice, used_strategies):
    score = 0
    if (strategy_name == "yahtzee" and strategy_name in used_strategies):
        score += 100
        for strategy in bonus_yahtzee_order:
            if strategy in used_strategies:
                continue
            # won't be yahtzee again so recursion is safe
            score += get_score(strategy_name, dice, used_strategies)
            if score > 0:
                return (score, strategy)

    else:
        strategy = strategies[strategy_name]
        if strategy["elligible"](dice):
            return score += strategy["score"](dice)
    return (score, strategy)


def get_total_score(game_scores):
    upper = ["one", "two", "three", "four", "five", "six"]
    upper_scores = [game_scores[u] for u in upper]
    total_score = 0
    if sum(upper_scores) >= 63:
        total_score += 35
    total_score += sum([game_scores[k] for k in game_scores.keys()])
    return total_score


def get_dice():
    return [roll() for i in range(5)]


def get_best_strategy(dice, used_strategies):
    best_strategy = ""
    best_ratio = 0
    best_score = 0
    for strategy_name in strategies:
        if strategy_name in used_strategies and strategy_name != "yahtzee":
            continue
        score = get_score(strategy_name, dice)
        ratio = score / strategies[strategy_name]["max"]
        if ratio == best_ratio:
            if score > best_score:
                best_strategy = strategy_name
                best_score = score
                best_ratio = ratio
        elif ratio > best_ratio:
            best_strategy = strategy_name
            best_ratio = ratio
            best_score = score
        if best_strategy == "":
            best_strategy = strategy_name
    return (best_strategy, best_ratio)


def get_best_sub(dice, used_strategies):
    best_sub = ()
    best_sub_ratio = 0
    for sub in yahtzee_subsets:
        sub_ratios = []
        for sim_num in range(100):
            sim_dice = [roll() if i in sub else dice[i]
                        for i in range(len(dice))]
            (best_strat, best_ratio) = get_best_strategy(
                sim_dice, used_strategies)
            sub_ratios.append(best_ratio)
        sub_average_ratio = sum(sub_ratios) / len(sub_ratios)
        if sub_average_ratio > best_sub_ratio:
            best_sub = sub
            best_sub_ratio = sub_average_ratio
    return best_sub


def run_yahtzee():
    used_strategies = set()
    game_score = 0
    game_scores = {}
    while len(used_strategies) < len(strategies):
        dice_1 = get_dice()
        best_sub_1 = get_best_sub(dice_1, used_strategies)
        # print("have", dice_1, "swapping", best_sub_1)
        dice_2 = [roll() if i in best_sub_1 else dice_1[i]
                  for i in range(len(dice_1))]
        best_sub_2 = get_best_sub(dice_2, used_strategies)
        # print("have", dice_2, "swapping", best_sub_2)
        dice_3 = [roll() if i in best_sub_2 else dice_2[i]
                  for i in range(len(dice_2))]
        (try_strat, real_ratio) = get_best_strategy(dice_3, used_strategies)
        (real_score, real_strat) = get_score(
            try_strat, dice_3, used_strategies)
        game_scores[real_strat] = real_score
        used_strategies.add(real_strat)
        # print(
        #     f"using strategy {real_strat} for dice {dice_3}, scored {real_score}")
    return game_scores


scores = []

for i in range(10):
    print("-------- game", i, "-------------")
    game_scores = run_yahtzee()
    for strat in strategies:
        print(strat, "=", game_scores[strat])
    total_score = get_total_score(game_scores)
    print("total =", total_score)
    scores.append(total_score)

print(f"max = {max(scores)}")
print(f"avg = {sum(scores) / len(scores)}")
