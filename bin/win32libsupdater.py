# win32libsupdater.py

import os
import sys
import utils
import portage
import subprocess
import xml.dom.minidom
from string import Template  # pylint: disable=W0402


#################################################

KDEROOT = os.getenv("KDEROOT")
KDEROOT.replace("\\", "/")

#################################################

def getSvnVersion( path ):
    svninfo = subprocess.Popen( ['svn', 'info', '--xml', path ], shell=True, stdout=subprocess.PIPE ).communicate()[0]
    doc = xml.dom.minidom.parseString( svninfo )
    latestcommit = doc.getElementsByTagName( "commit" )[0]
    rev = latestcommit.getAttribute( "revision" )
    if rev == "":
        rev = "-unknown"
    return "svn" + rev

def getGitVersion( path ):
    gitinfo = subprocess.Popen( ['git', 'log', '-n 1', '--format=format:%H'], shell=True, stdout=subprocess.PIPE ).communicate()[0]
    return "git" + gitinfo

def svnRename( currentName, newName ):
    cmd = "svn --non-interactive rename %s %s" % ( currentName, newName )

    utils.debug( "running command: %s" % cmd )
    p = subprocess.Popen( cmd, shell=True, stdin=subprocess.PIPE )
    return p.wait() == 0

def gitRename( currentName, newName ):
    p = subprocess.Popen( ['git', 'mv', currentName, newName], shell=True, stdin=subprocess.PIPE )
    return p.wait() == 0

def svnAdd( newDir ):
    cmd = "svn --non-interactive add %s" % ( newDir )
    ret = 0
    utils.debug( "running command: %s" % cmd )
    p = subprocess.Popen( cmd, shell=True, stdin=subprocess.PIPE )
    return p.wait() == 0

def gitAdd( newDir ):
    p = subprocess.Popen( ['git', 'add', newDir], shell=True, stdin=subprocess.PIPE )
    return p.wait() == 0

doPretend = False
if "-p" in sys.argv:
    doPretend = True
    sys.argv.remove('-p')

if len( sys.argv ) < 2 or not os.path.isfile( sys.argv[ 1 ] ):
    print "packageList as first argument required!"
    print
    print "%s [-p] packagelist" % sys.argv[ 0 ]
    print "The option -p shows what"
    exit( 1 )


# parse the package file
packagefile = file( sys.argv[ 1 ] )
addInfo = dict()
for line in packagefile:
    if not line.startswith( '#' ):
        cat, pac, target, patchlvl = line.strip().split( ',' )
        addInfo[ cat + "/" + pac ] = ( target, patchlvl )
packagefile.close()

baseDependencies = """
    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
"""

