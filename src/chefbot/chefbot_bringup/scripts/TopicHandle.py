#!/usr/bin/env python
import rospy

from std_msgs.msg import String

from std_msgs.msg import Int16,Int32, Int64, Float32, String, Header, UInt64

from sensor_msgs.msg import Imu

def callback(data):
    #rospy.loginfo("%s", data.data)

    dataLine = data.data.split('\n')
    for i in range(len(dataLine)):
    	#print(dataLine[i])
    	dataSplit = dataLine[i].split('\t')
    	if(dataSplit[0] == 'e'):
    		left_encoder_value = long(dataSplit[1])
    		right_encoder_value = long(dataSplit[2])
    		Left_Encoder.publish(left_encoder_value)
    		Right_Encoder.publish(right_encoder_value)

    	if(dataSplit[0] == 'i'):
    		qx = float(dataSplit[1])
    		qy = float(dataSplit[2])
    		qz = float(dataSplit[3])
    		qw = float(dataSplit[4])
    		qx_.publish(qx)
    		qy_.publish(qy)
    		qz_.publish(qz)
    		qw_.publish(qw)
    		imu_msg = Imu()
    		h = Header()
    		h.stamp = rospy.Time.now()
    		h.frame_id = frame_id

    		imu_msg.header = h

    		imu_msg.orientation_covariance = (-1., )*9	
    		imu_msg.angular_velocity_covariance = (-1., )*9
    		imu_msg.linear_acceleration_covariance = (-1., )*9


    		imu_msg.orientation.x = qx
    		imu_msg.orientation.y = qy
    		imu_msg.orientation.z = qz
    		imu_msg.orientation.w = qw

    		imu_pub.publish(imu_msg)

    	if(dataSplit[0] == 's'):
    		left_wheel_speed = float(dataSplit[1])
    		right_wheel_speed = float(dataSplit[2])

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("IMU", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    Left_Encoder = rospy.Publisher('lwheel', Int64, queue_size = 10)
    Right_Encoder = rospy.Publisher('rwheel', Int64, queue_size = 10)
    #Publisher for IMU rotation quaternion values
    qx_ = rospy.Publisher('qx', Float32, queue_size = 10)
    qy_ = rospy.Publisher('qy', Float32, queue_size = 10)
    qz_ = rospy.Publisher('qz', Float32, queue_size = 10)
    qw_ = rospy.Publisher('qw', Float32, queue_size = 10)
    frame_id = '/base_footprint'
    cal_offset = 0.0
    orientation = 0.0
    cal_buffer =[]
    cal_buffer_length = 1000
    imu_data = Imu(header=rospy.Header(frame_id="base_footprint"))
    imu_data.orientation_covariance = [1e6, 0, 0, 0, 1e6, 0, 0, 0, 1e-6]
    imu_data.angular_velocity_covariance = [1e6, 0, 0, 0, 1e6, 0, 0, 0, 1e-6]
    imu_data.linear_acceleration_covariance = [-1,0,0,0,0,0,0,0,0]
    gyro_measurement_range = 150.0 
    gyro_scale_correction = 1.35
    imu_pub = rospy.Publisher('imu/data', Imu,queue_size = 10)

    deltat = 0
    lastUpdate = 0

    listener()