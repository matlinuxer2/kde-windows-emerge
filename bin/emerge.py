# -*- coding: utf-8 -*-
# this will emerge some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>

import sys
import os
import utils
import portage
import emergePlatform
import shutil
from InstallDB import *



def usage():
    print """
Usage:
    emerge [[ command and flags ] [ singletarget ]
            [ command and flags ] [ singletarget ]
            ... ]

    where singletarget can be of the form:
        category
        package
        category/package

Emerge is a tool for building KDE-related software under Windows. emerge
automates it, looks for the dependencies and fetches them automatically.
Some options should be used with extreme caution since they will
make your kde installation unusable in 999 out of 1000 cases.

Commands (no packagename needed - will be ignored when given):

--print-installed               This will show a list of all packages that
                                are installed currently. It queries both
                                databases (etc\portage\installed) and the
                                manifest directory - it prints out only those
                                packages that are contained within
                                --print-installable
--print-installable             This will give you a list of packages that can
                                be installed. Currently you don't need to
                                enter the category and package: only the
                                package will be enough.
--update-all                    this option tries to update all installed
                                packages that contain one or multiple svn
                                targets. This is equivalent to running all
                                those packages with the flag --update.

Commands (must have a packagename):

--print-targets         This will print all the different targets one package
                        can contain: different releases might have different
                        tags that are build as targets of a package. As an
                        example: You could build the latest amarok sources with
                        the target 'svnHEAD' the previous '1.80' release would
                        be contained as target '1.80'.
--print-revision        This will print the revision that the source repository
                        of this package currently has or nothing if there is no
                        repository.
--fetch                 retrieve package sources (also checkout sources from
                        svn or git).
--unpack                unpack package sources and make up the build directory.
--compile               compile the sources: this includes
                        configure'ing/cmake'ing and running [mingw32-|n|]make.
--configure             configure the sources (support is package specific)
--make                  run [mingw32-|n|]make (support is package specific)
--install               This will run [mingw32-|n|]make install into the image
                        directory of each package.
--manifest              This step creates the files contained in the manifest
                        dir.
--qmerge                This will merge the image directory into the KDEROOT
--test                  This will run the unittests if they are present
--package               This step will create a package out of the image
                        directory instead of merge'ing the image directory into
                        the KDEROOT (Requires the packager to be installed
                        already.)
--full-package          This will create packages instead of installing stuff
                        to KDEROOT
--install-deps          This will fetch and install all required dependencies
                        for the specified package
--unmerge               this uninstalls a package from KDEROOT - it requires a
                        working manifest directory. unmerge only delete
                        unmodified files by default. You may use the -f or
                        --force option to let unmerge delete all files
                        unconditional.
--cleanallbuilds        Clean complete build directory.
--cleanbuild            Clean build directory for the specified package. This
                        cleans also all the image directories of all targets of
                        the specified package.
--checkdigest           Check digest for the specified package. If no digest is
                        available calculate and print digests.
--cleanimage            Clean image directory for the specified package and
                        target.
--createpatch           Create source patch file for the specific package based
                        on the original archive file or checkout revision of
                        the used software revision control system.
--disable-buildhost     This disables the building for the host.
--disable-buildtarget   This disables the building for the target.

Flags:

--buildtype=[BUILDTYPE]         This will override the build type set by the
                                environment option EMERGE_BUILDTYPE .
                                Please set it to one out of Release, Debug,
                                RelWithDebInfo, MinSizeRel
--target=[TARGET]               This will override the build of the default
                                target. The default Target is marked with a
                                star in the printout of --print-targets
--options=<OPTIONS>             Set emerge property from string <OPTIONS>.
                                An example for is "cmake.openIDE=1"; 
                                see options.py for more informations.
--patchlevel=[PATCHLEVEL]       This will add a patch level when used together
                                with --package
--log-dir=[LOG_DIR]             This will log the build output to a logfile in
                                LOG_DIR for each package. Logging information
                                is appended to existing logs.

-i          ignore install: using this option will install a package over an
            existing install. This can be useful if you want to check some
            new code and your last build isn't that old.
-p
--probe     probing: emerge will only look which files it has to build
            according to the list of installed files and according to the
            dependencies of the package.
-q          quiet: there should be no output - The verbose level should be 0
-t          test: if used on an KDE target it will override the environment
            variable and build the target with -DKDE_BUILD_TESTS=ON
-v          verbose: increases the verbose level of emerge. Default is 1.
            verbose level 1 contains some notes from emerge, all output of
            cmake, make and other programs that are used. verbose level 2
            adds an option VERBOSE=1 to make and emerge is more verbose
            highest level is verbose level 3.
-z          if packages from version control system sources are installed,
            it marks them as out of date and rebuilds them (tags are not
            marked as out of date).
-sz         similar to -z, only that it acts only on the last package, and
            works as normal on the rest.
--noclean   this option will try to use an existing build directory. Please
            handle this option with care - it will possibly break if the
            directory isn't existing.
--nocopy    this option is deprecated. In older releases emerge would have
            copied everything from the SVN source tree to a source directory
            under %KDEROOT%\\tmp - currently nocopy is applied by default if
            EMERGE_NOCOPY is not set to "False". Be aware that setting
            EMERGE_NOCOPY to "False" might slow down the build process,
            irritate you and increase the disk space roughly by the size of
            SVN source tree.
--offline   do not try to connect to the internet: KDE packages will try to
            use an existing source tree and other packages would try to use
            existing packages in the download directory. If that doesn't
            work, the build will fail.
--update    this option is the same as '-i --noclean'. It will update a single
            package that is already installed.
--cleanup   Clean your portage directory, to prevent emerge errors, removes
            empty directories and *.pyc files

Internal options or options that aren't fully implemented yet:
PLEASE DO NOT USE!
--version-dir
--version-package

More information see the README or http://windows.kde.org/.
Send feedback to <kde-windows@kde.org>.

"""

