import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from Plot import Scope

if __name__ == '__main__':
    # style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    scope = Scope(ax1, fig)
    ani = animation.FuncAnimation(fig, scope.animate, interval=1000)
    plt.show()

