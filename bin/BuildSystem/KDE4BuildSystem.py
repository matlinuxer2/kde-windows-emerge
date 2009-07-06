# -*- coding: utf-8 -*-
# definitions for the kde build system (cmake and svn)

# todo: split into base CMakeBuildSystem and KDE4BuildSystem

import os
import utils

import base
import info

from Source.SvnSource import *
from BuildSystemBase import *

class KDE4BuildSystem(SvnSource,BuildSystemBase):
    # todo fix setting sourcePath correctly
    sourcePath = ""
    def __init__( self, env = dict( os.environ ) ):
        SvnSource.__init__(self)
        BuildSystemBase.__init__(self)
        
        for key in ["KDESVNUSERNAME", "KDESVNPASSWORD", "KDECOMPILER", "KDESVNDIR", "KDESVNSERVER", 
                    "EMERGE_BUILDTYPE", "EMERGE_OFFLINE", "EMERGE_NOCOPY", "EMERGE_NOCLEAN", "EMERGE_NOFAST", "EMERGE_BUILDTESTS", "EMERGE_MAKE_PROGRAM", "DIRECTORY_LAYOUT" ]:
            if not key in env.keys():
                env[ key ] = None
        self.COMPILER            = env[ "KDECOMPILER" ]
        self.KDESVNUSERNAME      = env[ "KDESVNUSERNAME" ]
        self.KDESVNPASSWORD      = env[ "KDESVNPASSWORD" ]
        self.KDESVNDIR           = env[ "KDESVNDIR" ]
        self.KDESVNSERVER        = env[ "KDESVNSERVER" ]
        if ( self.KDESVNDIR    == None ):
            self.KDESVNDIR       = os.path.join( DOWNLOADDIR, "svn-src", "kde" )
        if ( self.KDESVNSERVER == None ):
            self.KDESVNSERVER    = "svn://anonsvn.kde.org"
        self.BUILDTYPE           = env[ "EMERGE_BUILDTYPE" ]
        if ( self.BUILDTYPE not in ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"] ):
            self.BUILDTYPE=None
        self.OFFLINE = env[ "EMERGE_OFFLINE" ]
        self.NOCOPY = env[ "EMERGE_NOCOPY" ]
        self.NOCLEAN = env[ "EMERGE_NOCLEAN" ]
        self.NOFAST = env[ "EMERGE_NOFAST" ]
        self.BUILDTESTS = env[ "EMERGE_BUILDTESTS" ]
        self.DIRECTORY_LAYOUT = env[ "DIRECTORY_LAYOUT" ]
        self.MAKE_PROGRAM = env[ "EMERGE_MAKE_PROGRAM" ]
        
    def setDirectories( self):
        """ """
        if self.COMPILER   == "msvc2005" or self.COMPILER == "msvc2008":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm      = "nmake"
        elif self.COMPILER == "mingw":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
            self.cmakeMakeProgramm      = "mingw32-make"
        else:
            utils.die( "KDECOMPILER: %s not understood" % self.COMPILER )

        if self.MAKE_PROGRAM:
            self.cmakeMakeProgramm = self.MAKE_PROGRAM
            utils.debug( "set custom make program: %s" % self.MAKE_PROGRAM, 1 )

        if utils.verbose() > 1:
            print "BuildType: %s" % self.BUILDTYPE
        self.buildType = self.BUILDTYPE


        self.buildTests      = False
        self.noCopy          = False
        self.noFetch         = False
        self.noClean         = False
        self.noFast          = True
        self.buildNameExt    = None

        if self.OFFLINE    == "True":
            self.noFetch     = True
        if self.NOCOPY     == "True":
            self.noCopy      = True
        if self.NOCLEAN    == "True":
            self.noClean     = True
        if self.NOFAST    == "False":
            self.noFast      = False
        if self.BUILDTESTS == "True":
            self.buildTests  = True

        # this has to be generalized and moved into VersionSystemSourceBase.py
        self.kdesvndir       = self.KDESVNDIR
        self.kdesvnserver    = self.KDESVNSERVER
        self.kdesvnuser      = self.KDESVNUSERNAME 
        self.kdesvnpass      = self.KDESVNPASSWORD
        
        if utils.verbose() > 1 and self.repositoryPath():
            print "noCopy       : %s" % self.noCopy
            print "repositoryPath()   : %s" % self.repositoryPath().replace("/", "\\")
            
        if not ( self.noCopy and self.repositoryPath() ) :
            if self.repositoryPath():
                self.sourcePath = "..\\%s" % self.repositoryPath().split('/')[-1]
            else:
                self.sourcePath = "..\\%s" % self.instsrcdir
        else:
            self.sourcePath = "%s" % os.path.join(self.kdesvndir, self.repositoryPath() ).replace("/", "\\")
        print "sourcePath" + self.sourcePath
            
    def __unpack( self, svnpath=None, packagedir=None ):
        """fetching and copying the sources from svn"""
        if not svnpath and not packagedir:
            if self.repositoryPath():
                svnpath = self.repositoryPath()[ :self.repositoryPath().rfind('/') ]
                packagedir = self.repositoryPath()[ self.repositoryPath().rfind('/') + 1:]
            else:
                utils.die( "no svn repository information are available" )
        self.fetch( svnpath, packagedir )

        if( not os.path.exists( self.workdir ) ):
            os.makedirs( self.workdir )

        if not ( self.noCopy and self.repositoryPath() ):
            # now copy the tree to workdir
            srcdir  = os.path.join( self.kdesvndir, svnpath, packagedir )
            destdir = os.path.join( self.workdir, packagedir )
            utils.copySrcDirToDestDir( srcdir, destdir )
        return True

    # is this kde or cmake specific 
    def configureDefaultDefines( self ):
        """defining the default cmake cmd line"""
        options = "\"%s\" -DCMAKE_INSTALL_PREFIX=\"%s\" " % \
              ( self.sourcePath, self.rootdir.replace( "\\", "/" ) )

        options = options + "-DCMAKE_INCLUDE_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "include" ).replace( "\\", "/" )

        options = options + "-DCMAKE_LIBRARY_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "lib" ).replace( "\\", "/" )

        if self.buildTests:
            options = options + " -DKDE4_BUILD_TESTS=1 "

        options = options + " -DKDE4_ENABLE_EXPERIMENTAL_LIB_EXPORT:BOOL=ON "
        options = options + " -DKDEWIN_DIR:PATH=\"%s\" " % \
               os.path.join( self.rootdir ).replace( "\\", "/" )

        return options

    def configure( self, buildType=None, customDefines="" ):
        """Using cmake"""

        self.enterBuildDir()
        
        if not self.noClean:
            utils.cleanDirectory( builddir )

        command = r"""cmake -G "%s" %s %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                self.configureDefaultDefines(), \
                customDefines, \
                buildtype )

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def make( self, buildType=None ):
        """Using the *make program"""
        builddir = "%s" % ( self.COMPILER )

        self.enterBuildDir()

        command = self.cmakeMakeProgramm
        # adding Targets later
        if utils.verbose() > 1:
            command += " VERBOSE=1"
        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""
        self.enterBuildDir()

        if utils.verbose() > 0:
            print "builddir: " + builddir

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imageDir() ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType == None ) :
            if( not ( self.configure( self.buildType, customDefines ) and self.make( self.buildType ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType == None ):
            if( not self.__install( self.buildType ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imageDir(), self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""
        self.enterBuildDir()

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True
