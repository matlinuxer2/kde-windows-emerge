# -*- coding: utf-8 -*-
import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20110510"
        self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w32-bin_i686-mingw_"+ver+"_sezero.zip"
        self.targetDigests['20110510'] = 'e0b11347ad731cfb0eb364d51750eb63480a17b4'
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

    def install(self):
        shutil.move( os.path.join( self.installDir() , "mingw32" ) , os.path.join( self.installDir(), "mingw" ) )
        shutil.copy( os.path.join( self.installDir() , "mingw" , "bin" , "gmake.exe") , os.path.join( self.installDir() , "mingw" , "bin" , "mingw32-make.exe") )
        utils.applyPatch( self.imageDir(), os.path.join( self.packageDir(), "gcc_Exit.diff"), 0 )
        # FIXME: this is a hack for tzSpecificTimeToSystemLocalTime
        # Remove this when you update the mingw version
        # the lib is generated out of the def file from the 2.0 release 
        #dlltool -d kernel32.def -l libkernel32.a -k
        shutil.copy( os.path.join( self.packageDir(), "libkernel32.a" ),
                    os.path.join( self.installDir(), "mingw", "i686-w64-mingw32", "lib" ) )
        return True

if __name__ == '__main__':
    Package().execute()
