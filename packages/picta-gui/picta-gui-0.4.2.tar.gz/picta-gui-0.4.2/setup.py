from setuptools import setup

setup(
    name='picta-gui',
    version='0.4.2',
    install_requires=[
        'opencv-python',
        'psd_tools',
        'tensorflow==2.13.0',
        'Pillow',
        'rawpy'
    ],
    author='Andrew Hanigan',
    author_email='andrew.hanigan@intelligent-it.com',
    description='Simple GUI for use with identifying turtle plastrons',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)