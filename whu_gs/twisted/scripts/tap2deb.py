# -*- test-case-name: twisted.scripts.test.test_tap2deb -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
tap2deb creates Debian packages which wrap .tap files.
"""

import os
import sys
import shutil
import subprocess
import warnings
from email.utils import formatdate as now

from twisted.python import usage
from twisted.python.filepath import FilePath

warnings.warn("tap2deb is deprecated since Twisted 15.2.",
              category=DeprecationWarning, stacklevel=2)


class MyOptions(usage.Options):
    optFlags = [["unsigned", "u"]]
    optParameters = [["tapfile", "t", "twistd.tap"],
                  ["maintainer", "m", "",
                   "The maintainer's name and email in a specific format: "
                   "'John Doe <johndoe@example.com>'"],
                  ["protocol", "p", ""],
                  ["description", "e", ""],
                  ["long_description", "l", ""],
                  ["set-version", "V", "1.0"],
                  ["debfile", "d", None],
                  ["type", "y", "tap", "Type of configuration: 'tap', 'xml', "
                   "'source' or 'python' for .tac files"]]

    compData = usage.Completions(
        optActions={
            "type": usage.CompleteList(["tap", "xml", "source", "python"]),
            "debfile": usage.CompleteFiles("*.deb")}
        )

    def postOptions(self):
        if not self["maintainer"]:
            raise usage.UsageError("maintainer must be specified.")


type_dict = {
    'tap': 'file',
    'python': 'python',
    'source': 'source',
    'xml': 'xml',
}



def run(args=None):
    """
    Parses the configuration options in C{args} and runs C{dpkg-buildpackage}
    to create a .deb file.

    @param args: List of strings representing the C{tap2deb} configuration
        options.
    @type args: L{list}
    """
    try:
        config = MyOptions()
        config.parseOptions(args)
    except usage.error as ue:
        sys.exit("%s: %s" % (sys.argv[0], ue))

    tapFile = config['tapfile']
    baseTapFile = os.path.basename(config['tapfile'])
    protocol = (config['protocol'] or os.path.splitext(baseTapFile)[0])
    debFile = config['debfile'] or 'twisted-' + protocol
    version = config['set-version']
    maintainer = config['maintainer']
    description = config['description'] or (
        'A Twisted-based server for %(protocol)s' % vars())
    longDescription = config['long_description'] or\
        'Automatically created by tap2deb'
    twistdOption = type_dict[config['type']]
    date = now()
    directory = debFile + '-' + version
    pythonVersion = '%s.%s' % sys.version_info[:2]
    buildDir = FilePath('.build').child(directory)

    if buildDir.exists():
        buildDir.remove()

    debianDir = buildDir.child('debian')
    debianDir.child('source').makedirs()
    shutil.copy(tapFile, buildDir.path)

    debianDir.child('README.Debian').setContent(
    '''This package was auto-generated by tap2deb\n''')

    debianDir.child('conffiles').setContent(
    '''\
/etc/init.d/%(debFile)s
/etc/default/%(debFile)s
/etc/%(baseTapFile)s
''' % vars())

    debianDir.child('default').setContent(
    '''\
pidfile=/var/run/%(debFile)s.pid
rundir=/var/lib/%(debFile)s/
file=/etc/%(tapFile)s
logfile=/var/log/%(debFile)s.log
 ''' % vars())

    debianDir.child('init.d').setContent(
    '''\
#!/bin/sh

PATH=/sbin:/bin:/usr/sbin:/usr/bin

pidfile=/var/run/%(debFile)s.pid \
rundir=/var/lib/%(debFile)s/ \
file=/etc/%(tapFile)s \
logfile=/var/log/%(debFile)s.log

[ -r /etc/default/%(debFile)s ] && . /etc/default/%(debFile)s

test -x /usr/bin/twistd || exit 0
test -r $file || exit 0
test -r /usr/share/%(debFile)s/package-installed || exit 0


case "$1" in
    start)
        echo -n "Starting %(debFile)s: twistd"
        start-stop-daemon --start --quiet --exec /usr/bin/twistd -- \
                          --pidfile=$pidfile \
                          --rundir=$rundir \
                          --%(twistdOption)s=$file \
                          --logfile=$logfile
        echo "."
    ;;

    stop)
        echo -n "Stopping %(debFile)s: twistd"
        start-stop-daemon --stop --quiet  \
            --pidfile $pidfile
        echo "."
    ;;

    restart)
        $0 stop
        $0 start
    ;;

    force-reload)
        $0 restart
    ;;

    *)
        echo "Usage: /etc/init.d/%(debFile)s {start|stop|restart|force-reload}" >&2
        exit 1
    ;;
esac

exit 0
''' % vars())

    debianDir.child('init.d').chmod(0755)

    debianDir.child('postinst').setContent(
    '''\
#!/bin/sh
update-rc.d %(debFile)s defaults >/dev/null
invoke-rc.d %(debFile)s start
#DEBHELPER#
''' % vars())

    debianDir.child('prerm').setContent(
    '''\
#!/bin/sh
invoke-rc.d %(debFile)s stop
#DEBHELPER#
''' % vars())

    debianDir.child('postrm').setContent(
    '''\
#!/bin/sh
if [ "$1" = purge ]; then
        update-rc.d %(debFile)s remove >/dev/null
fi
#DEBHELPER#
''' % vars())

    debianDir.child('changelog').setContent(
    '''\
%(debFile)s (%(version)s) unstable; urgency=low

  * Created by tap2deb

 -- %(maintainer)s  %(date)s

''' % vars())

    debianDir.child('control').setContent(
    '''\
Source: %(debFile)s
Section: net
Priority: extra
Maintainer: %(maintainer)s
Build-Depends-Indep: debhelper, python (>= 2.6.5-7)
Standards-Version: 3.8.4
XS-Python-Version: current

Package: %(debFile)s
Architecture: all
Depends: ${python:Depends}, python-twisted-core
XB-Python-Version: ${python:Versions}
Description: %(description)s
 %(longDescription)s
''' % vars())

    debianDir.child('copyright').setContent(
    '''\
This package was auto-debianized by %(maintainer)s on
%(date)s

It was auto-generated by tap2deb

Upstream Author(s):
Moshe Zadka <moshez@twistedmatrix.com> -- tap2deb author

Copyright:

Insert copyright here.
''' % vars())

    debianDir.child('dirs').setContent(
    '''\
etc/init.d
etc/default
var/lib/%(debFile)s
usr/share/doc/%(debFile)s
usr/share/%(debFile)s
''' % vars())

    debianDir.child('rules').setContent(
    '''\
#!/usr/bin/make -f

export DH_COMPAT=5

build: build-stamp
build-stamp:
	dh_testdir
	touch build-stamp

clean:
	dh_testdir
	dh_testroot
	rm -f build-stamp install-stamp
	dh_clean

install: install-stamp
install-stamp: build-stamp
	dh_testdir
	dh_testroot
	dh_clean -k
	dh_installdirs

	# Add here commands to install the package into debian/tmp.
	cp %(baseTapFile)s debian/tmp/etc/
	cp debian/init.d debian/tmp/etc/init.d/%(debFile)s
	cp debian/default debian/tmp/etc/default/%(debFile)s
	cp debian/copyright debian/tmp/usr/share/doc/%(debFile)s/
	cp debian/README.Debian debian/tmp/usr/share/doc/%(debFile)s/
	touch debian/tmp/usr/share/%(debFile)s/package-installed
	touch install-stamp

binary-arch: build install

binary-indep: build install
	dh_testdir
	dh_testroot
	dh_strip
	dh_compress
	dh_installchangelogs
	dh_python2
	dh_fixperms
	dh_installdeb
	dh_gencontrol
	dh_md5sums
	dh_builddeb

source diff:
	@echo >&2 'source and diff are obsolete - use dpkg-source -b'; false

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install
''' % vars())

    debianDir.child('rules').chmod(0755)

    args = ["dpkg-buildpackage", "-rfakeroot"]
    if config['unsigned']:
        args = args + ['-uc', '-us']

    # Build deb
    job = subprocess.Popen(args, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, cwd=buildDir.path)
    stdout, _ = job.communicate()
