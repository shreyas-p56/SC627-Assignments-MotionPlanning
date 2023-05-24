#!/usr/bin/env python2.7
import rospy
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import matplotlib.pyplot as plt

# Define the callback function for each turtlebot odometry topic
def callback_odom_tb(data, tb_index):
    global agent_state
    agent_state[tb_index][0] = data.pose.pose.position.x
    agent_state[tb_index][1] = data.pose.pose.position.y
    quaternion = (data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    agent_state[tb_index][2] = euler[2]

# Define a function to publish Twist messages for a given turtlebot
def publish_cmd_vel(tb_index, linear_vel, angular_vel):
    twist = Twist()
    twist.linear.x = linear_vel
    twist.angular.z = angular_vel
    pub_rate = rospy.Rate(20)
    #for j in range(10):
    if tb_index == 0:
        pub_tb1.publish(twist)
    elif tb_index == 1:
        pub_tb2.publish(twist)
    elif tb_index == 2:
        pub_tb3.publish(twist)
    elif tb_index == 3:
        pub_tb4.publish(twist)
        #pub_rate.sleep()

# Initialize global variable agent_state for all turtlebots
agent_state = [[0, 0, 0] for i in range(4)]


# Initialize the ROS node for each turtlebot
rospy.init_node("turtlebot_controller")

# Subscribe to the odometry topic for each turtlebot and specify the corresponding callback function
rospy.Subscriber("/tb3_6/odom", Odometry, callback_odom_tb, 0)
rospy.Subscriber("/tb3_5/odom", Odometry, callback_odom_tb, 1)
rospy.Subscriber("/tb3_4/odom", Odometry, callback_odom_tb, 2)
rospy.Subscriber("/tb3_0/odom", Odometry, callback_odom_tb, 3)

# Create a publisher for the cmd_vel topic for each turtlebot
pub_tb1 = rospy.Publisher("/tb3_6/cmd_vel", Twist, queue_size=10)
pub_tb2 = rospy.Publisher("/tb3_5/cmd_vel", Twist, queue_size=10)
pub_tb3 = rospy.Publisher("/tb3_4/cmd_vel", Twist, queue_size=10)
pub_tb4 = rospy.Publisher("/tb3_0/cmd_vel", Twist, queue_size=10)

# Set the rate at which to publish Twist messages
rate = rospy.Rate(20)

omega = 0
velocity = 0.2
K = -10
COM_posx, COM_posy, mlst = [], [], []

fig = plt.figure()

for m in range(3000):
    print(m)
    for i in range(4):
        ang_vel=0 + omega
        for j in range(4):
            ang_vel=ang_vel+ ((-K/4)*(math.sin(agent_state[j][2]- agent_state[i][2])))
        publish_cmd_vel(i, velocity, ang_vel)

    mlst.append(m)
    COM_posx.append((agent_state[0][0]+agent_state[1][0]+agent_state[2][0]+agent_state[3][0])/4)
    COM_posy.append((agent_state[0][1]+agent_state[1][1]+agent_state[2][1]+agent_state[3][1])/4)
    rate.sleep()

for i in range(4):
    linear_vel = 0
    angular_vel = 0 
    publish_cmd_vel(i, linear_vel, angular_vel)

plt.plot(mlst,COM_posx,label='COM X position')
plt.plot(mlst,COM_posy,label='COM Y position')
plt.legend()
plt.show()
