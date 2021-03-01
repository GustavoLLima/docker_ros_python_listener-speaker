from time import sleep

import rclpy

from std_msgs.msg import String



def main(args=None):
  rclpy.init(args=args)

  node = rclpy.create_node('minimal_publisher')

  publisher = node.create_publisher(String, 'topic', 10)

  msg = String()
  senden = true
  i = 3
  while rclpy.ok():
    msg.data = 'Hello World: %d' % i
    #node.get_logger().info('Publishing: "%s"' % msg.data)
    if (i > 3):
        publisher.publish(msg)
        i += 1
    sleep(0.5)  # seconds

# Destroy the node explicitly
# (optional - otherwise it will be done automatically
# when the garbage collector destroys the node object)
#node.destroy_node()
rclpy.shutdown()


if __name__ == '__main__':
  main()
