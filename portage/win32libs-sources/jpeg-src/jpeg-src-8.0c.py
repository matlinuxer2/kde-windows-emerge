import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['7.0'] = "http://www.ijg.org/files/jpegsrc.v7.tar.gz"
        self.targetInstSrc['7.0'] = "jpeg-7"
        self.targets['8.0'] = "http://www.ijg.org/files/jpegsrc.v8.tar.gz"
        self.targets['8.0c'] = "http://www.ijg.org/files/jpegsrc.v8c.tar.gz"
        self.targetDigests['8.0c'] = 'f0a3b88ac4db19667798bee971537eeed552bce9'
        
        self.targetInstSrc['8.0'] = "jpeg-8"
        self.targetInstSrc['8.0c'] = "jpeg-8c"
        
        self.patchToApply['7.0'] = ( 'jpeg7.diff', 1 )
        self.patchToApply['8.0'] = ( 'jpeg8.diff', 1 )
        self.patchToApply['8.0c'] = ( 'jpeg8.diff', 1 )

        self.shortDescription = 'A library for manipulating JPEG image format files'
        self.categoryName = 'win32libs'

        self.defaultTarget = '8.0c'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()