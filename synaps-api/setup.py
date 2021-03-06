# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 SamsungSDS, Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import glob
import os

from setuptools import find_packages
from setuptools import setup
from synaps import version

synaps_cmdclass = {}

def find_data_files(destdir, srcdir):
    package_data = []
    files = []
    for d in glob.glob('%s/*' % (srcdir,)):
        if os.path.isdir(d):
            package_data += find_data_files(
                                 os.path.join(destdir, os.path.basename(d)), d)
        else:
            files += [d]
    package_data += [(destdir, files)]
    return package_data

try: 
    from sphinx.setup_command import BuildDoc

    class local_BuildDoc(BuildDoc):
        def run(self):
            for builder in ['html', 'man']:
                self.builder = builder
                self.finalize_options()
                BuildDoc.run(self)
    synaps_cmdclass['build_sphinx'] = local_BuildDoc

except:
    pass

setup(
    name='synaps',
    version=version.canonical_version_string(),
    description='cloud monitoring system',
    author='Samsung SDS',
    author_email='june.yi@samsung.com',
    url='http://www.sdscloud.co.kr/',
    cmdclass=synaps_cmdclass,
    packages=find_packages(exclude=['bin']),
    include_package_data=True,
    data_files=[('/etc/init.d', ['etc/init.d/synaps-api',
                                 'etc/init.d/synaps-noti',
                                 'etc/init.d/storm-nimbus',
                                 'etc/init.d/storm-supervisor',
                                 'etc/init.d/storm-ui']),
                ],
    scripts=['bin/synaps-syncdb',
             'bin/synaps-api-cloudwatch',
             'bin/synaps-notification',
             ],
    setup_requires=[],
    py_modules=[]
)
