#!/usr/bin/env python

# Simple example of a subscriber that does "work" in the callback, this exhibits
# the importance of setting the queue_size for the subscriber (as well as the
# publisher).


import rospy
from std_msgs.msg import Int32
import time


def callback(data):
    # Here is a callback that sleeps for a while, simulating a callback that
    # does a lot of work.
    rospy.loginfo('Received data: {}'.format(data))
    time.sleep(0.1)


def run():
    rospy.init_node('delayed_publisher')
    pub = rospy.Publisher('/topic', Int32, queue_size=100)

    # NOTE: a specified queue size 1 allows dropping of messages so the
    # callbacks aren't queued up infinitely. Default value is queue_size=None,
    # which means keep all messages.
    sub = rospy.Subscriber('/topic', Int32, callback=callback, queue_size=5)

    # Publish a bunch of messages
    for idx in range(100):
        msg = Int32(idx)
        pub.publish(msg)
        rospy.loginfo('Published message: {}'.format(msg))
        rospy.sleep(0.01)

    # Wait a while longer, when queue size is > 1 any remaining messages in the
    # queue get processed.
    rospy.sleep(1.0)

if __name__ == '__main__':
    run()
