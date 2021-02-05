import os
from setuptools import setup, find_packages
import sys

here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, 'onvif2/version.txt')
version = open(version_path).read().strip()
def getfiles(dir):
    lst = []
    for i,j,k in os.walk(dir):
        for g in k:
            f=os.path.join(i,g)
            lst.append(f)
    return lst

requires = ['zeep >= 3.0.0']

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Telecommunications Industry',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Utilities',
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
]

wsdl_files = getfiles('wsdl')
wsdl_dst_dir = 'Lib/site-packages/wsdl' if sys.platform == 'win32' else \
               'lib/python%d.%d/site-packages/wsdl' % (sys.version_info.major,
                                                       sys.version_info.minor)

setup(
      name='onvif2_zeep',
      version=version,
      description='Python Client for ONVIF2 Camera',
      long_description=open('README.rst', 'r').read(),
      author='Cheng Ying',
      author_email='yingchengpa@qq.com',
      maintainer='city',
      maintainer_email='yingchengpa@qq.com',
      license='MIT',
      keywords=['ONVIF', 'Camera', 'IPC'],
      url='http://github.com/yingchengpa/python-onvif2',
      zip_safe=False,
      packages=find_packages(exclude=['docs', 'examples', 'tests']),
      install_requires=requires,
      include_package_data=True,
      data_files=[(wsdl_dst_dir, wsdl_files)],
      entry_points={
          'console_scripts': ['onvif-cli = onvif.cli:main']
          }
     )
