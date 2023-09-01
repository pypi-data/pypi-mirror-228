import sys
import os
import argparse
from pathlib import Path
from glob import glob

from . import version

class Options:
    """Argument for Docker-ENV.
    """
    def __init__(self, key=None):
        if key is None:
            self.all_option()
        elif key == 'name':
            self.name_option()

    def all_option(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-g', '--gpus', default='all', type=str,
                            help='[ all | 0 | 0,1,2,3,4 ]')
        parser.add_argument('-w', '--workspace', default='~/Lion', type=str,
                            help='server workspace - code')
        parser.add_argument('-p', '--port', default=None, type=int,
                            help='port number')
        parser.add_argument('-i', '--image', default=f'lionrocket/lr_vision:{version.IMG_VERSION}', type=str,
                            help='docker image')
        parser.add_argument('-n', '--name', default='noname', type=str,
                            help='docker name')
        parser.add_argument('-r', '--rm', action='store_true',
                            help='docker --rm option')
        parser.add_argument('-f', '--dockerfile', default=None, type=str,
                            help='docker file')
        self.opt, unknownopt = parser.parse_known_args()
        def get_remain_opt(unknownopt):
            remain_opt = []
            arg = None
            for i in unknownopt:
                if ' ' in i:
                    i = f"\'{i}'"
                if arg is not None and isinstance(i, str):
                    remain_opt.append(arg + ' ' +  i)
                    arg = None
                if i.startswith('-'):
                    arg = i
                else: 
                    arg = None
            return remain_opt
        def get_name_opt(unknownopt):
            if unknownopt:
                if unknownopt[0].startswith('-'):
                    return self.opt.name, unknownopt
                else:
                    return unknownopt.pop(0), unknownopt
            return self.opt.name, unknownopt
        self.opt.name, unknownopt = get_name_opt(unknownopt)
        self.opt.remain_opt = get_remain_opt(unknownopt)
        self.opt.workspace_docker = f'/{Path(self.opt.workspace).stem}'
        self.opt.datas = glob('/data*/')
        if self.opt.dockerfile is None:
            try:
                import donv
                self.opt.donv_dir = os.path.dirname(donv.__file__)
                self.opt.donv_docker_dir = os.path.join(self.opt.donv_dir, 'docker')
                self.opt.dockerfile = os.path.join(self.opt.donv_docker_dir, 'Dockerfile')
                self.opt.requirements = os.path.join(self.opt.donv_docker_dir, 'requirements.txt')
                self.opt.dockerfilesh = os.path.join(self.opt.donv_docker_dir, 'dockerfile.sh')
            except:
                self.opt.dockerfile = 'Dockerfile'

    def get_option(self):
        """get_option
        """
        return self.opt

if __name__ == '__main__':
    opt = Options().get_option()
    print(opt)