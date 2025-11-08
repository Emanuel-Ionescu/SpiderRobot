import time
import matplotlib.pyplot as plt
import numpy as np

from math import sin, cos, pi

from sequence import *

Body = {
    "x" : np.array([-0.5, 0.5]),"y" : np.array([-0.5, 0.5]),"z" : np.array([0, 0])
}

Leg1 = [np.array([-0.5, -0.5, 0]), np.array([-1, -1, 0]), np.array([-1.5, -1.5, 0])]
Leg2 = [np.array([ 0.5, -0.5, 0]), np.array([ 1, -1, 0]), np.array([ 1.5, -1.5, 0])]
Leg3 = [np.array([-0.5,  0.5, 0]), np.array([-1,  1, 0]), np.array([-1.5,  1.5, 0])]
Leg4 = [np.array([ 0.5,  0.5, 0]), np.array([ 1,  1, 0]), np.array([ 1.5,  1.5, 0])]

def rotateX(vec : np.ndarray, angle : float):
    angle = angle/360 * pi
    mat = np.array(
        [
            [1,               0,                0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle),  cos(angle)]
        ]
    )

    return np.dot(mat, vec.T).T

def rotateY(vec : np.ndarray, angle : float):
    angle = angle/360 * pi
    mat = np.array(
        [
            [ cos(angle), 0, sin(angle)],
            [ 0,               1,               0],
            [-sin(angle), 0, cos(angle)]
        ]
    )
    return np.dot(mat, vec.T).T

def rotateZ(vec : np.ndarray, angle : float):
    angle = angle/360 * pi
    mat = np.array(
        [
            [cos(angle), -sin(angle), 0],
            [sin(angle),  cos(angle), 0],
            [0,                0,               1]
        ]
    )
    return np.dot(mat, vec.T).T


def main():

    Legs = [Leg1, Leg2, Leg3, Leg4]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    

    current_sequence = WalkForwardSequence

    #
    # Plot legs dynamicaly
    #
    while True:

        ax.clear()

        ax.plot([-2,  2], [-2, -2], [-2, -2], "w")
        ax.plot([-2, -2], [ 2, -2], [-2, -2], "w")
        ax.plot([-2, -2], [-2, -2], [-2,  2], "w")


        #
        # Plot body only once
        #
        for y in np.arange(*Body["y"], 0.01):
            ax.plot(Body["x"], [y, y], Body["z"], "k")

        step = current_sequence.getStep()

        if type(step) == Delay:
            time.sleep(step.description)
        else: 
            # computing each leg points 
            for leg, id in zip(Legs, ["L1", "L2", "L3", "L4"]):
                if id in step.description.keys():

                    full_json = {"1" : 0, "2" : 0, "3" : 0}
                    for key, val in step.description.items():
                        full_json[key] = val

                    # efective computing
                    aux = leg[2] - leg[1]

                    leg[0] = leg[0]
                    leg[1] = leg[0] + rotateZ((leg[1] - leg[0]), 10)
                    leg[2] = leg[1] + rotateZ(aux, 10) 

                    leg[2] = leg[1] + rotateY((leg[2] - leg[1]), 10)

        # plotting the legs
        for leg in Legs:
            ax.plot([leg[0][0], leg[1][0]], [leg[0][1], leg[1][1]], [leg[0][2], leg[1][2]])
            ax.plot([leg[1][0], leg[2][0]], [leg[1][1], leg[2][1]], [leg[1][2], leg[2][2]])
        plt.pause(0.1)

if __name__ == "__main__":
    main()