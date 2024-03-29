import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.0.1', '2.0.2']:
            self.targets[ ver ] = 'ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'libassuan-' + ver

        self.patchToApply['2.0.1'] = [ ('libassuan-cmake.diff', 1), ('assuan-381-head.diff', 0), ('libassuan-2.0.1-20101029.diff', 1) ]
        self.patchToApply['2.0.2'] = [ ('libassuan-2.0.2-20110831.diff', 1), ('libassuan-2.0.2-cmake.diff', 1) ]

        self.targets['400'] = "http://downloads.sourceforge.net/kde-windows/libassuan-r400.tar.bz2"
        self.targetInstSrc['400'] = "libassuan-r400"
        self.patchToApply['400'] = [ ('libassuan-cmake.diff', 1), ('libassuan-2.0.1-20101029.diff', 1) ]
        self.targetDigests['400'] = '91d85d50ccdc40b5353abe8190d6bd5ee9fb0be4'
        self.targetDigests['2.0.1'] = 'b7e9dbd41769cc20b1fb7db9f2ecdf276ffc352c'
        self.targetDigests['2.0.2'] = 'dbcd96e2525d4c3a2da9e8054a06fa517f20a185'

        self.shortDescription = "an IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = '400'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/gpg-error'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
