import os.path as osp
from .cyclegan import load_model, im2torch, torch2im
import subprocess

URL = 'put url here'
default_path = osp.join(osp.abspath(osp.dirname(__file__)), 'latest_generator.pth')

if not osp.exists(default_path):
    print('Downloading generator...')
    bash = 'curl %s > latest_generator.pth' % URL
    subprocess.Popen(bash)
    print('Done')
