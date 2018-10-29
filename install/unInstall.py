import sys
import subprocess
import shutil
import installLog as logging
import argparse
import os
import shlex
import socket
import install


#distros
centos=0
ubuntu=1
distro = install.get_distro()

class unInstallCyberPanel:

    def fixResolvConf(self):
        if distro == centos:
            return

        if os.access('/etc/resolv.conf', os.F_OK):
            return

        try:
            f = open('/etc/resolv.conf', 'w')
            f.write('nameserver 8.8.8.8')
            f.close()
        except IOError as e:
            print "Unable to create /etc/resolv.conf: " + str(e) + \
                  ".  This may need to be fixed manually as 'echo \"nameserver 8.8.8.8\"> " \
                  "/etc/resolv.conf'"

    def unInstallCyberPanelRepo(self):

        if distro == centos:
            try:
                copyPath = "/etc/yum.repos.d/cyberpanel.repo"
                os.remove(copyPath)

            except OSError,msg:
                logging.InstallLog.writeToFile(str(msg)+ " [unInstallCyberPanelRepo]")

    def removeGunicorn(self):
        try:

            os.chdir(self.cwd)

            service = "/etc/systemd/system/gunicorn.service"
            socket = "/etc/systemd/system/gunicorn.socket"
            conf = "/etc/tmpfiles.d/gunicorn.conf"

            os.remove(service)
            os.remove(socket)
            os.remove(conf)


        except BaseException, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeGunicorn]")

    def removePostfixDovecot(self):
        try:

            if distro == centos:
                command = 'yum -y remove postfix'
            else:
                command = 'apt-get -y remove postfix'

            cmd = shlex.split(command)

            res = subprocess.call(cmd)

            shutil.rmtree("/etc/postfix")
            shutil.rmtree("etc/dovecot")


        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePostfixDovecot]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePostfixDovecot]")
            return 0

        return 1

    def removeMysql(self):
        try:

            if distro == centos:
                command = 'yum -y remove mariadb mariadb-server'
            else:
                command = 'apt-get -y remove mariadb-server'

            cmd = shlex.split(command)

            res = subprocess.call(cmd)

            shutil.rmtree("/var/lib/mysql")
            os.remove("/etc/my.cnf")


        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeMysql]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeMysql]")
            return 0

        return 1

    def removeLiteSpeed(self):
        try:

            if distro == centos:
                command = 'yum -y remove openlitespeed'
            else:
                command = 'apt-get -y remove openlitespeed'

            cmd = shlex.split(command)

            res = subprocess.call(cmd)

            shutil.rmtree("/usr/local/lsws")

        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeLiteSpeed]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeLiteSpeed]")
            return 0
        return 1

    def removeCyberPanel(self):
        try:

           shutil.rmtree("/usr/local/CyberCP")
           os.remove("/usr/local/CyberCP2.tar.gz")
           shutil.rmtree("/etc/cyberpanel")

        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeCyberPanel]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removeCyberPanel]")
            return 0
        return 1

    def removePureFTPD(self):
        try:

            if distro == centos:
                command = 'yum -y remove pure-ftpd'
            else:
                command = 'apt-get -y remove pure-ftpd'

            cmd = shlex.split(command)

            res = subprocess.call(cmd)

            shutil.rmtree("/etc/pure-ftpd")

        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePureFTPD]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePureFTPD]")
            return 0
        return 1

    def removePowerDNS(self):
        try:
            if distro == centos:
                command = 'yum -y remove pdns'
            else:
                command = 'apt-get -y remove pdns-server'

            cmd = shlex.split(command)

            res = subprocess.call(cmd)

            shutil.rmtree("/etc/pdns")

        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePowerDNS]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePowerDNS]")
            return 0
        return 1

    def removePHP(self):
        try:

            if distro == centos:
                command = 'yum -y remove lsphp*'
            else:
                command = 'apt-get -y remove lsphp*'

            cmd = shlex.split(command)

            res = subprocess.call(cmd)

            shutil.rmtree("/etc/pdns")

        except OSError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePHP]")
            return 0
        except ValueError, msg:
            logging.InstallLog.writeToFile(str(msg) + " [removePHP]")
            return 0
        return 1



def Main():

    remove = unInstallCyberPanel()

    remove.fixResolvConf()
    remove.removeLiteSpeed()
    remove.removeMysql()
    remove.removePostfixDovecot()
    remove.removePureFTPD()
    remove.removeCyberPanel()
    remove.removeGunicorn()
    remove.unInstallCyberPanelRepo()
    remove.removePowerDNS()
    remove.removePHP()

    print("##########################################")
    print("         Successfully Uninstalled         ")
    print("##########################################")



Main()