import argparse
import os
from faceg.images_grouper import imagesGrouper


def valid_dir_path_type(arg_dir_path_type_str: str):
    if os.path.isdir(arg_dir_path_type_str):
        return arg_dir_path_type_str
    else:
        raise argparse.ArgumentTypeError('The entered directory is not valid')


parser = argparse.ArgumentParser(description='Tool to group photos by found faces')
parser.add_argument('-d', '--directory', type=valid_dir_path_type, required=True, help='Directory containing photos')
parser.add_argument('--itr', dest='iterate_dir', action='store_true', help='Subdirectories of the provided directory will be searched')
parser.add_argument('--move', dest='move', action='store_true', help='Found photos are moved to the destination instead of being copied')
args = parser.parse_args()


if __name__ == '__main__':
    grouper = imagesGrouper(args.directory, args.iterate_dir, args.move)
    grouper.group_images()


