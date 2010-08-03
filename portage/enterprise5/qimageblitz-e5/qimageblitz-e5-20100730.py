import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.0.5'] = 'tags/qimageblitz/0.0.5'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/qimageblitz'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/qimageblitz'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/qimageblitz'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/qimageblitz'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/qimageblitz'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/qimageblitz'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/qimageblitz'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/qimageblitz'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/qimageblitz'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/qimageblitz'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/qimageblitz'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/qimageblitz'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/qimageblitz'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/qimageblitz'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/qimageblitz'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/qimageblitz'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/qimageblitz'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/qimageblitz'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdesupport/qimageblitz'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdesupport/qimageblitz'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdesupport/qimageblitz'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdesupport/qimageblitz'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdesupport/qimageblitz'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdesupport/qimageblitz'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdesupport/qimageblitz'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdesupport/qimageblitz'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdesupport/qimageblitz'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdesupport/qimageblitz'
        self.defaultTarget = '20100730'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "qimageblitz"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "qimageblitz", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()