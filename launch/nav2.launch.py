import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_share = get_package_share_directory('nav_stack_project')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    nav2_params = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    map_file = os.path.join(pkg_share, 'maps', 'map.yaml')  # generate via slam.launch.py + map_saver_cli

    map_yaml_arg = DeclareLaunchArgument(
        'map', default_value=map_file,
        description='Full path to map yaml file (only used if not running SLAM live)')

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='true')

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': LaunchConfiguration('map'),
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'params_file': nav2_params,
            'autostart': 'true',
        }.items()
    )

    return LaunchDescription([
        map_yaml_arg,
        use_sim_time_arg,
        nav2_bringup,
    ])
