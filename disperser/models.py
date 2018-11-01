import git
import os
from django.db import models

# Create your models here.
class GitHub(object):
    def __init__(self, url, path):
        self.__url = url
        self.__path = path
        self.__repo = None
    
    def __pull(self, branch):
        repo = git.Repo(self.__path)
        repo.remotes.origin.pull(refspec=branch + ':' + branch)
        return repo

    def __clone(self, branch):
        repo = git.Repo.clone_from(
            self.__url,
            self.__path,
            branch=branch
        )
        return repo
    
    def pull(self, branch='master'):
        try:
            if not os.path.isdir(self.__path):
                print('Clone playbooks from main repo')
                self.__repo = self.__clone(branch)
            else:
                print('Pull playbooks from main repo')
                self.__repo = self.__pull(branch)

        except git.exc.GitCommandError as err:
            print('Traceback: %s' % err.args)
    
    def add(self, file):
        self.__repo.index.add([file]) 
        self.__repo.index.commit("Added file %s." % file)
    
    def push(self):
        self.__repo.git.push()
        

