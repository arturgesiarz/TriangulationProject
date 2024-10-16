
import matplotlib.pyplot as plt
import matplotlib
import pickle

matplotlib.use('macosx')


class PointSelector:
    def __init__(self,OXRange=(0,10),OYRange=(0,10)):

        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Polygons select')

        self.ax.set_xlim(OXRange[0], OXRange[1])
        self.ax.set_ylim(OYRange[0], OYRange[1])

        self.points = []
        self.current_polygon = []

        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.button == 1:
            self.points.append((event.xdata, event.ydata))
            self.current_polygon.append((event.xdata, event.ydata))
            self.ax.plot(event.xdata, event.ydata, 'co')
            self.fig.canvas.draw()
        elif event.button == 3: plt.close()

def render(max_heigh = 20):

    objectCreated = PointSelector((0,max_heigh),(0,max_heigh))
    plt.title("Point selector - Please insert your points :)")
    plt.grid()
    plt.show(block=True)
    plt.close('all')
    return objectCreated.points

def start():
    pointSelects = render(10)

    with open('points.pkl', 'wb') as file:
        pickle.dump(pointSelects, file)

    return pointSelects

if __name__ == '__main__':
    print(start())

    poly = [[(1.9556451612903225, 1.9805194805194808), (8.024193548387096, 1.9264069264069263), (7.993951612903226, 8.000541125541126), (6.512096774193548, 4.889069264069264), (5.191532258064516, 3.2521645021645025), (3.1048387096774195, 2.3051948051948052)]]




