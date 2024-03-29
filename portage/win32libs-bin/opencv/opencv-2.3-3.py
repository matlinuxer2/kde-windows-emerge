# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git475c7d8bede9822dd317bc9ae7868544e04a7cf7

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '2.3', '2.3-1', '2.3-2', '2.3-3' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'opencv', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'opencv', version, '.tar.bz2.sha1' )

        self.defaultTarget = '2.3-3'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
