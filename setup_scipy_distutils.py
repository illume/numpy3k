#!/usr/bin/env python

import os
from misc_util import get_path, default_config_dict, dot_join

def configuration(parent_package='',parent_path=None):
    package = 'scipy_distutils'
    local_path = get_path(__name__,parent_path)
    config = default_config_dict(package,parent_package)

    sub_package = dot_join(package,'command')
    config['packages'].append(dot_join(parent_package,sub_package))
    config['package_dir'][sub_package] = os.path.join(local_path,'command')

    config['data_files'].append((package,[os.path.join(local_path,'sample_site.cfg')]))
    return config

if __name__ == '__main__':
    from scipy_distutils_version import scipy_distutils_version
    print 'scipy_distutils Version',scipy_distutils_version
    from distutils.core import setup
    config = configuration()
    for k,v in config.items():
        if not v:
            del config[k]
    setup(version = scipy_distutils_version,
          description = "Changes to distutils needed for SciPy "\
          "-- mostly Fortran support",
          author = "Travis Oliphant, Eric Jones, and Pearu Peterson",
          author_email = "scipy-dev@scipy.org",
          license = "SciPy License (BSD Style)",
          url = 'http://www.scipy.org',
          **config
          )
