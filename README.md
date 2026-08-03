# nav_stack_project

[![Build](https://github.com/YOUR_USERNAME/nav_stack_project/actions/workflows/build.yml/badge.svg)](https://github.com/YOUR_USERNAME/nav_stack_project/actions/workflows/build.yml)
![ROS2](https://img.shields.io/badge/ROS2-Humble%20%7C%20Jazzy-22314E?logo=ros&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

A ROS2 portfolio project: a differential-drive robot with LiDAR, mapped with
**SLAM Toolbox**, navigated autonomously with **Nav2**, using a **custom
global planner plugin** written from scratch (not just stock Nav2 config).

Built for: Nav2 + SLAM + Gazebo, ROS2 Humble or Jazzy.

<!-- Demo GIF goes here once recorded -- highest-impact addition to this README:
![demo](docs/demo.gif) -->

![architecture](docs/architecture.svg)

## What's actually custom here

Most "I did ROS2 nav" portfolio projects stop at launching `nav2_bringup`
with default params. This project adds a hand-written **global planner
plugin** (`src/nav_stack_project/straight_line_planner.cpp`) that implements
the `nav2_core::GlobalPlanner` interface directly — it's registered via
`planner_plugin.xml` and swapped in as `GridBased` in `config/nav2_params.yaml`.

It currently does simple greedy interpolation toward the goal and flags
costmap collisions rather than avoiding them. That's intentional: it's a
clean base to extend into something more interesting for a resume bullet —
Theta*, Jump Point Search, or a potential-field/gradient planner. The hook
point is clearly marked in `createPlan()`.

## Prerequisites

- Ubuntu 22.04 (Humble) or 24.04 (Jazzy)
- ROS2 installed (`sudo apt install ros-<distro>-desktop`)
- `sudo apt install ros-<distro>-navigation2 ros-<distro>-nav2-bringup \
    ros-<distro>-slam-toolbox ros-<distro>-gazebo-ros-pkgs \
    ros-<distro>-xacro ros-<distro>-robot-state-publisher`

## Build

```bash
mkdir -p ~/nav_ws/src
cp -r nav_stack_project ~/nav_ws/src/
cd ~/nav_ws
colcon build --symlink-install
source install/setup.bash
```

## Workflow

**1. Map the environment (SLAM):**
```bash
ros2 launch nav_stack_project bringup.launch.py
```
This starts Gazebo (robot in `worlds/simple_world.world`), SLAM Toolbox, and
RViz. In another terminal, drive the robot around to build the map:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**2. Save the map:**
```bash
ros2 run nav2_map_server map_saver_cli -f ~/nav_ws/src/nav_stack_project/maps/map
```

**3. Autonomous navigation with the custom planner:**
```bash
ros2 launch nav_stack_project gazebo.launch.py
ros2 launch nav_stack_project nav2.launch.py map:=~/nav_ws/src/nav_stack_project/maps/map.yaml
```
Set an initial pose and a Nav2 goal in RViz (`2D Pose Estimate`, `Nav2 Goal`),
or via CLI:
```bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: 1.5, y: 0.5, z: 0.0}}}}"
```

Watch `/plan` in RViz — that path is coming from your custom planner, not
the stock Nav2 A*/Theta* implementation.

## Project structure

```
nav_stack_project/
├── urdf/robot.urdf.xacro          # diff-drive base + LiDAR + Gazebo plugins
├── worlds/simple_world.world       # arena with obstacles for SLAM/nav testing
├── config/slam_params.yaml         # SLAM Toolbox tuning
├── config/nav2_params.yaml         # Nav2 stack config, wires in custom planner
├── include/ + src/                 # custom StraightLinePlanner (nav2_core::GlobalPlanner)
├── planner_plugin.xml              # pluginlib export for the custom planner
├── launch/
│   ├── gazebo.launch.py            # spawn robot in Gazebo
│   ├── slam.launch.py              # SLAM Toolbox mapping
│   ├── nav2.launch.py              # Nav2 bringup with custom planner + saved map
│   └── bringup.launch.py           # gazebo + SLAM + RViz, all together
├── rviz/nav_view.rviz
├── docs/architecture.svg           # system diagram (shown above)
├── .github/workflows/build.yml     # CI: colcon build + test on every push
├── LICENSE
└── .gitignore
```

## Suggested next steps (good "what I'd do with more time" answers)

- Replace the greedy interpolation in `createPlan()` with **Theta\*** (line-of-sight
  smoothing over A*) or **Jump Point Search** — biggest algorithmic upgrade.
- Add a **behavior tree** customization (`bt_navigator`) for recovery behaviors
  specific to this robot's failure modes.
- Swap the LiDAR-only setup for LiDAR + depth camera and fuse via `robot_localization`
  (EKF) for better odometry — good talking point for a perception-adjacent role.
- Containerize with Docker so anyone can reproduce the demo without a ROS2 install.
- Record a short screen-capture GIF of RViz showing SLAM building the map and
  then the robot navigating with the custom planner — put it at the top of
  the GitHub README. This single artifact does more for a recruiter's first
  30 seconds than anything else in this repo.

## License

MIT — use freely for your own portfolio.
