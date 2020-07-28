import pickle
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from PIL import Image
import sh

from utils import get_input_columns


def generate_image_files(videos_path, images_path, fps=30):
    """
    Find videos in a directory, and generate image files for the frames in the videos.
    """
    for video in videos_path.glob('*.mp4'):
        print('Extracting images from', video.name, '...')
        sh.ffmpeg('-i', str(video),
                  '-r', '{}/1'.format(fps),
                  '{}/{}_%03d.jpg'.format(images_path, video.name.replace('.', '_')))


def get_image_data(image_path, picture_size, input_columns):
    """
    Extract pixels from one particular image.
    """
    image = Image.open(str(image_path))
    image = image.crop((80, 0, 560, 480))
    image = image.resize((picture_size, picture_size), Image.ANTIALIAS)
    image_data = np.array(list(zip(*image.getdata()))).reshape(len(input_columns))

    return image_data


def load_images(images_path, dump_path, picture_size):
    """
    Find all image files in a directory, and extract their pixels as a dataframe.
    """
    input_columns = get_input_columns(picture_size)
    sorted_images = list(sorted(images_path.glob('*.jpg')))

    def extract_all_data():
        for image_path in sorted_images:
            yield get_image_data(image_path, picture_size, input_columns)

    print('Reading images...')
    images_data = pd.DataFrame(extract_all_data(), columns=input_columns)

    images_data['file'] = [p.name for p in sorted_images]

    person, place = zip(*[p.name.split('_')[:2]
                          for p in sorted_images])
    images_data['person'] = person
    images_data['place'] = place

    print('Dumping dataframe...')
    images_data.to_pickle(str(dump_path))


if __name__ == '__main__':
    picture_size = int(sys.argv[1])

    images_path = Path('./images')
    videos_path = Path('./videos')
    dump_path = Path('./data_{}x{}.pkl'.format(picture_size, picture_size))

    if '-g' in sys.argv:
        generate_image_files(videos_path, images_path)

    if '-d' in sys.argv:
        load_images(images_path, dump_path, picture_size)
