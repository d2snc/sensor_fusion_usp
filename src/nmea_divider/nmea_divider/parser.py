#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import socket
import pynmea2
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float32


class Parser(Node):
    def __init__(self):
        super().__init__("parser_node")
        self.publisher_gps = self.create_publisher(NavSatFix, 'gps', 10)
        self.publisher_speed = self.create_publisher(Float32, 'speed', 10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 10110))
        self.parse_data()

    def parse_data(self):
        while True:
            data, _ = self.sock.recvfrom(1024)
            try:
                msg = pynmea2.parse(data.decode('utf-8'))
                if isinstance(msg, pynmea2.GGA):
                    self.publish_data(msg)
            except pynmea2.ParseError:
                pass

    def publish_data(self, msg):
        if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
            gps_msg = NavSatFix()
            gps_msg.latitude = msg.latitude
            gps_msg.longitude = msg.longitude
            self.publisher_gps.publish(gps_msg)
            self.get_logger().info("GPS data was published")

        if hasattr(msg, 'spd_over_grnd_kmph'):
            speed_msg = Float32()
            speed_msg.data = msg.spd_over_grnd_kmph
            self.publisher_speed.publish(speed_msg)
            self.get_logger().info("Speed {} was published in topic speed".format(msg.spd_over_grnd_kmph))


def main(args=None):
    rclpy.init(args=args)
    node = Parser()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
