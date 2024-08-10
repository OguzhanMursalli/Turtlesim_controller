from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),
        glob('turtle_controller/launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oguzhan',
    maintainer_email='oguzhan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "turtle1_controller = turtle_controller.turtle_pub:main",
            "turtle_add_node = turtle_controller.add_turtle:main"
        ],
         
    },
)
