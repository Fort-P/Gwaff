# Import
import matplotlib.pyplot as plt

class Plot:
    def __init__(self, data, dates, title, ylbl, xlbl, start=None, end=None):
        self.data = data
        self.dates = dates
        ticks = [i for i, item in enumerate(self.dates) if i % 24 == 0]
        self.start = start
        self.end = end
        
        plt.style.use('fivethirtyeight')
        self.fig, self.ax = plt.subplots()
        self.ax.set(title=title, ylabel=ylbl, xlabel=xlbl, xticks=ticks)
        plt.subplots_adjust(right=0.82, bottom=0.17)
        
        self.annotations = []
        
    def draw(self):
        for row in self.data:
            if row[1] == "NOT IN SERVER":
                row[1] = "000000"
            self.ax.plot(self.dates, row[3:(len(row))], linewidth=2.0, color=row[1])
            self.annotations.append([row[-1], row[0], row[2], row[1]])    # Add a list containing [total xp, name, icon, color] to the list annotations
        plt.xticks(rotation=70)

    def annotate(self):
        heights = [350]
        for index, item in enumerate(sorted(self.annotations, key=lambda x: x[0])):
            height = item[0]
            if height - heights[-1] <= 350:
                height = heights[-1] + 350
            heights.append(height)
#             self.ax.annotate(getimg(item[2]), )
            self.ax.annotate(item[1], (0.98, height), xycoords=('axes fraction', 'data'), color=item[3], va='center', size='small')
            self.annotate_image()

    def annotate_image(self):
        pass

    def show(self):
        plt.show()
    
    def save(self, name):
        self.fig.savefig(name, bbox_inches='tight')