from setuptools import setup

package_name = 'codigo_gustavo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = codigo_gustavo.my_node:main',
            'talker = codigo_gustavo.publisher_member_function:main',
            'original_talker = codigo_gustavo.original_publisher_member_function:main',
            'listener = codigo_gustavo.subscriber_member_function:main',
            'original_listener = codigo_gustavo.original_subscriber_member_function:main',
            
        ],
    },
)
