#!/usr/bin/env python
# encoding: utf-8
""" 单点导航
"""

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math
from geometry_msgs.msg import PointStamped, PoseStamped, Quaternion
from tf.transformations import quaternion_from_euler
import actionlib
from move_base_msgs.msg import *
import time
import argparse
from math import pi


def move_to_point(point_x, point_y, force_w):           #移动到一个点
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = point_x
    pose.pose.position.y = point_y

    # 角度
    quaternions = [(0, 1), (1, 0), (0.707, 0.707), (0.707, -0.707)]
    z,w = quaternions[force_w]
    pose.pose.orientation.z = z
    pose.pose.orientation.w = w
    goal_pub.publish(pose)


def send_mark(point_x, point_y, force_w):
    global goal_pub
    rospy.init_node('path_point_demo')
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 1)
    time.sleep(2)
    move_to_point(point_x, point_y, force_w)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ros Balance Wheel Server")
    parser.add_argument("-x", "--pointx", type=float, help="小车移动的目的地 X 坐标轴")
    parser.add_argument("-y", "--pointy", type=float, help="小车移动的目的地 Y 坐标轴")
    parser.add_argument("-r", "--orientation", type=int, default=1, help="小车停止朝向")

    args = parser.parse_args()
    send_mark(args.pointx, args.pointy, args.orientation)