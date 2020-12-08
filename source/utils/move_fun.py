#!/usr/bin/env python
# encoding: utf-8
""" 单点导航
"""

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math
from geometry_msgs.msg import PointStamped, PoseStamped
import actionlib
from move_base_msgs.msg import *
import time


def move_to_point(goal_pub, point_x, point_y):           #移动到一个点
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = point_x
    pose.pose.position.y = point_y
    pose.pose.orientation.w = 1
    goal_pub.publish(pose)


def send_mark(point_x=1.51060724258, point_y=0.143926501274):
    global goal_pub
    rospy.init_node('path_point_demo')
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 1)
    time.sleep(2)
    move_to_point(point_x, point_y)

if __name__ == "__main__":
    send_mark()