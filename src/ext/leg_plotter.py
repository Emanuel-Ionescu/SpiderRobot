import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def plot_base(length, width, color):
    OFFSET_Y, OFFSET_X = width/2, length/2

    ax.plot([-OFFSET_X,  OFFSET_X], [ OFFSET_Y,  OFFSET_Y], color=color)
    ax.plot([-OFFSET_X,  OFFSET_X], [-OFFSET_Y, -OFFSET_Y], color=color)
    ax.plot([ OFFSET_X,  OFFSET_X], [-OFFSET_Y,  OFFSET_Y], color=color)
    ax.plot([-OFFSET_X, -OFFSET_X], [-OFFSET_Y,  OFFSET_Y], color=color)

    for i in range(20):
        ax.plot([OFFSET_X-i,  OFFSET_X-i], [-OFFSET_Y,  OFFSET_Y], color=color)
        
    
    ax.set_xlim(-130 - max(OFFSET_Y, OFFSET_X), 130 + max(OFFSET_Y, OFFSET_X))
    ax.set_ylim(-130 - max(OFFSET_Y, OFFSET_X), 130 + max(OFFSET_Y, OFFSET_X))
    ax.set_zlim(-130 - max(OFFSET_Y, OFFSET_X), 130 + max(OFFSET_Y, OFFSET_X))


    

def plot_leg(joint_positions, line_color='blue', leg_no=0):
    global ax    
    # Add a 3D subplot to the figure, where 111 stands for 1x1 grid and the first subplot

    # Extract x, y, and z coordinates of each joint from joint_positions
    # if leg_no in [1, 2]:
    #     x = [joint[0] + OFFSET_X for joint in joint_positions]
    # else:
    #     x = [joint[0] - OFFSET_X for joint in joint_positions]

    # if leg_no in [1, 3]:
    #     y = [joint[1] + OFFSET_Y for joint in joint_positions]
    # else:
    #     y = [joint[1] - OFFSET_Y for joint in joint_positions]

    x = [joint[0] for joint in joint_positions]
    y = [joint[1] for joint in joint_positions]
    z = [joint[2] for joint in joint_positions]

    # Plot the leg segments connecting the joints with markers at each joint
    ax.plot(x, y, z, marker='o', linewidth=2, markersize=8, color=line_color)

    # Calculate the midpoints of each segment (Coxa, Femur, and Tibia)
    coxa_mid = [(joint_positions[0][i] + joint_positions[1][i])/2 for i in range(3)]
    femur_mid = [(joint_positions[1][i] + joint_positions[2][i])/2 for i in range(3)]
    tibia_mid = [(joint_positions[2][i] + joint_positions[3][i])/2 for i in range(3)]

    # Add labels for each segment at their respective midpoints
    # ax.text(coxa_mid[0],  coxa_mid[1],  coxa_mid[2],  'Coxa',  fontsize=12, color=line_color)
    ax.text(femur_mid[0], femur_mid[1], femur_mid[2], str(leg_no), fontsize=12, color=line_color)
    # ax.text(tibia_mid[0], tibia_mid[1], tibia_mid[2], 'Tibia', fontsize=12, color=line_color)

    # Set labels for the x, y, and z axes
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Set the title for the plot
    ax.set_title('Spider Leg Visualization')

def spider_show(pause = 100.0):
    global ax
    plt.draw()
    a = plt.waitforbuttonpress(pause) # this will wait for indefinite time
    ax.cla()
    if a == ord('q'):
        plt.close(fig)
        return True
    return False