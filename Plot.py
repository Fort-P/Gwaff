# Import
import matplotlib.pyplot as plt

class Plot:
    def __init__(self, data, dates, title, ylbl, xlbl, start=None, end=None):
        self.data = data
        self.dates = dates
        ticks = [x for x in self.dates if str(x).endswith('12')]
        self.start = start
        self.end = end
        
        plt.style.use('fivethirtyeight')
        self.fig, self.ax = plt.subplots()
        self.ax.set(title=title, ylabel=ylbl, xlabel=xlbl, xticks=[])
        plt.subplots_adjust(right=0.82)
        
        self.annotations = []
        
    def draw(self):
        for row in self.data:
            self.ax.plot(self.dates, row[3:(len(row))], linewidth=2.0, color=row[1])
            self.annotations.append([row[-1], row[0], row[2], row[1]])    # Add a list containing [total xp, name, icon, color] to the list annotations

    def annotate(self):
        heights = [100]
        for index, item in enumerate(sorted(self.annotations, key=lambda x: x[0])):
            height = item[0]
            if height - heights[-1] <= 100:
                height = heights[-1] + 100
            heights.append(height)
#             self.ax.annotate(getimg(item[2]), )
            self.ax.annotate(item[1], (0.98, height), xycoords=('axes fraction', 'data'), color=item[3], va='center', size='small')
            self.annotate_image()

    def annotate_image(self):
        pass

    def show(self):
        plt.show()