@utils.log
def doExec( category, package, version, action, opts ):
    utils.startTimer("%s for %s" % ( action,package),1)
    utils.debug( "emerge doExec called. action: %s opts: %s" % (action, opts), 2 )
    fileName = portage.getFilename( category, package, version )
    opts_string = ( "%s " * len( opts ) ) % tuple( opts )
    commandstring = "python %s %s %s" % ( fileName, action, opts_string )

    utils.debug( "file: " + fileName, 1 )
    try:
        #Switched to import the packages only, because otherwise degugging is very hard, if it troubles switch back
        #makes touble for xcompile -> changed back
        if not utils.system( commandstring ):
            utils.die( "running %s" % commandstring )
        #mod = portage.__import__( fileName )
        #mod.Package().execute(action)
    except OSError:
        utils.stopTimer("%s for %s" % ( action,package))
        return False
    utils.stopTimer("%s for %s" % ( action,package))
    return True

def handlePackage( category, package, version, buildAction, opts ):
    utils.debug( "emerge handlePackage called: %s %s %s %s" % (category, package, version, buildAction), 2 )
    success = True

    if continueFlag:
        actionList = ['fetch', 'unpack', 'configure', 'make', 'cleanimage', 'install', 'manifest', 'qmerge']
        
        found = None
        for action in actionList: 
            if not found and action != buildAction:
                continue
            found = True
            success = success and doExec( category, package, version, action, opts )
    elif ( buildAction == "all" or buildAction == "full-package" ):
        os.putenv( "EMERGE_BUILD_STEP", "" )
        success = doExec( category, package, version, "fetch", opts )
        success = success and doExec( category, package, version, "unpack", opts )
        if emergePlatform.isCrossCompilingEnabled():
            if not disableHostBuild:
                os.putenv( "EMERGE_BUILD_STEP", "host" )
                success = success and doExec( category, package, version, "compile", opts )
                success = success and doExec( category, package, version, "cleanimage", opts )
                success = success and doExec( category, package, version, "install", opts )
                if ( buildAction == "all" ):
                    success = success and doExec( category, package, version, "manifest", opts )
                if ( buildAction == "all" ):
                    success = success and doExec( category, package, version, "qmerge", opts )
                if( buildAction == "full-package" ):
                    success = success and doExec( category, package, version, "package", opts )
            if disableTargetBuild:
                return success
            os.putenv( "EMERGE_BUILD_STEP", "target" )

        success = success and doExec( category, package, version, "compile", opts )
        success = success and doExec( category, package, version, "cleanimage", opts )
        success = success and doExec( category, package, version, "install", opts )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "manifest", opts )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "qmerge", opts )
        if( buildAction == "full-package" ):
            success = success and doExec( category, package, version, "package", opts )

    elif ( buildAction in [ "fetch", "unpack", "preconfigure", "configure", "compile", "make", "qmerge", "checkdigest", "dumpdeps",
                            "package", "manifest", "unmerge", "test", "cleanimage", "cleanbuild", "createpatch", "geturls",
                            "printrev"] and category and package and version ):
        os.putenv( "EMERGE_BUILD_STEP", "" )
        success = True
        if emergePlatform.isCrossCompilingEnabled():
            if not disableHostBuild:
                os.putenv( "EMERGE_BUILD_STEP", "host" )
                success = doExec( category, package, version, buildAction, opts )
            if disableTargetBuild:
                return success
            os.putenv( "EMERGE_BUILD_STEP", "target" )
        success = success and doExec( category, package, version, buildAction, opts )
    elif ( buildAction == "install" ):
        os.putenv( "EMERGE_BUILD_STEP", "" )
        success = True
        if emergePlatform.isCrossCompilingEnabled():
            if not disableHostBuild:
                os.putenv( "EMERGE_BUILD_STEP", "host" )
                success = doExec( category, package, version, "cleanimage", opts )
                success = success and doExec( category, package, version, "install", opts )
            if disableTargetBuild:
                return success
            os.putenv( "EMERGE_BUILD_STEP", "target" )
        success = success and doExec( category, package, version, "cleanimage", opts )
        success = success and doExec( category, package, version, "install", opts )
    elif ( buildAction == "version-dir" ):
        print "%s-%s" % ( package, version )
        success = True
    elif ( buildAction == "version-package" ):
        print "%s-%s-%s" % ( package, os.getenv( "KDECOMPILER" ), version )
        success = True
    elif ( buildAction == "print-installable" ):
        portage.printInstallables()
        success = True
    elif ( buildAction == "print-installed" ):
        if isDBEnabled():
            printInstalled()
        else:
            portage.printInstalled()
        success = True
    elif ( buildAction == "print-targets" ):
        portage.printTargets( category, package, version )
        success = True
    elif ( buildAction == "install-deps" ):
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success

