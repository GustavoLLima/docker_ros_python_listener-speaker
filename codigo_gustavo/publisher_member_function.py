import socket
import sys
import json
from random import randrange
from time import time, sleep

from types import SimpleNamespace


import rclpy
import random
from rclpy.node import Node

from std_msgs.msg import String

msg_to_send = ""


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 10  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        # if (random.randint(1,10) >= 5):
        #   msg.data = '1'
        # else:
        #   msg.data = '0'
        msg.data = msg_to_send
        
        #msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("talker", 9999))
    s.listen(2)

    while True:
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind(("python_server", 9999))
        # s.listen(2)
        conn, addr = s.accept()
        print("Conexão estabelecida com %s" % str(addr))
        received_message = bytes.decode(conn.recv(1024))
        print ("Mensagem recebida:")
        print(received_message)
        global msg_to_send
        msg_to_send = "received_message"

        #x = json.loads(received_message, object_hook=lambda d: SimpleNamespace(**d))
        #print(x.id, x.action)

        # m = {"id": int(received_message), "action": "stop"} # a real dict.
        # command = json.dumps(m)

        #command = "dsadsasdasadsda"
        #print ("Enviando para o cliente:"+command)

        #conn.sendall(command.encode('ascii'))



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



# import rclpy
# import random
# from rclpy.node import Node

# from std_msgs.msg import String


# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'topic', 10)
#         timer_period = 0.5  # seconds
#         self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.i = 0

#     def timer_callback(self):
#         msg = String()
#         if (random.randint(1,10) >= 5):
#           msg.data = '1'
#         else:
#           msg.data = '0'
        
#         #msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         self.i += 1


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_publisher = MinimalPublisher()

#     rclpy.spin(minimal_publisher)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

# # Copyright 2016 Open Source Robotics Foundation, Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String


# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'chatter', 10)
#         timer_period = 0.5  # seconds
#         self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.i = 0

#     def timer_callback(self):
#         msg = String()
#         msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         self.i += 1


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_publisher = MinimalPublisher()

#     rclpy.spin(minimal_publisher)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
