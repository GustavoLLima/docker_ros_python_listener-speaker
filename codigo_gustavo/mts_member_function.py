import socket
import sys
import json

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from types import SimpleNamespace

import os

queue_size = int(os.environ['queue_size'])
queue = []


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
        # x = json.loads(msg.data, object_hook=lambda d: SimpleNamespace(**d))
        # #print(x.id, x.position)

        # m = {"id": x.id, "position": x.position}
        # command = json.dumps(m)
        global queue
        queue.append(msg.data)
        print ("Comando adicionado na fila:"+msg.data)
        print ("Fila após a adição: "+queue)
        #print ("Enviando para o modelo:"+command)

        print("len queue: "+str(len(queue))+" queue_size: "+str(queue_size))
        print(len(queue) == queue_size)
        if (len(queue) == queue_size):
            print ("Fila atingiu o tamanho para envio")
            print (queue)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #m = {"id": x.id, "position": x.position}
            command = json.dumps(queue)
            print("Enviando para o modelo:"+command)
            
            # print(socket.gethostname())
            sock.connect(('modelo', 9999))
            sock.sendall(command.encode())
            # while len(queue) > 0:
            #     elemento = queue.pop(0)
            #     print(elemento)
            #     x = json.loads(elemento, object_hook=lambda d: SimpleNamespace(**d))
            #     #print(x.id, x.position)

            #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     m = {"id": x.id, "position": x.position}
            #     command = json.dumps(m)
            #     print("Enviando para o modelo:"+command)
                
            #     # print(socket.gethostname())
            #     sock.connect(('modelo', 9999))
            #     sock.sendall(command.encode())
            queue = []

        # print("len queue: "+str(len(queue))+" queue_size: "+str(queue_size))
        # print(len(queue) == queue_size)
        # if (len(queue) == queue_size):
        #     print ("Fila atingiu o tamanho para envio")
        #     while len(queue) > 0:
        #         elemento = queue.pop(0)
        #         print(elemento)
        #         x = json.loads(elemento, object_hook=lambda d: SimpleNamespace(**d))
        #         #print(x.id, x.position)

        #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #         m = {"id": x.id, "position": x.position}
        #         command = json.dumps(m)
        #         print("Enviando para o modelo:"+command)
                
        #         # print(socket.gethostname())
        #         sock.connect(('modelo', 9999))
        #         sock.sendall(command.encode())
        #     queue = []


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
