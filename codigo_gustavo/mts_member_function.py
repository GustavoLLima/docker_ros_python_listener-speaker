import socket
import sys
import json

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from types import SimpleNamespace

msg_to_send = ""

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        # x = json.loads(msg.data, object_hook=lambda d: SimpleNamespace(**d))
        print(x.id, x.action)

        global msg_to_send
        msg_to_send = msg.data


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic2', 10)
        while True:
            self.timer_callback()

    def timer_callback(self):

        test_string = my_hostname
        my_id = int(''.join(filter(lambda i: i.isdigit(), test_string)))
        # print (str(my_id))

        #position = random.randint(0,100)

        #m = {"id": my_id, "position": position} # a real dict.
        command = json.loads(msg_to_send, object_hook=lambda d: SimpleNamespace(**d))
        #command = json.dumps(m)

        msg = String()
        msg.data = msg_to_send
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()