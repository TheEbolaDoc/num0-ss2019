from math import sin, radians, degrees, pi


class Neville:
    def __init__(self, p):
        """p(x) := (x; f; [x_0, ... , x_n])"""
        self.x = p[0]
        self.func = p[1]
        # for each x calculate the corresponding y and eliminate duplicates
        self.grid_points = [(x, self.func(x)) for x in p[2]]
        self.pik = [
            [None for _ in range(i)]
            if i != 0 else [x_y[1] for x_y in self.grid_points]
            for i in range(len(self.grid_points))
        ]

    def compute(self, verbose=False):
        if verbose:
            max_len = 0
        for k in range(len(self.pik) - 1):
            for i in range(k, len(self.pik[k]) - 1):
                next_pik = self.pik[k][
                    i+1] + (self.x - self.grid_points[i+1][0]) / (
                        self.grid_points[i+1][0] - self.grid_points[i-k][0]
                    ) * (self.pik[k][i+1] - self.pik[k][i])
                if verbose:
                    compute_str = f"{next_pik:5.4f} = {self.pik[k][i+1]:5.4f} + "
                    compute_str += f"({degrees(self.x):3.1f} - {degrees(self.grid_points[i+1][0]):3.1f})"
                    compute_str += f"/({degrees(self.grid_points[i+1][0]):3.1f} - {degrees(self.grid_points[i-k][0]):4.1f})"
                    compute_str += f" * ({self.pik[k][i+1]:5.4f} - {self.pik[k][i]:5.4f})"
                    compute_str += f" | i={i}, k={k}"
                    max_len = max(max_len, len(compute_str))
                    print(compute_str)
                self.pik[k + 1].append(next_pik)
        if verbose:
            print("-" * max_len)
        return self.pik[len(self.pik)-1][len(self.pik[len(self.pik)-1]) - 1]

    def piktable(self):
        """ this function only creates the table as we created """
        # transpose it
        local = [[self.pik[j][i] for j in range(len(self.pik))]
                 for i in range(len(self.pik[0]))]

        output = " " * 6
        for k in range(len(self.pik)):
            output += f" | p_i{k} "
        output += "\n"
        output += " " + "-" * len(output) + "\n"
        for k in range(len(local)):
            output += f" i = {k}"
            for i in range(len(local[k])):
                if local[k][i] is not None:
                    output += f" | {local[k][i]:5.3f}"
                else:
                    output += " |" + " " * 6
            output += "\n"
        return output

    def plot(self):
        pass


def main():
    x_n = [0, 30, 60, 90]
    # transform the values from degree to radian
    x_n = [radians(x) for x in x_n]

    # p(x) := (x; f; [x_0, ... , x_n])
    px = [radians(45), sin, x_n]

    sin_interpol = Neville(px)
    print("Result: ", sin_interpol.compute(verbose=True), "\n")
    print(sin_interpol.piktable())

    # create a scaled version of the sin() function
    scaled_sin = lambda n: lambda x: sin(n*x)
    # for i in [2, 4, 8]:
    #     px = [radians(45), scaled_sin(i), x_n]
    #     sin_interpol_b = Neville(px)
    #     print(sin_interpol_b.compute())

if __name__ == "__main__":
    main()
