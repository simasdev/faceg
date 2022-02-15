import shutil
import os
import numpy as np
import faceg.face_clusterer as fc
import uuid
import sys


class imagesGrouper():
    def __init__(self, directory, iterate_dir=False, move_imgs=False, img_extensions = ['.png', '.jpg', '.jpeg']):
        self.directory = directory
        self.iterate_dir = iterate_dir
        self.move_imgs = move_imgs
        self.img_extensions = img_extensions


    def __move_file(self, dest, file):
        if not self.move_imgs:
            shutil.copy(file, dest)
        else:
            shutil.move(file, dest)


    def __find_images(self):
        images = []
        for path, subdirs, files in os.walk(self.directory):
            if not self.iterate_dir and path != self.directory:
                break

            for name in files:
                file_path = os.path.join(path, name)
                extension = os.path.splitext(file_path)[1]
                if extension.lower() in self.img_extensions:
                    images.append(file_path)

        return images


    def create_directory(self, prefix, unique_lbl):
        if unique_lbl is not None:
            folder_base = self.directory + f'\\{prefix}_{str(unique_lbl + 1)}'
        else:
            folder_base = self.directory + f'\\{prefix}'
            
        folder_final = folder_base
        
        while os.path.isdir(folder_final):
            folder_final = folder_base + str(uuid.uuid4())

        try:
            os.mkdir(folder_final)
            return folder_final
        except:
            sys.exit(f'Unable to write to the folder {self.directory}. Please check if you have permission to write to this folder')


    def group_images(self):
        images = self.__find_images()
        fClt = fc.faceClusterer(images)
        labeled_imgs = fClt.cluster_faces()

        unique_lbls = np.unique([li[1] for li in labeled_imgs])

        for unique_lbl in unique_lbls:
            imgs = [li[0] for li in labeled_imgs if li[1] == unique_lbl]
            if unique_lbl != -1:
                dest_folder = self.create_directory('People', unique_lbl)

                for img in imgs:
                    try:
                        self.__move_file(dest_folder, img)
                    except FileNotFoundError:
                        pass
            else:
                for idx, img in enumerate(imgs):
                    dest_folder = self.create_directory('Person', idx)

                    try:
                        self.__move_file(dest_folder, img)
                    except FileNotFoundError:
                        pass


        unlabeled_imgs = [img for img in images if img not in [lblImg[0] for lblImg in labeled_imgs]]
        dest_folder = self.create_directory('FaceNotDetected', None)

        for unlabeled_img in unlabeled_imgs:
            try:
                self.__move_file(dest_folder, unlabeled_img)
            except FileNotFoundError:
                pass