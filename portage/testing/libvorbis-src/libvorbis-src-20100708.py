# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.3.1'] = 'http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.1.tar.gz'
        self.targetInstSrc['1.3.1'] = 'libvorbis-1.3.1'
        self.patchToApply['1.3.1'] = ('libvorbis-1.3.1-20100708.diff', 1)
        self.options.package.withCompiler = False
        self.options.package.packageName = "libvorbis"
        self.defaultTarget = '1.3.1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['testing/libogg-src'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()