import socket
import sys
import json

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from types import SimpleNamespace


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
        # if(msg.data == "1"):
        #     self.get_logger().info('Andar, pois ouvi: "%s"' % msg.data)
        # else:
        #     self.get_logger().info('Parar, pois ouvi: "%s"' % msg.data)
        self.get_logger().info('I heard: "%s"' % msg.data)
        x = json.loads(msg.data, object_hook=lambda d: SimpleNamespace(**d))
        print(x.id, x.position)

        m = {"id": x.id, "position": position}
        command = json.dumps(m)
        print ("Enviando para o modelo:"+command)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(socket.gethostname())
        sock.connect(('modelo', 9999))
        sock.sendall(command.encode())


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
