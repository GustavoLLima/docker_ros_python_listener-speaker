from time import sleep

import rclpy

from std_msgs.msg import String

import json

def main(args=None):
  rclpy.init(args=args)

  node = rclpy.create_node('minimal_publisher')

  publisher = node.create_publisher(String, 'topic', 10)

  #msg = String()
  #senden = true
  i = 3
  while rclpy.ok():
    #msg.data = 'Hello World: %d' % i
    if (i > 3):
        m = {"id": 1, "position": 10}
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
