import numpy as np
import math
import csv

'''
class for interacting with the function:
h ( t ) = 3 * pi * exp(-lambda [ t ] )
where lambda ( t ) = 5 * sin ( 2 * pi * 1 * t )

By typing in the plot_data.txt file interactions can be made with the plot
1. the first row specifies the max and min values for the t value shown in the plot
2. the second row tells the interval between t values
3. if the third row is set to true it the plotted values will be saved to a csv file
4. if the forth row is set to true an image of the plot will be saved
5. the fifth row controls the label of the plot
6. the sixth row sets the x-label vale of the plot
7. the seventh row sets the y-label value of the plot
'''

class Scope:

    def __init__(self, ax, fig, min_t=0, max_t=5, interval=0.0499):
        # Plot related
        self.ax = ax
        self.fig = fig

        # A list of all the t values for which h will be plotted
        self.t = np.arange(min_t, max_t, interval)
        # Calculating lambda(t)
        self.l = [self.calc_lambda(val) for val in self.t]
        # Calculate h(lambda)
        self.h = [self.calc_h(val) for val in self.l]

        # Interaction parameters
        self.save_csv = False
        self.save_plot = False
        self.set_title = False
        self.plt_title = ''
        self.set_x_label = False
        self.plt_x_label = ''
        self.set_y_label = False
        self.plt_y_label = ''

    def change_t(self, min_t, max_t, interval):
        self.t = np.arange(min_t, max_t, interval)
        self.l = [self.calc_lambda(val) for val in self.t]
        self.h = [self.calc_h(val) for val in self.l]

    # Function for reading data from plot_data text file and interact accordingly
    def update_data(self):
        file_changed = False
        # open the plot_data file and start reading from it
        with open('plot_data.txt', 'r') as data_file:
            lines = data_file.readlines()
            new_t_min, new_t_max = lines[0].rstrip().split(',')
            new_t_interval = lines[1]
            self.change_t(float(new_t_min), float(new_t_max), float(new_t_interval))

            # Check so there is a third row and if saving to csv should be done
            if len(lines) > 2:
                if lines[2].rstrip() == 'True':
                    self.save_csv = True
                    lines[2] = 'False\n'
                    file_changed = True

            # Check if there is a fourth line and if it is true -> save plot
            if len(lines) > 3:
                if lines[3].rstrip() == 'True':
                    self.save_plot = True
                    lines[3] = 'False\n'
                    file_changed = True

            # Check if a title for the plot should be set
            if len(lines) > 4:
                if len(lines[4].rstrip()) > 0 and self.plt_title != lines[4].rstrip():
                    self.set_title = True
                    self.plt_title = lines[4].rstrip()

            # Check if the x_label should be set
            if len(lines) > 5:
                if len(lines[5].rstrip()) > 0 and self.plt_x_label != lines[5].rstrip():
                    self.set_x_label = True
                    self.plt_x_label = lines[5].rstrip()

            # Check if the y_label should be set
            if len(lines) > 6:
                if len(lines[6].rstrip()) > 0 and self.set_y_label != lines[6].rstrip():
                    self.set_y_label = True
                    self.plt_y_label = lines[6].rstrip()

        # If the content of file has been changed the new changes should be written to
        if file_changed:
            with open('plot_data.txt', 'w') as data_file:
                data_file.writelines(lines)

    # Argument i is the value of the animation iteration variable
    def save_to_csv(self, i):
        with open('graph_data{}'.format(i), 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for i, val in enumerate(self.t):
                row = [val, self.h[i]]
                writer.writerow(row)

    # The callback function for matplotlib.animate.FuncAnimation
    def animate(self, i):
        self.update_data()
        self.plot()

        # Check to change attributes of plot according to plot_data file
        if self.save_csv:
            self.save_csv = False
            self.save_to_csv(i)
        if self.save_plot:
            self.save_plot = False
            self.fig.savefig('plot{}.png'.format(i))
        if self.set_title:
            self.ax.set(title=self.plt_title)
        if self.set_x_label:
            self.ax.set(xlabel=self.plt_x_label)
        if self.set_y_label:
            self.ax.set(ylabel=self.plt_y_label)

    def calc_h(self, l):
        return 3 * math.pi * math.exp(-l)

    def calc_lambda(self, t):
        return 5 * math.sin(2 * math.pi * t)

    # Plot the data, and make the plot pritty
    def plot(self):
        self.ax.clear()
        self.ax.plot(self.t, self.h)