#
# "main" action starts here
#

# TODO: all the rest should go into main(). But here I am not
# sure - maybe some of those variables are actually MEANT to
# be used in other modules. Put this back for now

# but as a temporary solution rename variables to mainXXX
# where it is safe so there are less redefinitions in inner scopes

utils.startTimer("Emerge")
mainBuildAction = "all"
packageName = None
doPretend = False
outDateVCS = False
outDatePackage = False
stayQuiet = False
disableHostBuild = False
disableTargetBuild = False
ignoreInstalled = False
updateAll = False
continueFlag = False

if len( sys.argv ) < 2:
    usage()
    utils.die("")

environ = dict() # TODO: why do we need this at all?
environ["EMERGE_TRACE"]         = os.getenv( "EMERGE_TRACE" )
environ["EMERGE_BUILDTESTS"]    = os.getenv( "EMERGE_BUILDTESTS" )
environ["EMERGE_OFFLINE"]       = os.getenv( "EMERGE_OFFLINE" )
environ["EMERGE_FORCED"]        = os.getenv( "EMERGE_FORCED" )
environ["EMERGE_VERSION"]       = os.getenv( "EMERGE_VERSION" )
environ["EMERGE_BUILDTYPE"]     = os.getenv( "EMERGE_BUILDTYPE" )
environ["EMERGE_TARGET"]        = os.getenv( "EMERGE_TARGET" )
environ["EMERGE_PKGPATCHLVL"]        = os.getenv( "EMERGE_PKGPATCHLVL" )
environ["EMERGE_LOG_DIR"]       = os.getenv( "EMERGE_LOG_DIR" )

if environ['EMERGE_TRACE'] == None or not environ['EMERGE_TRACE'].isdigit():
    trace = 0
    os.environ["EMERGE_TRACE"] = str( trace )
else:
    trace = int( environ[ "EMERGE_TRACE" ] )

mainOpts = list()

executableName = sys.argv.pop( 0 )
nextArguments = sys.argv[:]

