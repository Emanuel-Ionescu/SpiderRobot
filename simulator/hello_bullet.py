import pybullet as p
import time
import pybullet_data
import math

from utils import ServerThread

server_thread = ServerThread()
server_thread.start()

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, 0)
#planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0, 0, 0]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
robotID = p.loadURDF("SpiderRobot.urdf", cubeStartPos, cubeStartOrientation,
                     flags=p.URDF_USE_INERTIA_FROM_FILE, useFixedBase=True)


revolute_joints = []
for i in range( p.getNumJoints(robotID)):
    jointInfo = p.getJointInfo(robotID, i)
    jointType = jointInfo[2]
    
    if jointType == p.JOINT_REVOLUTE:
        revolute_joints.append(i)

joint_angles = [0.0] * len(revolute_joints) 

while True:

    data = server_thread.get_element()
    if data is not None:
        joint_angles = [round(float(x), 1) for x in data.split(':')]
        print(f"Received angles: {joint_angles}")
        
        # angle prelucration
        joint_angles[-2] *= -1

        # 0 1 2 | 3 4 5 | 6 7 8 | 9 10 11
        for idx in [2, 5, 8, 11]:
            joint_angles[idx] *= -1

        for i in range(12):
            p.setJointMotorControl2(robotID, i, p.POSITION_CONTROL, targetPosition=math.radians(joint_angles[i]))
    
    p.stepSimulation()
    time.sleep(1./240.)

cubePos, cubeOrn = p.getBasePositionAndOrientation(robotID)
print(cubePos, cubeOrn)

