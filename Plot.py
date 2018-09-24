import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import math
import csv


class Scope:
    '''
    h ( t ) = 3 * pi * exp(-lambda [ t ] )
    where lambda ( t ) = 5 * sin ( 2 * pi * 1 * t )
    '''

    def __init__(self, ax, fig, min_t=0, max_t=5, interval=0.0499):
        self.ax = ax
        self.fig = fig
        self.t = np.arange(min_t, max_t, interval)
        self.save_csv = False
        # Calculating lambda(t)
        self.l = [self.calc_lambda(val) for val in self.t]
        # Calculate h(lambda)
        self.h = [self.calc_h(val) for val in self.l]

    def change_t(self, min_t, max_t, interval):
        self.t = np.arange(min_t, max_t, interval)
        self.l = [self.calc_lambda(val) for val in self.t]
        self.h = [self.calc_h(val) for val in self.l]



    def update_data(self):
        #graph_data = open('plot_data.txt', 'rw')
        file_changed = False
        with open('plot_data.txt', 'r') as data_file:
            lines = data_file.readlines()

            print('lines[0]: {}'.format(lines[0].rstrip().split(',')) )

            new_t_min, new_t_max = lines[0].rstrip().split(',')
            new_t_interval = lines[1]
            self.change_t(float(new_t_min), float(new_t_max), float(new_t_interval))
            # Check so there is a third row and if saving to csv should be done
            if len(lines) > 2:
                if lines[2].rstrip() == 'True':
                    self.save_csv = True
                    lines[2] = 'False\n'
                    file_changed = True
        # If the content of file has been changed the new changes should be written to fiel
        if file_changed:
            with open('plot_data.txt', 'w') as data_file:
                data_file.writelines(lines)

    # Argument i is the vlue of the animation itteration variable
    def save_to_csv(self, i):
        with open('graph_data{}'.format(i), 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for i, val in enumerate(self.t):
                row = [val, self.h[i]]
                writer.writerow(row)




    def animate(self, i):
        print('is animating, i: {}' .format(i))
        self.update_data()
        self.plot()
        if self.save_csv:
            print('graph should be saved to csv')
            self.save_to_csv(i)
            self.save_csv = False



    def calc_h(self, l):
        return 3 * math.pi * math.exp(-l)

    def calc_lambda(self, t):
        return 5 * math.sin(2 * math.pi * t)

    # Plot the data, and make the plot pritty
    def plot(self):

        #fig, ax = plt.subplots()

        self.ax.clear()
        self.ax.plot(self.t, self.h)

        # ax.set(xlabel='sannolikhet att smitta', ylabel='antal smittade i %',
        #       title='Antal smittade individer i förhållande till smittsannolikhet')
        # ax.grid()

        # fig.savefig("test.png")

if __name__ == '__main__':
    style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    scope = Scope(ax1, fig)
    ani = animation.FuncAnimation(fig, scope.animate, interval=1000)
    plt.show()