for i in sys.argv:
    nextArguments.pop(0)
    if ( i == "-p" or i == "--probe" ):
        doPretend = True
    elif ( i.startswith("--options=") ):
        # @todo how to add -o <parameter> option
        options = i.replace( "--options=", "" )
        if "EMERGE_OPTIONS" in os.environ:
            os.environ["EMERGE_OPTIONS"] += " %s" % options
        else:
            os.environ["EMERGE_OPTIONS"] = options
    elif ( i == "-z" ):
        outDateVCS = True
    elif ( i == "-sz" ):
        outDatePackage = True
    elif ( i == "-q" ):
        stayQuiet = True
    elif ( i == "-t" ):
        os.environ["EMERGE_BUILDTESTS"] = "True"
    elif i == "-c" or i == "--continue":
        continueFlag = True
    elif ( i == "--offline" ):
        mainOpts.append( "--offline" )
        os.environ["EMERGE_OFFLINE"] = "True"
    elif ( i == "-f" or i == "--force" ):
        os.environ["EMERGE_FORCED"] = "True"
    elif ( i.startswith( "--buildtype=" ) ):
        os.environ["EMERGE_BUILDTYPE"] = i.replace( "--buildtype=", "" )
    elif ( i.startswith( "--target=" ) ):
        os.environ["EMERGE_TARGET"] = i.replace( "--target=", "" )
    elif ( i.startswith( "--patchlevel=" ) ):
        os.environ["EMERGE_PKGPATCHLVL"] = i.replace( "--patchlevel=", "" )
    elif ( i.startswith( "--log-dir=" ) ):
        os.environ["EMERGE_LOG_DIR"] = i.replace( "--log-dir=", "" )
    elif ( i == "-v" ):
        utils.Verbose.increase()
    elif ( i == "--trace" ):
        trace = trace + 1
        os.environ["EMERGE_TRACE"] = str( trace )
    elif ( i == "--nocopy" ):
        os.environ["EMERGE_NOCOPY"] = str( True )
    elif ( i == "--noclean" ):
        os.environ["EMERGE_NOCLEAN"] = str( True )
    elif ( i == "--clean" ):
        os.environ["EMERGE_NOCLEAN"] = str( False )
    elif ( i in [ "--version-dir", "--version-package", "--print-installable",
                  "--print-installed", "--print-targets" ] ):
        mainBuildAction = i[2:]
        stayQuiet = True
        if i in [ "--print-installable", "--print-installed" ]:
            break
    elif ( i == "-i" ):
        ignoreInstalled = True
    elif ( i == "--update" ):
        ignoreInstalled = True
        os.environ["EMERGE_NOCLEAN"] = str( True )
    elif ( i == "--update-all" ):
        ignoreInstalled = True
        os.environ["EMERGE_NOCLEAN"] = str( True )
        updateAll = True
    elif ( i == "--install-deps" ):
        ignoreInstalled = True
        mainBuildAction = "install-deps"
    elif ( i in [ "--fetch", "--unpack", "--preconfigure", "--configure", "--compile", "--make",
                  "--install", "--qmerge", "--manifest", "--package", "--unmerge", "--test", "--checkdigest", "--dumpdeps",
                  "--full-package", "--cleanimage", "--cleanbuild", "--createpatch", "--geturls"] ):
        mainBuildAction = i[2:]
    elif ( i == "--print-revision" ):
        mainBuildAction = "printrev"
        stayQuiet = True
    elif ( i == "--disable-buildhost" ):
        disableHostBuild = True
    elif ( i == "--disable-buildtarget" ):
        disableTargetBuild = True
    elif( i == "--cleanup" ):
        utils.debug("Starting to clean emerge" )
        utils.system("cd %s && git clean -f -x -e *.py -e *.diff -e *.ba\\t -e *.cmd -e *.reg" % os.path.join(os.getenv("KDEROOT"),"emerge") )
        exit(0)
    elif( i == "--cleanup-dry" ):
        utils.debug("Starting to clean emerge" )
        utils.system("cd %s && git clean --dry-run -x -e *.py -e *.diff -e *.ba\\t -e *.cmd -e *.reg" % os.path.join(os.getenv("KDEROOT"),"emerge") )
        exit(0)
    elif i == "--cleanallbuilds":
        # clean complete build directory
        utils.cleanDirectory(os.path.join( os.getenv("KDEROOT"), "build"))
        exit(0)
    elif ( i.startswith( "-" ) ):
        usage()
        exit ( 1 )
    else:
        packageName = i
        break

