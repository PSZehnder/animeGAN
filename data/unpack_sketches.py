import ndjson
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import os

def unpack_ndjson(jsonpath):
    '''return vectorized drawings'''
    with open(jsonpath) as json:
        data = ndjson.load(json)
    data = [(datum['key_id'], datum['drawing']) for datum in data]
    return data

class Worker: # really just a container for the process function

    def __init__(self, args):
        self.path = args.o
        self.format = args.f

    def draw_vectorized(self, vectors, size=(256, 256)):
        image = np.zeros((*size, 3))
        image.fill(255)
        for vector in vectors:
            vector = np.array(list(zip(*vector)))
            vector = np.int32([vector])
            cv2.polylines(image, vector, isClosed=False, color=(0, 0, 0))
        return image

    def process(self, item):
        vectorized = item[1]
        path = item[0]
        image = self.draw_vectorized(vectorized)
        cv2.imwrite(os.path.join(self.path, path + self.format), image)

def parseargs():
    parser = argparse.ArgumentParser('unpack vectorized images')
    parser.add_argument('-i', help='input file')
    parser.add_argument('-o', help='target folder')
    parser.add_argument('-f', help='format', default='.png')
    parser.add_argument('-w', help='number of workers', default=4, type=int)

    return parser.parse_args()

def main(args):
    processes = args.w
    list_of_imgs = unpack_ndjson(args.i)
    worker = Worker(args)
    with Pool(processes=processes) as pool:
        pool.map(worker.process, list_of_imgs)

if __name__ == '__main__':
    args = parseargs()
    main(args)