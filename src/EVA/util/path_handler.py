import sys
import os

def get_path(path):
    # check if running from the executable or not
    bundle_dir = getattr(sys, '_MEIPASS', "")
    return os.path.abspath(os.path.join(bundle_dir, path))