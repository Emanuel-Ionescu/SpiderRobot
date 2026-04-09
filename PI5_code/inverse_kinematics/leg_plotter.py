import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

COLORS = ["blue", "red", "green", "orange"]

def plot_base(length, width, color="purple"):
    OFFSET_Y, OFFSET_X = width/2, length/2

    ax.plot([-OFFSET_X,  OFFSET_X], [ OFFSET_Y,  OFFSET_Y], color=color)
    ax.plot([-OFFSET_X,  OFFSET_X], [-OFFSET_Y, -OFFSET_Y], color=color)
    ax.plot([ OFFSET_X,  OFFSET_X], [-OFFSET_Y,  OFFSET_Y], color=color)
    ax.plot([-OFFSET_X, -OFFSET_X], [-OFFSET_Y,  OFFSET_Y], color=color)

    ax.scatter(0, 0, 0, color=color, s=20)

    for i in range(20):
        ax.plot([-OFFSET_X,  OFFSET_X], [OFFSET_Y-i,  OFFSET_Y-i], color=color)
        
    
    ax.set_xlim(-130 - max(OFFSET_Y, OFFSET_X), 130 + max(OFFSET_Y, OFFSET_X))
    ax.set_ylim(-130 - max(OFFSET_Y, OFFSET_X), 130 + max(OFFSET_Y, OFFSET_X))
    ax.set_zlim(-130 - max(OFFSET_Y, OFFSET_X), 130 + max(OFFSET_Y, OFFSET_X))


CACHED_LEGS = [None, None, None, None]

def plot_leg(joint_positions, leg_no=0):
    global ax, COLORS, CACHED_LEGS    

    CACHED_LEGS[leg_no] = joint_positions

    x = [joint[0] for joint in joint_positions]
    y = [joint[1] for joint in joint_positions]
    z = [joint[2] for joint in joint_positions]

    # Plot the leg segments connecting the joints with markers at each joint
    ax.plot(x, y, z, marker='o', linewidth=2, markersize=8, color=COLORS[leg_no])
    ax.scatter(*joint_positions[-1], color='white', marker='o', s=40)
    ax.scatter(*joint_positions[-1], color='black', marker='o', s=20)

    # Draw a pink line between each end point of the legs
    if None not in CACHED_LEGS:
        for i in range(4):
            ax.plot([CACHED_LEGS[i][-1][0], joint_positions[-1][0]], [CACHED_LEGS[i][-1][1], joint_positions[-1][1]], [CACHED_LEGS[i][-1][2], joint_positions[-1][2]], color='pink', linewidth=2)

    # Calculate the midpoints of each segment (Coxa, Femur, and Tibia)
    coxa_mid = [(joint_positions[0][i] + joint_positions[1][i])/2 for i in range(3)]
    femur_mid = [(joint_positions[1][i] + joint_positions[2][i])/2 for i in range(3)]
    tibia_mid = [(joint_positions[2][i] + joint_positions[3][i])/2 for i in range(3)]

    # Add labels for each segment at their respective midpoints
    # ax.text(coxa_mid[0],  coxa_mid[1],  coxa_mid[2],  'Coxa',  fontsize=12, color=line_color)
    ax.text(femur_mid[0], femur_mid[1], femur_mid[2], str(leg_no + 1), fontsize=12, color=COLORS[leg_no])
    # ax.text(tibia_mid[0], tibia_mid[1], tibia_mid[2], 'Tibia', fontsize=12, color=line_color)

    # Set labels for the x, y, and z axes
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Set the title for the plot
    ax.set_title('Spider Leg Visualization')

def spider_show(pause = 100.0, draw = True):
    global ax
    
    # takes 2 pictures, one from default view, one from top 

    fig.canvas.flush_events()
    fig.canvas.draw()

    #move camera to default
    ax.view_init(elev=45, azim=-45)
    fig.canvas.draw()
    graph_image_normal = np.array(fig.canvas.get_renderer()._renderer)
    
    #move camera to top
    ax.view_init(elev=90, azim=0)
    fig.canvas.draw()
    graph_image_top = np.array(fig.canvas.get_renderer()._renderer)

    graph_image_normal = cv2.cvtColor(graph_image_normal, cv2.COLOR_RGB2BGR)
    graph_image_top = cv2.cvtColor(graph_image_top, cv2.COLOR_RGB2BGR)
    ax.cla()  # Clear the axis for the next frame
    return np.concatenate([graph_image_normal, graph_image_top], axis=1)