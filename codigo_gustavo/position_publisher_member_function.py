import socket
import sys
import json
#from random import randrange
#from time import time, sleep

from types import SimpleNamespace

import os
my_hostname = os.environ['my_hostname']

import rclpy
import random
from rclpy.node import Node

from std_msgs.msg import String

msg_to_send = ""


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        while True:
            self.timer_callback()


        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind((my_hostname, 9999))
        # s.listen(2)

        # while True:
        #     conn, addr = s.accept()
        #     print("Conexão estabelecida com %s" % str(addr))
        #     received_message = bytes.decode(conn.recv(1024))
        #     print ("Mensagem recebida:")
        #     print(received_message)
        #     global msg_to_send
        #     msg_to_send = received_message
        #     self.timer_callback()

    def timer_callback(self):
        # msg = String()
        # msg.data = msg_to_send
        # self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)

        test_string = my_hostname
        my_id = int(''.join(filter(lambda i: i.isdigit(), test_string)))
        # print (str(my_id))

        position = random.randint(0,100)

        m = {"id": my_id, "position": position} # a real dict.
        command = json.dumps(m)

        msg = String()
        msg.data = command
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    #Código ROS
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
