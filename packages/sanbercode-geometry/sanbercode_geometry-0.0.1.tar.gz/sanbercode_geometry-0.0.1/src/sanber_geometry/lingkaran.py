import numpy as np
import matplotlib.pyplot as plt

class Lingkaran:
    pi = np.pi
    
    def __init__(self,radius):
        self.radius = radius
    
    def luas(self):
        return self.pi*self.radius**2
    
    def keliling(self):
        return  2*self.pi*self.radius
    
    def plot(self, color="False"):
        print("plotting lingkaran")
        center = (0,0)
        draw = plt.Circle(center,
                                 self.radius,
                                 color=color)
        
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.add_patch(draw)
        ax.set_xlim(-self.radius-(self.radius*0.2),self.radius+(self.radius*0.2))
        ax.set_ylim(-self.radius-(self.radius*0.2),self.radius+(self.radius*0.2))
        # plt.autoscale(enable=True, axis='both')
        plt.show()
        
        return fig
        
        
    