if stayQuiet == True:
    utils.setVerbose(0)

# get KDEROOT from env
KDEROOT = os.getenv( "KDEROOT" )
utils.debug( "buildAction: %s" % mainBuildAction )
utils.debug( "doPretend: %s" % doPretend, 1 )
utils.debug( "packageName: %s" % packageName )
utils.debug( "buildType: %s" % os.getenv( "EMERGE_BUILDTYPE" ) )
utils.debug( "buildTests: %s" % utils.envAsBool( "EMERGE_BUILDTESTS" ) )
utils.debug( "verbose: %d" % utils.verbose(), 1 )
utils.debug( "trace: %s" % os.getenv( "EMERGE_TRACE" ), 1 )
utils.debug( "KDEROOT: %s\n" % KDEROOT, 1 )
utils.debug_line()

def unset_var( varname ):
    if not os.getenv( varname ) == None:
        print
        utils.warning( "%s found as environment variable. you cannot override emerge"\
                       " with this - unsetting %s locally" % ( varname, varname ) )
        os.environ[ varname ] = ""

unset_var( "CMAKE_INCLUDE_PATH" )
unset_var( "CMAKE_LIBRARY_PATH" )
unset_var( "CMAKE_FIND_PREFIX" )
unset_var( "CMAKE_INSTALL_PREFIX" )

# adding emerge/bin to find base.py and gnuwin32.py etc.
os.environ["PYTHONPATH"] = os.getenv( "PYTHONPATH", "" ) + os.pathsep + \
                           os.path.join( os.getcwd(), os.path.dirname( executableName ) )
sys.path.append( os.path.join( os.getcwd(), os.path.dirname( executableName ) ) )

_deplist = []
deplist = []
packageList = []
categoryList = []


buildType = os.getenv("EMERGE_BUILDTYPE")
if "EMERGE_DEFAULTCATEGORY" in os.environ:
    defaultCategory = os.environ["EMERGE_DEFAULTCATEGORY"]
else:
    defaultCategory = "kde"

if updateAll:
    installedPackages = portage.PortageInstance.getInstallables()
    if portage.PortageInstance.isCategory( packageName ):
        utils.debug( "Updating installed packages from category " + packageName, 1 )
    else:
        utils.debug( "Updating all installed packages", 1 )
    packageList = []
    for mainCategory, mainPackage, mainVersion in installedPackages:
        if portage.PortageInstance.isCategory( packageName ) and ( mainCategory != packageName ):
            continue
        if portage.isInstalled( mainCategory, mainPackage, mainVersion, buildType ) \
                and portage.isPackageUpdateable( mainCategory, mainPackage, mainVersion ):
            categoryList.append( mainCategory )
            packageList.append( mainPackage )
    utils.debug( "Will update packages: " + str (packageList), 1 )
elif packageName:
    packageList, categoryList = portage.getPackagesCategories(packageName)

for entry in packageList:
    utils.debug( "%s" % entry, 1 )
utils.debug_line( 1 )

for mainCategory, entry in zip (categoryList, packageList):
    _deplist = portage.solveDependencies( mainCategory, entry, "", _deplist )

deplist = [p.ident() for p in _deplist]

for item in range( len( deplist ) ):
    if deplist[ item ][ 0 ] in categoryList and deplist[ item ][ 1 ] in packageList:
        deplist[ item ].append( ignoreInstalled )
    else:
        deplist[ item ].append( False )

    utils.debug( "dependency: %s" % deplist[ item ], 1 )

#for item in deplist:
#    cat = item[ 0 ]
#    pac = item[ 1 ]
#    ver = item[ 2 ]

#    if portage.isInstalled( cat, pac, ver, buildType) and updateAll and not portage.isPackageUpdateable( cat, pac, ver ):
#        print "remove:", cat, pac, ver
#        deplist.remove( item )

if mainBuildAction == "install-deps":
    # the first dependency is the package itself - ignore it
    # TODO: why are we our own dependency?
    del deplist[ 0 ]

deplist.reverse()

