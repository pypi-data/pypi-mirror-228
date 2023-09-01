from . import option
from .base import Docker_Base

class Docker_Stop(Docker_Base):
    def __init__(self, opt):
        super(Docker_Stop, self).__init__(opt)
        self.set_cmd()

    def set_cmd(self):
        self.add_option(f'docker stop')
        self.add_remain_option(' \\')  
        self.add_option(f'{self.opt.name}', ' \\')

def main():
    opt = option.Options().get_option()
    docker = Docker_Stop(opt)
    docker.print_cmd()
    docker.do_cmd()

if __name__ == '__main__':
    main()