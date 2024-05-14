Sensor Fusion with Foxglove

How to run:

Do the "colcon build" in the ros2_ws repository.
Go to /home/ros2_ws/build/nmea_divider/build/lib/nmea_divider and do "./parser.py" to run the NMEA parser to get udp data from simulator in port 10110 (Simulator must be running in UDP Client mode port 10110).

Install the foxglove bridge and launch (https://docs.foxglove.dev/docs/connecting-to-data/ros-foxglove-bridge/).

Set the map panel in the foxglove.