# package[0] -> category
# package[1] -> package
# package[2] -> version

if ( mainBuildAction != "all" and mainBuildAction != "install-deps" ):
    # if a buildAction is given, then do not try to build dependencies
    # and do the action although the package might already be installed.
    # This is still a bit problematic since packageName might not be a valid
    # package

    if packageName and len( deplist ) >= 1:
        mainCategory, mainPackage, mainVersion, tag, ignoreInstalled = deplist[ -1 ]
    else:
        mainCategory, mainPackage, mainVersion = None, None, None

    if not handlePackage( mainCategory, mainPackage, mainVersion, mainBuildAction, mainOpts ):
        exit(1)

else:
    for mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled in deplist:
        target = ""
        targetList = []
        isLastPackage = [mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled] == deplist[-1]
        if outDateVCS or (outDatePackage and isLastPackage):
            target = os.getenv( "EMERGE_TARGET" )
            if not target or target not in portage.PortageInstance.getAllTargets( mainCategory, mainPackage, mainVersion ).keys():
                # if no target or a wrong one is defined, simply set the default target here
                target = defaultTarget
            targetList = portage.PortageInstance.getUpdatableVCSTargets( mainCategory, mainPackage, mainVersion )
        if isDBEnabled():
            if emergePlatform.isCrossCompilingEnabled():
                hostEnabled = portage.isHostBuildEnabled( mainCategory, mainPackage, mainVersion )
                targetEnabled = portage.isTargetBuildEnabled( mainCategory, mainPackage, mainVersion )
                hostInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
                targetInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                isInstalled = ( not hostEnabled or hostInstalled ) and ( not targetEnabled or targetInstalled )
            else:
                isInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
        else:
            isInstalled = portage.isInstalled( mainCategory, mainPackage, mainVersion, buildType )
        if ( isInstalled and not ignoreInstalled ) and not (
                        isInstalled and (outDateVCS  or (outDatePackage and isLastPackage) ) and target in targetList ):
            if utils.verbose() > 1 and mainPackage == packageName:
                utils.warning( "already installed %s/%s-%s" % ( mainCategory, mainPackage, mainVersion ) )
            elif utils.verbose() > 2 and not mainPackage == packageName:
                utils.warning( "already installed %s/%s-%s" % ( mainCategory, mainPackage, mainVersion ) )
        else:
            # find the installed version of the package
            if isDBEnabled():
                instver = installdb.findInstalled( mainCategory, mainPackage )
            else:
                instver = portage.findInstalled( mainCategory, mainPackage )

            # in case we only want to see which packages are still to be build, simply return the package name
            if ( doPretend ):
                if utils.verbose() > 0:
                    msg = " "
                    if emergePlatform.isCrossCompilingEnabled():
                        if isDBEnabled():
                            hostEnabled = portage.isHostBuildEnabled( mainCategory, mainPackage, mainVersion )
                            targetEnabled = portage.isTargetBuildEnabled( mainCategory, mainPackage, mainVersion )
                            hostInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
                            targetInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                            msg += portage.getHostAndTarget( hostEnabled and not hostInstalled, targetEnabled and not targetInstalled )
                        else:
                            msg = ""
                    utils.warning( "pretending %s/%s-%s%s" % ( mainCategory, mainPackage, mainVersion, msg ) )
            else:
                mainAction = mainBuildAction
                if mainBuildAction == "install-deps":
                    mainAction = "all"

                if not handlePackage( mainCategory, mainPackage, mainVersion, mainAction, mainOpts ):
                    utils.error( "fatal error: package %s/%s-%s %s failed" % \
                        ( mainCategory, mainPackage, mainVersion, mainBuildAction ) )
                    exit( 1 )

utils.new_line()
if len( nextArguments ) > 0:
    command = "\"" + sys.executable + "\" -u " + executableName + " " + " ".join( nextArguments )

    #for element in environ.keys():
    #    if environ[ element ]:
    #        os.environ[ element ] = environ[ element ]
    #    elif element == "EMERGE_VERBOSE":
    #        os.environ[ element ] = "1"
    #    else:
    #        os.environ[ element ] = ""
    if not utils.system(command):
        utils.die( "cannot execute next commands cmd: %s" % command )

utils.stopTimer("Emerge")

