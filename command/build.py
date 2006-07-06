import os
import sys
from distutils.command.build import build as old_build
from distutils.util import get_platform

class build(old_build):

    sub_commands = [('config_fc',     lambda *args: 1),
                    ('build_src',     old_build.has_ext_modules),
                    ] + old_build.sub_commands

    def finalize_options(self):
        build_scripts = self.build_scripts
        old_build.finalize_options(self)
        plat_specifier = ".%s-%s" % (get_platform(), sys.version[0:3])
        if build_scripts is None:
            self.build_scripts = os.path.join(self.build_base,
                                              'scripts' + plat_specifier)
