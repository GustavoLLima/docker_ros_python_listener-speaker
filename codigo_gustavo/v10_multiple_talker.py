import socket
import sys
import json
from random import randrange
from time import time, sleep

from types import SimpleNamespace

import os
my_name = os.environ['my_name']
end_topic = os.environ['end_topic']
import rclpy
import random
from rclpy.node import Node

from std_msgs.msg import String

msg_to_send = ""


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 10  # seconds


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((my_name, 9999))
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

            x = json.loads(received_message, object_hook=lambda d: SimpleNamespace(**d))
            print(x)

            print ("------------")
            #received_message = ["{\"id\": 1, \"position\": 9}", "{\"id\": 2, \"position\": 60}"]
            for msg in x:
                print("message:")
                print(msg)
                #message = str(message).replace('"',"'")
                #x = json.loads(message, object_hook=lambda d: SimpleNamespace(**d))
                print ("msg.id:")
                print (msg.id)
                print ("msg.action")
                print (msg.action)
                m = {'id': msg.id, 'action': msg.action}
                #conf_parameters.append(["agent", int(msg.id), int(msg.action)])

                global msg_to_send
                msg_to_send = m

                #x = json.loads(m, object_hook=lambda d: SimpleNamespace(**d))
                #print(x.id, x.position)

                # test_string = my_hostname
                # my_id = int(''.join(filter(lambda i: i.isdigit(), test_string)))
                topic = end_topic+msg.id
                self.publisher_ = self.create_publisher(String, topic, 10)
                # self.timer_callback()
                msg = String()
                # if (random.randint(1,10) >= 5):
                #   msg.data = '1'
                # else:
                #   msg.data = '0'
                print("msg_to_send:")
                print(msg_to_send)
                msg.data = json.dumps(msg_to_send)
                
                #msg.data = 'Hello World: %d' % self.i
                self.publisher_.publish(msg)
                self.get_logger().info('Publishing: "%s"' % msg.data)


            # self.timer_callback()


        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

    def timer_callback(self):
        print (".")
        # msg = String()
        # # if (random.randint(1,10) >= 5):
        # #   msg.data = '1'
        # # else:
        # #   msg.data = '0'
        # msg.data = msg_to_send
        
        # #msg.data = 'Hello World: %d' % self.i
        # self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1


def main(args=None):

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(("talker", 9999))
    # s.listen(2)

    # while True:
    #     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # s.bind(("python_server", 9999))
    #     # s.listen(2)
    #     conn, addr = s.accept()
    #     print("Conexão estabelecida com %s" % str(addr))
    #     received_message = bytes.decode(conn.recv(1024))
    #     print ("Mensagem recebida:")
    #     print(received_message)
    #     global msg_to_send
    #     msg_to_send = received_message

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

# FUNCIONANDO, MAS QUERENDO DEIXAR O TALKER COMO UM ÚNICO CONTAINER QUE MANDA PRA TODOS, DINAMICAMENTE COM BASE NO ID DA MENSAGEM

# import socket
# import sys
# import json
# from random import randrange
# from time import time, sleep

# from types import SimpleNamespace

# import os
# my_hostname = os.environ['my_hostname']

# import rclpy
# import random
# from rclpy.node import Node

# from std_msgs.msg import String

# msg_to_send = ""


# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         # self.publisher_ = self.create_publisher(String, 'topic', 10)
#         timer_period = 10  # seconds


#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.bind((my_hostname, 9999))
#         s.listen(2)

#         while True:
#             # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             # s.bind(("python_server", 9999))
#             # s.listen(2)
#             conn, addr = s.accept()
#             print("Conexão estabelecida com %s" % str(addr))
#             received_message = bytes.decode(conn.recv(1024))
#             print ("Mensagem recebida:")
#             print(received_message)
#             global msg_to_send
#             msg_to_send = received_message

#             test_string = my_hostname
#             my_id = int(''.join(filter(lambda i: i.isdigit(), test_string)))
#             topic = "final_output_agent"+str(my_id)
#             self.publisher_ = self.create_publisher(String, topic, 10)


#             self.timer_callback()


#         # self.timer = self.create_timer(timer_period, self.timer_callback)
#         # self.i = 0

#     def timer_callback(self):
#         msg = String()
#         # if (random.randint(1,10) >= 5):
#         #   msg.data = '1'
#         # else:
#         #   msg.data = '0'
#         msg.data = msg_to_send
        
#         #msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         # self.i += 1


# def main(args=None):

#     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # s.bind(("talker", 9999))
#     # s.listen(2)

#     # while True:
#     #     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #     # s.bind(("python_server", 9999))
#     #     # s.listen(2)
#     #     conn, addr = s.accept()
#     #     print("Conexão estabelecida com %s" % str(addr))
#     #     received_message = bytes.decode(conn.recv(1024))
#     #     print ("Mensagem recebida:")
#     #     print(received_message)
#     #     global msg_to_send
#     #     msg_to_send = received_message

#     #x = json.loads(received_message, object_hook=lambda d: SimpleNamespace(**d))
#     #print(x.id, x.action)

#     # m = {"id": int(received_message), "action": "stop"} # a real dict.
#     # command = json.dumps(m)

#     #command = "dsadsasdasadsda"
#     #print ("Enviando para o cliente:"+command)

#     #conn.sendall(command.encode('ascii'))



#     #Código ROS
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

### FUNCIONANDO, SÓ SEPARANDO PRA MANDAR PRA TÓPICOS SEPARADOS E NÃO ENTRAR EM CONFLITO COM O PRINCIPAL
# import socket
# import sys
# import json
# from random import randrange
# from time import time, sleep

# from types import SimpleNamespace

# import os
# my_hostname = os.environ['my_hostname']

# import rclpy
# import random
# from rclpy.node import Node

# from std_msgs.msg import String

# msg_to_send = ""


# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'topic', 10)
#         timer_period = 10  # seconds


#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.bind((my_hostname, 9999))
#         s.listen(2)

#         while True:
#             # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             # s.bind(("python_server", 9999))
#             # s.listen(2)
#             conn, addr = s.accept()
#             print("Conexão estabelecida com %s" % str(addr))
#             received_message = bytes.decode(conn.recv(1024))
#             print ("Mensagem recebida:")
#             print(received_message)
#             global msg_to_send
#             msg_to_send = received_message
#             self.timer_callback()


#         # self.timer = self.create_timer(timer_period, self.timer_callback)
#         # self.i = 0

#     def timer_callback(self):
#         msg = String()
#         # if (random.randint(1,10) >= 5):
#         #   msg.data = '1'
#         # else:
#         #   msg.data = '0'
#         msg.data = msg_to_send
        
#         #msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         # self.i += 1


# def main(args=None):

#     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # s.bind(("talker", 9999))
#     # s.listen(2)

#     # while True:
#     #     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #     # s.bind(("python_server", 9999))
#     #     # s.listen(2)
#     #     conn, addr = s.accept()
#     #     print("Conexão estabelecida com %s" % str(addr))
#     #     received_message = bytes.decode(conn.recv(1024))
#     #     print ("Mensagem recebida:")
#     #     print(received_message)
#     #     global msg_to_send
#     #     msg_to_send = received_message

#     #x = json.loads(received_message, object_hook=lambda d: SimpleNamespace(**d))
#     #print(x.id, x.action)

#     # m = {"id": int(received_message), "action": "stop"} # a real dict.
#     # command = json.dumps(m)

#     #command = "dsadsasdasadsda"
#     #print ("Enviando para o cliente:"+command)

#     #conn.sendall(command.encode('ascii'))



#     #Código ROS
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
