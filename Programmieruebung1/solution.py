from math import sin, radians, degrees, pi
import numpy as np
import matplotlib.pyplot  as plt


class Neville:
    def __init__(self, p):
        """p(x) := (x; f; [x_0, ... , x_n])"""
        self.x = p[0]
        self.func = p[1]
        self.func_name = "sin(x)"
        # for each x calculate the corresponding y and eliminate duplicates
        self.x_n = p[2]
        self.y_n = [self.func(x) for x in self.x_n]
        self._construct_piktable()

    def _construct_piktable(self):
        self.pik = [
            [None] * len(self.x_n) if i != 0
            else [y for y in self.y_n]
            for i in range(len(self.x_n))
        ]

    def compute(self, x="",verbose=False):
        if not x:
            x = self.x
        self._construct_piktable()
        if verbose:
            self._max_len = 0
        for k in range(1, len(self.pik)):
            for i in range(k, len(self.pik[k])):
                right = (x - self.x_n[i]) / (self.x_n[i] - self.x_n[i-k])
                right *= (self.pik[k-1][i] - self.pik[k-1][i-1])
                self.pik[k][i] = self.pik[k-1][i]
                self.pik[k][i] += right
                if verbose:
                    print(self._compute_str(k, i))
        if verbose:
            print("-" * self._max_len)
        # return the lower right element
        return self.pik[-1][-1]

    def piktable(self):
        """ this function only creates beautiful output"""
        local = [l + [None]*(len(self.pik)-len(l)) for l in self.pik]
        # transpose it
        local = [[local[j][i] for j in range(len(local))]
                 for i in range(len(local[0]))]

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

    def __str__(self):
        return self.piktable()

    def _compute_str(self, k, i):
        compute_str = f"{self.pik[k][i]:5.4f} = {self.pik[k-1][i]:5.4f} + "
        compute_str += f"({degrees(self.x):3.1f} - {degrees(self.x_n[i]):3.1f})"
        compute_str += f"/({degrees(self.x_n[i]):3.1f} - {degrees(self.x_n[i-k]):4.1f})"
        compute_str += f" * ({self.pik[k-1][i]:5.4f} - {self.pik[k-1][i-1]:5.4f})"
        compute_str += f" | i={i}, k={k}"
        self._max_len = max(self._max_len, len(compute_str))
        return compute_str

    def plot(self):
        startx, endx = 0.00001, pi/2
        x = np.linspace(startx, endx, 100)
        y1 = self.func(x)
        y2 = [self.compute(x=i) for i in x]
        y3 = [(i-c) for i,c in zip(y1, y2)]
        y4 = x * (x - pi/2) * (x - pi/3) * (x - pi/6)


        #  Figure  erstellen
        plt.figure()

        #  Plots  erstellen
        plt.plot(x, y1, label=f'{self.func_name}')
        plt.plot(x, y2, label='interpoliert')
        plt.plot(x, y3, 'r--', label=f'{self.func_name}-interpoliert')
        plt.plot(x, y4, label=r'$\omega_3$')

        #  Labels  fuer x- und y-Achse
        plt.xlabel('x-Achse')
        plt.ylabel('y-Achse')

        # Titel , Legende , Grid
        plt.title('Neville Schema')
        plt.legend()
        plt.grid()

        # Plot  anzeigen
        plt.show()
        # plt.savefig(self.func_name+".png", dpi=300)


def main():
    x_n = [0, 30, 60, 90]
    # transform the values from degree to radian
    x_n = [radians(x) for x in x_n]

    # p(x) := (x; f; [x_0, ... , x_n])
    px = [radians(45), np.sin, x_n]

    sin_interpol = Neville(px)
    print(sin_interpol)
    print("Result: ", sin_interpol.compute(verbose=True), "\n")
    print(sin_interpol)
    # sin_interpol.plot()

    # create a scaled version of the sin() function
    scaled_sin = lambda n: lambda x: np.sin(n*x)
    for i in [2, 4, 8]:
        px = [radians(45), scaled_sin(i), x_n]
        sin_interpol_b = Neville(px)
        sin_interpol_b.func_name = f"sin({i}x)"
        print(sin_interpol_b.func_name + ":", sin_interpol_b.compute())
        # sin_interpol_b.plot()


if __name__ == "__main__":
    main()