for packageKey in addInfo:
    category, package = packageKey.split( '/' )
    version = portage.PortageInstance.getNewestVersion( category, package )
    srcTargets = portage.PortageInstance.getAllTargets( category, package, version )
    binCategory, binPackage = portage.PortageInstance.getCorrespondingBinaryPackage( package )
    if binPackage:
        utils.debug( "found a binary package for %s" % package, 1 )
        binVersion = portage.PortageInstance.getNewestVersion( binCategory, binPackage )
        binTargets = portage.PortageInstance.getAllTargets( binCategory, binPackage, binVersion )

        description = ""
        metadata = portage.PortageInstance.getMetaData( category, package, version )
        if "shortDescription" in metadata: description = metadata["shortDescription"]

        # check that the target from the source package which has been build is contained in the
        # binary package
        buildTarget = addInfo[ packageKey ] [ 0 ]
        if buildTarget == '':
            buildTarget = portage.PortageInstance.getDefaultTarget( category, package, version )
        if addInfo[ packageKey ] [ 1 ]:
            buildTarget += "-" + addInfo[ packageKey ] [ 1 ]
        regenerateFile = False
        if not buildTarget in binTargets:
            utils.warning( "key %s not contained in binary package %s" % ( buildTarget, binPackage ) )
            regenerateFile = True

        dependencies = baseDependencies
        # get buildDependencies from the source package
        runtimeDependencies, buildDependencies = portage.readChildren( category, package, version )
        binRuntimeDependencies, binBuildDependencies = portage.readChildren( binCategory, binPackage, binVersion )
        commonDependencies = dict()

        for i in runtimeDependencies:
            if i in runtimeDependencies and i in buildDependencies:
                commonDependencies[ i ] = buildDependencies[ i ]
                if not i in binRuntimeDependencies:
                    regenerateFile = True

        for key in commonDependencies:
            dependencies += "        self.runtimeDependencies[ '%s' ] = '%s'\n" % ( key, commonDependencies[ key ] )


        if regenerateFile:
            template = Template( file( KDEROOT + '/emerge/bin/binaryPackage.py.template' ).read() )
            targetkeys = binTargets.keys()
            if 'svnHEAD' in binTargets and binTargets[ 'svnHEAD' ] == False:
                targetkeys.remove( 'svnHEAD' )
            if not buildTarget in targetkeys:
                targetkeys.append( buildTarget )
            targetsString = "'" + "', '".join( targetkeys ) + "'"
            result = template.safe_substitute( { 'revision': getGitVersion( os.path.join( KDEROOT, "emerge", "portage" ) ),
                                                 'package': binPackage,
                                                 'versionTargets': targetsString,
                                                 'defaultTarget': buildTarget,
                                                 'description': description,
                                                 'dependencies': dependencies
                                               } )

            currentName = portage.getFilename( binCategory, binPackage, binVersion )
            newName = portage.getFilename( binCategory, binPackage, buildTarget )
            gitCurrentName = currentName.replace("%semerge\\" % KDEROOT ,"")
            gitNewName = newName.replace("%semerge\\" % KDEROOT ,"")

            if not doPretend:
                if not currentName == newName:
                    if not gitRename( gitCurrentName, gitNewName ):
                        utils.warning( 'failed to rename file %s' % os.path.basename( gitCurrentName ) )
                        continue

                f = file( newName, 'w+b' )
                f.write( result )
                f.close()
            else:
                utils.debug("renaming/updating file %s" % gitNewName )


        # check that all targets from the source package are contained in the binTargets
        # do we really need binaries for each and every target?
#        utils.new_line
#        for srcKey in srcTargets:
#            if not srcKey in binTargets:
#                utils.warning( "key %s not contained in binary package %s" % ( srcKey, binPackage ) )
#        utils.new_line()
#        utils.info( "working on package %s" % package )
#        utils.new_line()
    else:
        utils.warning( "no corresponding binary Package is available for %s!" % package )
        buildTarget = addInfo[ packageKey ] [ 0 ]
        if buildTarget == '':
            buildTarget = portage.PortageInstance.getDefaultTarget( category, package, version )
        regenerateFile = True

        if category == "win32libs-sources" and package.endswith("-src"):
            binCategory = "win32libs-bin"
            binPackage = package[:-4]
            binVersion = buildTarget
        else:
            continue

        dependencies = baseDependencies
        # get buildDependencies from the source package
        runtimeDependencies, buildDependencies = portage.readChildren( category, package, version )

        for key in runtimeDependencies:
            if key in runtimeDependencies and key in buildDependencies:
                dependencies += "        self.runtimeDependencies[ '%s' ] = '%s'\n" % ( key, buildDependencies[ key ] )


        if regenerateFile:
            template = Template( file( KDEROOT + '/emerge/bin/binaryPackage.py.template' ).read() )
            targetkeys = [ buildTarget ]
            targetsString = "'" + "', '".join( targetkeys ) + "'"
            result = template.safe_substitute( { 'revision': getGitVersion( os.path.join( KDEROOT, "emerge", "portage" ) ),
                                                 'package': binPackage,
                                                 'versionTargets': targetsString,
                                                 'defaultTarget': buildTarget,
                                                 'dependencies': dependencies
                                               } )

            newName = portage.getFilename( binCategory, binPackage, buildTarget )
            newDir = os.path.dirname( newName )
            gitPath = newDir.replace("%semerge\\" % KDEROOT ,"")
            gitName = newName.replace("%semerge\\" % KDEROOT ,"")
            
            if not doPretend:
                if not os.path.exists( newDir ):
                    os.makedirs( newDir )
                    if not gitAdd( gitPath ):
                        utils.warning( 'failed to add directory %s' % os.path.basename( gitPath ) )
                        continue


                f = file( newName, 'w+b' )
                f.write( result )
                f.close()


                if not gitAdd( gitName ):
                    utils.warning( 'failed to add file %s' % os.path.basename( gitName ) )
                    continue
            else:
                if not os.path.exists( newDir ):
                    print "mkdir", newDir
                    print "git add", gitPath

                print "write", newName
                print "git add", gitName
