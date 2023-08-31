import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Persegi:
    
    def __init__(self,panjang,lebar):
        self.panjang = panjang
        self.lebar = lebar
    
    def luas(self):
        return self.panjang*self.lebar
    
    def keliling(self):
        return  (2*self.panjang)+(2*self.lebar)
    
    def plot(self, color=None):
        print("plotting persegi")
        center = (0,0)
        draw = Rectangle(center,
                                 self.panjang,
                                 self.lebar,
                                 facecolor=color)
        
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.add_patch(draw)
        ax.set_xlim(-(self.panjang*0.2),max(self.lebar+(self.lebar*0.2),self.panjang+(self.panjang*0.2)))
        ax.set_ylim(-(self.lebar*0.2),max(self.lebar+(self.lebar*0.2),self.panjang+(self.panjang*0.2)))
        # plt.autoscale(enable=True, axis='both')
        plt.show()
        
        return fig
        
        
    