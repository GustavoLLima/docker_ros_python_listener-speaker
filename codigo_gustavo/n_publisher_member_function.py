from time import sleep

import rclpy

from std_msgs.msg import String

import json

import random

import os
my_hostname = (os.environ['my_hostname'])

def main(args=None):
  rclpy.init(args=args)

  node = rclpy.create_node('minimal_publisher')

  publisher = node.create_publisher(String, 'topic', 10)

  #msg = String()
  #senden = true
  i = 0
  while rclpy.ok():
    #msg.data = 'Hello World: %d' % i
    if (i < 1):
        test_string = my_hostname
        my_id = int(''.join(filter(lambda i: i.isdigit(), test_string)))
        # print (str(my_id))

        position = random.randint(0,100)

        m = {"id": my_id, "position": position} # a real dict.
        command = json.dumps(m)

        msg = String()
        msg.data = command

        print (msg.data)
        node.get_logger().info('Publishing: "%s"' % msg.data)
        publisher.publish(msg)
        i += 1
    sleep(0.5)  # seconds

  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  node.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()




# from time import sleep

# import rclpy

# from std_msgs.msg import String



# def main(args=None):
#   rclpy.init(args=args)

#   node = rclpy.create_node('minimal_publisher')

#   publisher = node.create_publisher(String, 'topic', 10)

#   msg = String()
#   senden = true
#   i = 0
#   while rclpy.ok():
#     msg.data = 'Hello World: %d' % i
#     i += 1
#     #node.get_logger().info('Publishing: "%s"' % msg.data)
#     If send:
#         publisher.publish(msg)
#         Send= false
#     sleep(0.5)  # seconds

# # Destroy the node explicitly
# # (optional - otherwise it will be done automatically
# # when the garbage collector destroys the node object)
# node.destroy_node()
# rclpy.shutdown()


# if __name__ == '__main__':
#   main()
