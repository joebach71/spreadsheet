from svn import local, remote
from subprocess import Popen, PIPE
import re
from os import path
from languagestrings.settings import DEFAULT_REPO_WORKDIR,\
                                     DEFAULT_REPO_REPODIR, DEFAULT_REPO_PROTOCOL

# Create your models here.
class SVNManager(object):
    changelist = ''
    product = ''
    category = ""
    message = ''
    result = []
    status = ''
    revision = None
    def __init__(self, repo=None, changelist='', product="", category=""):
        self.repo = repo
        self.product = product
        self.category = category
        self.changelist = changelist
        self.status = 'Initialized'
        self.result.append(self.status)
        
        cmd = ['svn', 'info']
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        output = []
        if (err):
            output = ''.join(err)
        else:
            output = ''.join(out)
        
        for line in output.split("\n"):
            m = re.match(r"Revision: (\d+)", line)
            if m:            
                self.revision = m.group(1)
        pass
    
    def __unicode__(self):
        return "{0}_{1}".format(self.status, self.repo)
    def set_changelist(self, name):
        self.changelist = name
        return self
    def get_changelist(self):
        return self.changelist
    def commit(self, message='Default Message'):
        self.message = message
        cmd = ['svn', 'commit', '-m', message, self.repo.workdir]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        
        output = []
        if (err):
            print ''.join(err)
            output = self.output("commit failed", err)
        else:
            print ''.join(out)
            self.set_revision(out)
            output = self.output("committed", out)
        
#         workingfiles = path.join(self.repo.workdir, self.product, self.category+'_*.json')
        cmd = ['svn', 'changelist', '--remove', '--changelist', self.changelist, '--depth', 'infinity', self.repo.workdir]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if (err):
            print ''.join(err)
            self.output("failed remove changelist", err)
        else:
            print ''.join(out)
            self.output("cleaned changelist", out)
        return output
        pass
    def commit_changelist(self, message='Default Message'):
        self.message = message
        cmd = ['svn', 'commit', '-m', self.message, '--changelist', self.changelist, self.repo.workdir]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        output = ""
        if (err):
            print ''.join(err)
            output = self.output("commit failed", err)
        else:
            print ''.join(out)
            self.set_revision(out)
            output = self.output("committed", out)
        # Remove any unchange file revert from changelist
        cmd = ['svn', 'changelist', '--remove', '--changelist', self.changelist, '--depth', 'infinity', self.repo.workdir]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if (err):
            print ''.join(err)
            self.output("cleaned changelist", err)
        else:
            print ''.join(out)
            self.output("cleaned changelist", out)
        return output
    def set_revision(self, output):
        out = ''.join(output)
        match = re.search(r"Committed revision (\d+).", out)
        if (match):
            self.revision = match.group(1)
        return self.revision
    def add_to_changelist(self, filename):
        # check to see if this is a new file
        cmd = ['svn', 'status', filename]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        output = ""
        if (err):
            output = ''.join(err)
        else:
            output = ''.join(out)
        
        m = re.match('\?', output)
        if m:
            self.add(filename)
        
        if not self.changelist:
            self.changelist = "default"
        cmd = ['svn', 'changelist', self.changelist, filename]
#         print cmd
        p = Popen(cmd, cwd=self.repo.workdir, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if (err):
            return self.output("FAILED add a file to changelist, "+self.changelist, err)
        else:
            return self.output('added a file to changelist, '+self.changelist, out)
        pass
        
    def add(self, filename):
#         print file
        cmd = ['svn', 'add', filename]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if (err):
            return self.output("FAILED add a file ", err)
        else:
            return self.output('added a file ', out)
        pass
    def remove(self, filename):
        if not self.changelist:
            self.changelist = "default"
        cmd = ['svn', 'changelist', self.changelist, '--remove', filename]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if (err):
            return self.output('FAILED remove a file to '+self.changelist, err)
        else:
            return self.output('removed a file to '+self.changelist, out)
        pass
    def diff(self):
        if not self.revision:
            print "No Revision found for this SVNManager"+str(self)
            return self.result
        cmd = ['svn', 'diff', '-c', str(self.revision), self.repo.workdir]
        print cmd
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        if (err):
            self.output('FAILED diff for revision '+str(self.revision), err)
        else:
            self.output('Diff on revision '+str(self.revision), out)
            pass
        output = ''.join(out)
        print output
        # remove repo workdir
        #re.sub(self.repo.workdir, '', output)
        return re.sub(self.repo.workdir, '', output)
    def output(self, status, message):
        self.result.append(''.join(message))
        self.status = status
        return self.result
        
'''
This should not be model object but regular object
'''
PROTOCOLS = (
    ('F', 'file'),
    ('H', 'http'),
    ('T', 'https'),
    ('S', 'svn'),
    ('O', 'svn+ssh')
)
                                     
class Repo(object):
    '''
        Defines Repository
    '''
    protocol = []
    workdir = ""
    repodir = ""
    def __init__(self, protocol=DEFAULT_REPO_PROTOCOL, workdir=DEFAULT_REPO_WORKDIR, repodir=DEFAULT_REPO_REPODIR):
        self.protocol = protocol
        self.workdir = workdir
        self.repodir = repodir
    def __unicode__(self):
        return "Repo {0} at WORKDIR - {1}".format(self.repodir, self.workdir)
    def checkout(self):
        r = remote.RemotClient('{0}://{1}'.format(self.protocol, self.repodir))
        r.checkout(self.workdir)
        return r
    def info(self):
        r = local.LocalClient(self.workdir)
        return r.info()
    def add(self, *args):
        return self
    def logs(self):
        logs = local.LocalClient(self.workdir)
        return logs
    def revision(self):
        pass
