# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

__version__           = '0.42'
__build__             = '1087'
__bundle_name__       = 'parrot'
__bundle_identifier__ = f'com.themacronaut.{__bundle_name__.lower()}'

class _AppInfo(object):
    def __init__(self):
        super(_AppInfo, self).__init__()
        
        self.name        = 'Parrot'
        self.bundle_name = __bundle_name__
        self.tag_line    = 'An intuitive way to mimic REST APIs'
        self.version     = __version__
        self.build       = __build__
        self.identifier  = __bundle_identifier__
        self.copyright   = 'Copyright © 2010-2019 Farhan Ahmed. All rights reserved.'

__app_info__ = _AppInfo()
