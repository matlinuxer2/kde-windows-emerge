import os
import shutil
import utils
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/lloyd/yajl'
        self.targets['1.0.12'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/lloyd-yajl-1.0.12-0-g17b1790.tar.gz"
        self.targetDigests['1.0.12'] = 'f0177e3a946d6ae9a0a963695b2c143a03219bf2'
        self.patchToApply['1.0.12'] = ('lloyd-yajl-17b1790-20110725.diff', 1)
        self.shortDescription = 'Yet Another JSON Library'
        self.targetInstSrc['1.0.12'] = 'lloyd-yajl-17b1790'
        self.defaultTarget = '1.0.12'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

