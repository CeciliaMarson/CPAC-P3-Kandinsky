import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

class MplColorHelper:

    def __init__(self, map_name, start_val, end_val):
        self.map_name = map_name
        self.cmap = plt.get_cmap(map_name)
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=end_val)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)
