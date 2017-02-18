import numpy as np

from cut import Cut
from point import Point

FILENAME = 'data/small.in'
OUTFILENAME = FILENAME.replace('.in', '.out')

with open(FILENAME) as infile:
    R, C, L, H = [int(i) for i in infile.readline().split()]
    pizza = np.array(list(map(lambda x: list(x)[:-1], infile.readlines())))


def contains(current_cuts, cut):
    answer = False
    for exist_cut in current_cuts:
        answer = answer or (
            (
                exist_cut.begin.x <= cut.begin.x <= exist_cut.end.x and exist_cut.begin.y <= cut.begin.y <= exist_cut.end.y)
            or
            (
                exist_cut.begin.x <= cut.end.x <= exist_cut.end.x and exist_cut.begin.y <= cut.end.y <= exist_cut.end.y)
            or
            (
                exist_cut.begin.x <= cut.end.x <= exist_cut.end.x and exist_cut.begin.y <= cut.begin.y <= exist_cut.end.y)
            or
            (
                exist_cut.begin.x <= cut.begin.x <= exist_cut.end.x and exist_cut.begin.y <= cut.end.y <= exist_cut.end.y)
        )
    return answer


def score(current_cuts):
    answer = 0
    for cut in current_cuts:
        answer += cut.square()
    return answer


def approciate_way(current_cuts):
    global all_mushrooms
    global all_tomatoes
    global all_square
    global best_score
    used_mushrooms = 0
    used_tomatoes = 0
    current_score = score(current_cuts)
    for exist_cut in current_cuts:
        used_mushrooms += exist_cut.count('M')
        used_tomatoes += exist_cut.count('T')
    least_mushrooms = all_mushrooms - used_mushrooms
    least_tomatoes = all_tomatoes - used_tomatoes
    return best_score < current_score + min((min(least_mushrooms, least_tomatoes) / L) * H, all_square - current_score)


def find_cut(x, y, current_cuts):
    global best_score
    global best_cuts
    for x0 in range(x, C):
        for y0 in range(y, R):
            for x1 in range(x0, C):
                for y1 in range(y0, R):
                    if (x1 - x0 + 1) * (y1 - y0 + 1) <= H:
                        cut = Cut(Point(x0, y0), Point(x1, y1))
                        if cut.valid() and not contains(current_cuts, cut):
                            current_cuts.append(cut)
                            if approciate_way(current_cuts):
                                find_cut(x0, y0, current_cuts)
                                if score(current_cuts) > best_score:
                                    best_score = score(current_cuts)
                                    best_cuts = current_cuts.copy()
                            current_cuts.remove(cut)


def main():
    print('R = {}, C = {}, L = {}, H = {}'.format(R, C, L, H))
    print(pizza)
    current_cuts = []

    for x0 in range(0, C):
        for y0 in range(0, R):
            find_cut(x0, y0, current_cuts.copy())

    with open(OUTFILENAME, 'w') as outfile:
        print(best_score)
        outfile.write(str(len(best_cuts)))
        outfile.write('\n')
        for cut in best_cuts:
            outfile.writelines('{} {} {} {}'.format(cut.begin.y, cut.begin.x, cut.end.y, cut.end.x))
            outfile.write('\n')


if __name__ == '__main__':
    best_score = 0
    best_cuts = []
    all_pizza = Cut(Point(0, 0), Point(C - 1, R - 1))
    all_mushrooms = all_pizza.count('M')
    all_tomatoes = all_pizza.count('T')
    all_square = all_pizza.square()
    main()
