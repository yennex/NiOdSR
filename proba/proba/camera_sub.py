#!/usr/bin/env python3
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from geometry_msgs.msg import Point # Image is the message type
from cv_bridge import CvBridge # ROS2 package to convert between ROS and OpenCV Images
import cv2 # Python OpenCV library
import numpy as np

#Funkcja wyrysowująca linie oraz wypisująca tekst na podanym obrazie
def draw_window(image_data):
        cv_image = np.zeros((512,700,3), np.uint8)
        cv_image = cv2.line(cv_image,(255,0),(255,512),(255,200,0))
        cv_image = cv2.line(cv_image,(445,0),(445,512),(255,200,0))
        cv_image = cv2.line(cv_image,(255,256),(445,256),(255,200,0))
        cv_image = cv2.putText(cv_image,'DO PRZODU', (305,125),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,200,0),2,cv2.LINE_AA)
        cv_image = cv2.putText(cv_image,'DO TYLU', (320,400),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,200,0),2,cv2.LINE_AA)
        cv_image = cv2.putText(cv_image,'SKRET LEWO', (70,260),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,200,0),2,cv2.LINE_AA)
        cv_image = cv2.putText(cv_image,'SKRET PRAWO', (530,260),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,200,0),2,cv2.LINE_AA)
        return cv_image
        
    


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('Point_Publisher')
        self.window_name = "camera"
        self.subscription = self.create_subscription(Image,'image_raw',self.listener_callback,10)
        self.declare_parameter('size', 5)
        self.my_size = self.get_parameter('size').value       
        self.subscription  # prevent unused variable warning
        self.point = None
        self.point_msg = Point()
        self.publisher = self.create_publisher(Point,'point',10) #stworzenie publishera na temacie point
        

    def listener_callback(self, image_data):
        cv_image=draw_window(image_data)
        if(self.point is not None):
            cv2.circle(cv_image,self.point,self.my_size,(255,200,0),-1)
            self.publisher.publish(self.point_msg)
        cv2.imshow(self.window_name, cv_image)
        cv2.waitKey(25)
        cv2.setMouseCallback(self.window_name, self.draw_rectangle) 

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN: # check if mouse event is click
            self.point = (x,y)
            self.point_msg.x = np.float(x)
            self.point_msg.y = np.float(y)
         	


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    minimal_subscriber.get_logger().info('Subskrybent Camery Aktywny')
    rclpy.spin(minimal_subscriber)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
