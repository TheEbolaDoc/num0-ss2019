from math import sin, radians, degrees, pi
from itertools import tee

# class Point():
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def __str__(self):
#         return f"({self.x}, {self.y})"

class Neville:
    def __init__(self, p):
        """p(x) := (x; f; [x_0, ... , x_n])"""
        self.x = p[0]
        self.func = p[1]
        # for each x calculate the corresponding y and eliminate duplicates
        self.grid_points = [(x, self.func(x)) for x in p[2]]
        self.pik = [
            list() if i != 0
            else [x_y[1] for x_y in self.grid_points]
            for i in range(len(self.grid_points))
        ]
        # print(self.pik)

    def compute(self):
        for k in range(len(self.pik)-1):
            for i in range(len(self.pik[k])-1):

                # print("k", k)
                # print("i", i)
                # print("p_(i,k-1)", self.pik[k][i+1])
                # print("x", degrees(self.x))
                # print(f"x_{i}", degrees(self.grid_points[i+1][0]))
                # print("x_i-k", degrees(self.grid_points[i-k][0]))
                # print("p_(i-1,k-1)", self.pik[k][i])1
                # print("----------")

                next = self.pik[k][i+1] + (self.x -
                        self.grid_points[i+1][0])/(self.grid_points[i+1][0] - self.grid_points[i-k][0]) * (self.pik[k][i+1] - self.pik[k][i])
                self.pik[k+1].append(next)
        return self.pik[len(self.pik)-1][0]

    def print_piktable(self):
        import copy
        local = copy.deepcopy(self.pik)
        # fill the matrix
        local = [l + [None]*(len(self.pik)-len(l)) for l in local]
        # transpose it
        local = [[local[j][i] for j in range(len(local))] for i in range(len(local[0]))]

        x = "      "
        for k in range(len(self.pik)):
            x += f" | p_i{k} "
        print(x)
        print(" " + "-" * len(x))
        for k in range(len(local)):
            x = f" i = {k}"
            for i in range(len(local[k])):
                if local[k][i] is not None:
                    x += f" | {local[k][i]:5.3f}"
                else:
                    x += " |      "
            print(x)

    def plot(self):
        pass

def main():
    x_n = [0, 30, 60, 90]
    # transform the values from degree to radian
    x_n = [radians(x) for x in x_n]

    # p(x) := (x; f; [x_0, ... , x_n])
    px = [radians(45), sin, x_n]

    sin_interpol = Neville(px)
    print(sin_interpol.compute())
    sin_interpol.print_piktable()

def pairwise(iterable):
    """ Creates pairs which follow each other in the list """
    first, second = tee(iterable)
    next(second, None)
    return zip(fist, second)


if __name__ == "__main__":
    main()
