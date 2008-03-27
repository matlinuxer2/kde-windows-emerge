import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4'
        self.defaultTarget = 'svnHEAD'
        self.languages = 'de'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['testing/gettext-tools'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        svnpath = self.kdeSvnPath()
        utils.cleanDirectory( self.workdir )

        if not self.kdeSvnUnpack( svnpath, "scripts" ):
            return False
            
        for pkg in self.subinfo.languages.split():
            if not self.kdeSvnUnpack( svnpath, pkg ):
                return False

                
        srcdir  = os.path.join( self.kdesvndir, svnpath, "scripts" )
        destdir = os.path.join( self.workdir, "scripts" )
        utils.copySrcDirToDestDir( srcdir, destdir )
        
        for pkg in self.subinfo.languages.split():
            srcdir  = os.path.join( self.kdesvndir, svnpath, pkg )
            destdir = os.path.join( self.workdir, pkg )
            utils.copySrcDirToDestDir( srcdir, destdir )
            
        # execute autogen.sh and generate the CMakeLists.txt files
        self.msys.msysExecute( self.workdir, os.path.join( self.workdir, "scripts", "autogen.sh" ), self.subinfo.languages )
        # revpath is not available in msys
        return True

    def compile( self ):
        self.kde.nocopy = False
        for pkg in self.subinfo.languages.split():
            self.kde.buildNameExt = pkg
            self.kde.sourcePath = "..\\" + pkg
            if not self.kdeCompile():
                return False
        return True

    def install( self ):
        self.kde.nocopy = False
        for pkg in self.subinfo.languages.split():
            self.kde.buildNameExt = pkg
            if not self.kdeInstall():
                return False
        return True

    def make_package( self ):
        self.svnpath = os.path.join( self.kdesvndir, self.subinfo.svnTargets['svnHEAD'] )
        self.filesdir = os.path.join( self.packagedir, "files" )
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        if not utils.test4application( "kdewin-packager" ):
            utils.die( "kdewin-packager not found - please make sure it is in your path" )

        for pkg in self.subinfo.languages.split():
            workdir = os.path.join( self.workdir, pkg )
            cmd = "kdewin-packager -name kde-i18n-%s -version %s -hashfirst -compression 2 -root %s/%s -destdir %s" % \
                  ( pkg, self.version, self.imagedir, pkg, dstpath )
            utils.system( cmd )
        return True

if __name__ == '__main__':
    subclass().execute()
