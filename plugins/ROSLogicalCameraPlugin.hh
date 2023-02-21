 * Copyright 2016 Open Source Robotics Foundation * * Licensed under the Apache License, Version 2.0 (the "License"); * you may not use this file except in compliance with the License. * You may obtain a copy of the License at * *     http://www.apache.org/licenses/LICENSE-2.0 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
*/

#ifndef _ROS_LOGICAL_CAMERA_PLUGIN_HH_
#define _ROS_LOGICAL_CAMERA_PLUGIN_HH_

#include <sdf/sdf.hh>

#include "gazebo/common/Plugin.hh"
#include "gazebo/common/UpdateInfo.hh"
#include "gazebo/msgs/logical_camera_image.pb.h"
#include "gazebo/physics/PhysicsTypes.hh"
#include "gazebo/transport/Node.hh"
#include "gazebo/transport/Subscriber.hh"
#include "gazebo/transport/TransportTypes.hh"

// ROS
#include <ros/ros.h>

namespace gazebo
{
  class ROSLogicalCameraPlugin : public ModelPlugin
  {
    public: ROSLogicalCameraPlugin();
    public: virtual ~ROSLogicalCameraPlugin();
    protected: physics::ModelPtr model;
    protected: physics::LinkPtr cameraLink;
    protected: sensors::SensorPtr sensor;
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf);
    protected: void FindLogicalCamera();
    public: void OnImage(ConstLogicalCameraImagePtr &_msg);
    protected: transport::NodePtr node;
    protected: transport::SubscriberPtr imageSub;
    protected: std::string robotNamespace;
    protected: ros::NodeHandle *rosnode;
    protected: ros::Publisher imagePub;
  };
}
#endif