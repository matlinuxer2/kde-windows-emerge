# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git9e68ba20b63f582f00614117ddfd24524f758f1c

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '1.1.4-3', '1.3.0', '1510', '1510-1', '1510-2' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'gpgme', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'gpgme', version, '.tar.bz2.sha1' )

        self.shortDescription = '''GnuPG cryptography support library (runtime)'''

        self.defaultTarget = '1510-2'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/assuan2' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/gpg-error' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
