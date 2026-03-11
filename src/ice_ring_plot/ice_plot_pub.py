
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
import matplotlib.patches as mpatches
import os
import math


"""
Setup Default Values
"""
AXISSPACE = (0.09, 0.12)
EXTRAPADDING = (0.15,0.01)
FIG_SIZE = (10, 5)
DEFAULT_EXTENSIONS = ['pdf'] # ['pdf', 'png'] 

# ICE PARAMETERS
ICE_RING_DIM = (200, 85) # Feet
CORNER_RADIUS = 28 # Feet
GOAL_LINE = 11 # Feet from the end boards
BLUE_LINE = 25 # Feet from the centre line
FACE_OFF_OFFSET = (69, 22) # Feet
FACE_OFF_RADIUS = 15 # Feet
C_FACE_OFF_OFFSET = (20, 22) # Feet
GOAL_CREASE_RADIUS = 6 # Feet
GOAL_LINE = 11 # Feet

SHOT_ARROW_LENGTH = 20 # Feet

TICKS_INTERVAL = 20 # Feet
BORDER_PADDING = 1 # Feet


class Ice_Plot_Pub():
    """ 
    Default Ice Ring Plot Publisher
    """
    def __init__(self, dir, filename, axisSpace=AXISSPACE, 
                 extrapadding=EXTRAPADDING, exts=DEFAULT_EXTENSIONS):
        self.dir = dir
        self.filename = filename
        self.axisSpace = axisSpace
        self.extrapadding = extrapadding 
        self.create_fig(axisSpace, extrapadding)
        self.exts = exts
        self.handles = []
        self.labels = []

    def create_fig(self,axisSpace=AXISSPACE, extrapadding=EXTRAPADDING):
        """
        Generate Figure
        """
        self.fig = plt.figure(figsize=FIG_SIZE)
        self.ax = self.fig.add_axes([axisSpace[0], axisSpace[1], 1.-axisSpace[0]-.001-extrapadding[0], 1.-axisSpace[1]-.001-extrapadding[1]])

        # Specific to Ice Rings
        self.ax.set_xlim(-ICE_RING_DIM[0]/2-BORDER_PADDING, 
                         ICE_RING_DIM[0]/2+BORDER_PADDING)
        self.ax.set_ylim(-ICE_RING_DIM[1]/2-BORDER_PADDING, 
                         ICE_RING_DIM[1]/2+BORDER_PADDING)
        self.ax.set_aspect('equal')
        # Set ticks interval
        self.ax.xaxis.set_major_locator(MultipleLocator(TICKS_INTERVAL))
        self.ax.yaxis.set_major_locator(MultipleLocator(TICKS_INTERVAL))

        # Add Ice Ring
        self.ice_box = FancyBboxPatch(
            (-ICE_RING_DIM[0]/2, -ICE_RING_DIM[1]/2), # bottom-left corner (x, y)
            width=ICE_RING_DIM[0],     
            height=ICE_RING_DIM[1],       
            boxstyle="round,pad=0.1,rounding_size=%f"%(CORNER_RADIUS),  # rounded corners
            linewidth=2,
            edgecolor='black',
            facecolor='none',
            zorder=10
        )
        self.ax.add_patch(self.ice_box)
        self.ax.plot(0,0, 'o', color='red', markersize=5) 

        # Center Line
        self.ax.plot([0, 0], 
                             [-ICE_RING_DIM[1]/2, ICE_RING_DIM[1]/2], 
                             color='red', linewidth=2, zorder=3)      
        
        # Center ice circle
        circle = Circle(
            (0, 0),    
            radius=FACE_OFF_RADIUS,
            edgecolor='blue',
            facecolor='none',
            linewidth=2,
            zorder=2 
        )
        self.ax.add_patch(circle)

        # Face-off circles
        face_off_cir = [(FACE_OFF_OFFSET[0],FACE_OFF_OFFSET[1]),
                        (-FACE_OFF_OFFSET[0],FACE_OFF_OFFSET[1]),
                        (FACE_OFF_OFFSET[0],-FACE_OFF_OFFSET[1]),
                        (-FACE_OFF_OFFSET[0],-FACE_OFF_OFFSET[1]),]
        for p in face_off_cir:
            circle = Circle(
                p,    
                radius=FACE_OFF_RADIUS,
                edgecolor='blue',
                facecolor='none',
                linewidth=2,
                zorder=2 
            )
            self.ax.add_patch(circle)
            self.ax.plot(*p, 'o', color='red', markersize=5) 

        # Center Face-off points
        face_off_cir = [(C_FACE_OFF_OFFSET[0],C_FACE_OFF_OFFSET[1]),
                        (-C_FACE_OFF_OFFSET[0],C_FACE_OFF_OFFSET[1]),
                        (C_FACE_OFF_OFFSET[0],-C_FACE_OFF_OFFSET[1]),
                        (-C_FACE_OFF_OFFSET[0],-C_FACE_OFF_OFFSET[1]),]
        for p in face_off_cir:
            self.ax.plot(*p, 'o', color='red', markersize=5) 

        # Blue Lines
        x = BLUE_LINE
        y = ICE_RING_DIM[1]/2
        self.ax.plot([-x, -x], [-y, y], 
                        color='blue', linewidth=2, zorder=3)
        self.ax.plot([x, x], [-y, y], 
                        color='blue', linewidth=2, zorder=3)
                        
        # Goal Line
        x = ICE_RING_DIM[0]/2-GOAL_LINE
        y = ICE_RING_DIM[1]/2
        line, = self.ax.plot([-x, -x], [-y, y], 
                        color='red', linewidth=2, zorder=3)
        line.set_clip_path(self.ice_box) 
        line, = self.ax.plot([x, x], [-y, y], 
                        color='red', linewidth=2, zorder=3)
        line.set_clip_path(self.ice_box) 

        # Goal Crease
        x = ICE_RING_DIM[0]/2-GOAL_LINE
        wedge = Wedge(center=(-x,0), 
                        r=GOAL_CREASE_RADIUS, 
                        theta1=-90, theta2=90,
                        facecolor='lightblue', edgecolor='red', 
                        linewidth=2) 
        self.ax.add_patch(wedge)
        wedge = Wedge(center=(x,0), 
                        r=GOAL_CREASE_RADIUS, 
                        theta1=90, theta2=-90,
                        facecolor='lightblue', edgecolor='red', 
                        linewidth=2) 
        self.ax.add_patch(wedge)

    def add_players(self, ps, markers='x', color='green',  label='', **kwargs):
        '''  
        ps: Array of tuple positions (x,y)
        '''
        x, y = zip(*ps)
        p = self.ax.plot(x,y, markers, color=color, zorder=50, **kwargs)

        self.handles.append(p[0]) 
        self.labels.append(label)

    def add_shot(self, p, dir, stype='o', color='green', label='', **kwargs):
        '''  
        p: Shot position (x,y)
        dir: Direction Vector (x,y)
        '''
        self.ax.plot(*p, stype, color=color, markersize=5, zorder=40)
        dir = list(dir)
        dir =[x / math.sqrt(sum(x**2 for x in dir)) *SHOT_ARROW_LENGTH for x in dir]
        p = self.ax.arrow(*p, *dir, head_width=5, head_length=5, 
                      linewidth=1,
                      fc=color, ec=color, zorder=40,
                      **kwargs)
        
        self.handles.append(p) 
        self.labels.append(label)
        
    def add_zone(self,x,y,z, hatches, levels, labels, **kwargs):
        #c = self.ax.contour(x, y, z, n_levels, colors='black', linestyles='-')
        cs = self.ax.contourf(x, y, z, levels, colors='none', extend='both',
                            hatches=hatches, labels = labels, **kwargs) 
        
        # Clip Contours
        #c.set_clip_path(self.ice_box)   
        cs.set_clip_path(self.ice_box) 
   

        # Create legend handles and labels
        if labels is not None:
            for i, level in enumerate(levels):
                label = labels[level]
                if label is None: continue
                p = mpatches.Patch(
                    facecolor='none',
                    hatch=hatches[i] if hatches is not None else '',
                    edgecolor='black'
                )
                self.handles.append(p)
                self.labels.append(label)
            

    def plot(self,x,y, color=None, label=None, marker=None, markersize=None, 
             linestyle = "solid"):
        """
        Plot Standard Line
        """
        p = self.ax.plot(x, y, color=color,label=label, marker=marker, 
                         linestyle=linestyle, markersize=markersize)
        self.handles.append(p)
        self.labels.append(label)
    
    def setup_ax(self, xlabel, ylabel):
        self.ax.set(xlabel = xlabel, ylabel=ylabel)

    def loadLegend(self):
        legendKwargs = {'frameon' : True,
                        'labelcolor' : 'black', 
                        'facecolor' : 'white', 
                        'edgecolor':'black',
                        'framealpha': 0.8,  # 1.0
                        'labelspacing' : 0.1,
                        'handlelength' : 2, #0.5
                        'columnspacing' : 0.5,
                        'handletextpad' : 0.4,
                        'borderpad' : 0.2,
                        'fontsize' : 'small',
                        #'loc' : 'outside upper left',
                        'loc' : 'lower left',
                        'bbox_to_anchor' : (0., 1.02), #, 1., .102
                        'borderaxespad': 0.,
                        'ncol' : 2,
                    }
        if len(self.labels) != 0: self.ax.legend(self.handles, self.labels, 
                                                 **legendKwargs)

    def release_files(self):
        for ext in self.exts:
            self.fig.savefig(os.path.join(self.dir, self.filename+"."+ext), 
                             format=ext )

    def show(self):
        self.loadLegend()
        self.fig.show()

    def close_window(self):
        plt.close(self.fig)
    
    def setTitle(self,title):
        self.ax.set_title(title)
