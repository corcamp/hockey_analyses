import numpy as np
import os
from ice_plot_pub import Ice_Plot_Pub

# Define the Plot Publisher
ice_pub = Ice_Plot_Pub(os.path.dirname(os.path.abspath(__file__)), 
                    'IcePlotExemple')

# -----------------------------------
# Add Players on Ice
player_pos = [  (9,23),
                (45,20),
                (45,-10),
                (9,-18),
                (-1,-18)]
ice_pub.add_players(player_pos, color='green', label='Players', 
                    markers = 'x', markersize = 10)

# -----------------------------------
# Add Shot
ice_pub.add_shot(p =  (45,-10), dir = (-30,-10), color='orange', 
                 label='Player Shot')

# -----------------------------------
# Add Zones
rows, cols = 85, 200
y, x = np.meshgrid(np.arange(rows,dtype=float),
                   np.arange(cols,dtype=float),indexing="ij" )
x-=200/2
y-=85/2
z = np.zeros((rows, cols), dtype=int)
# Create rectangular region of 1 values
bot_left = (20, 20)   
height, width = 40, 25
z[ bot_left[0]:bot_left[0] + height,
        bot_left[1]:bot_left[1] + width ] = 1
# Create rectangular region of 2 values
bot_left = (60, 110)   
height, width = 40, 25
z[ bot_left[0]:bot_left[0] + height,
        bot_left[1]:bot_left[1] + width ] = 2

labels = {
    0: None,
    1: "Difficulty Scores",
    2: "Easy Scores"
}
ice_pub.add_zone(x, y, z, hatches=[None, '.', '..'], 
                levels=[0, 1, 2], color='black', 
                labels = labels)

# -----------------------------------
# Add Axis Labels
ice_pub.setup_ax('Tracking x [Feet]','Tracking y [Feet]')

# -----------------------------------
# Publish
ice_pub.show()
ice_pub.release_files()

temp = 1