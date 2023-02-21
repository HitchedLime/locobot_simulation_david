#ifndef _LOGCAM_PLUGIN_HH_
#define _LOGCAM_PLUGIN_HH_

#include <gazebo/gazebo.hh>
#include <gazebo/sensors/Sensor.hh>
#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <gazebo/sensors/LogicalCameraSensor.hh>
#include <gazebo/transport/TransportTypes.hh>
#include "ros/callback_queue.h"


namespace gazebo
{
  /// \brief A plugin to publish the objects seen by the logical camera sensor.
  class LogCamPlugin : public SensorPlugin
  {
    /// \brief Constructor
    public: LogCamPlugin() {}

    /// \brief The load function is called by Gazebo when the plugin is
    /// inserted into simulation
    /// \param[in] _sensor A pointer to the model that this plugin is
    /// attached to.
    /// \param[in] _sdf A pointer to the plugin's SDF element.
    public: virtual void Load(sensors::SensorPtr _sensor, sdf::ElementPtr _sdf)
    {

      // Make sure the ROS node for Gazebo has already been initialized
      // Initialize ROS node
      if (!ros::isInitialized())
      {
        int argc = 0;
        char **argv = NULL;
        ros::init(argc, argv, "gazebo", ros::init_options::NoSigintHandler);
      }


      // Create our ROS node. This acts in a similar manner to
      // the Gazebo node
      this->rosNode.reset(new ros::NodeHandle("gazebo_client"));

      // Create a ROS publisher for the camera data
      ros::NodeHandle nh;
      std::string topic_name = _sdf->Get<std::string>("topic_name");
      // camera_pub_ = nh.advertise<sensor_msgs::Image>(topic_name, 1);
      // camera_pub_ = nh.advertise<msgs::LogicalCameraImage>(topic_name, 1);

      sensors::LogicalCameraSensorPtr logicalCamera = std::dynamic_pointer_cast<sensors::LogicalCameraSensor>(_sensor);
      
      msgs::LogicalCameraImage sensorOutput = logicalCamera->Image();
      // Just output a message for now
      std::cerr << "\n\n\n\n\n\nThe Logical camera plugin is attach to model[" <<
        _sensor->Name() << "]\n\n\n\n\n\n";


      // Spin up the queue helper thread.
      this->rosQueueThread =
        std::thread(std::bind(&LogCamPlugin::QueueThread, this));
    }
    
    /// \brief ROS helper function that processes messages
    private: void QueueThread()
    {
      static const double timeout = 0.01;
      while (this->rosNode->ok())
      {
        this->rosQueue.callAvailable(ros::WallDuration(timeout));
      }
    }


    /// \brief A ROS publisher to publish the contents of the logical camera
    private: ros::Publisher camera_pub_;
    /// \brief A node use for ROS transport
    private: std::unique_ptr<ros::NodeHandle> rosNode;
    /// \brief A ROS callbackqueue that helps process messages
    private: ros::CallbackQueue rosQueue;
    /// \brief A thread the keeps running the rosQueue
    private: std::thread rosQueueThread;


  };

  // Tell Gazebo about this plugin, so that Gazebo can call Load on this plugin.
  GZ_REGISTER_SENSOR_PLUGIN(LogCamPlugin)
}
#endif