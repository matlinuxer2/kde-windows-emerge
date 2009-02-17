import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdemultimedia'
        for ver in ['60']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.1.' + ver + '/src/kdemultimedia-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdemultimedia-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/taglib'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        path = os.path.join( self.rootdir, "win32libs" )
        
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdemultimedia", self.buildTarget, True )
        else:
            return self.doPackaging( "kdemultimedia" )


if __name__ == '__main__':
    subclass().execute()
