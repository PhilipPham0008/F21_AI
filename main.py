import pickle
import sys
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from tensorflow.keras.utils import to_categorical
from time import time as now
import argparse

import image_ops
from PIL import Image
import models
import data_loader
import math

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--debug',  type=bool,
                        help='Keep true unless working on a machine with large memory (75gb+)')
    args = parser.parse_args()

    #data_dir = "C:\\Data\\Latest"
    #train_images = np.asarray(data_loader.get_train_data(dir_path=data_dir))
    #img = train_images[0]
    #status, im3 = image_ops.filter_image_contours(img)
    #plt.imshow(im3)
    #plt.show()

    aug_images_file = open("aug_data.pkl", 'rb')
    aug_labels_file = open("aug_labels.pkl", 'rb')
    #rgb_images_file = open("rbg_data.pkl", 'rb')

    aug_images = pickle.load(aug_images_file)
    aug_labels = pickle.load(aug_labels_file)
    #rgb_images = pickle.load(rgb_images_file)
    if (len(aug_images) == len(aug_labels)):
        print("Lengths match")
    else:
        print("Lengths do not match, check data loader")
        sys.exit(0)
    fig, axs = plt.subplots(4)
    for i, ax in enumerate(axs):
        ax.imshow(aug_images[i])
    #axs[0].imshow(aug_images[0])
    #axs[1].imshow(rgb_images[0])

    plt.show()

    """
    1. No change
    2. Flip_x = True
    3. Flip_y = True
    4. Flip_x==Flip_y==True
    5. Rotate_90, No flip
    6. Rotate_90, Flip_x = True
    7. Rotate_90, Flip_y = True
    8. Rotate_90, Flip_x==Flip_y==True
    9. Rotate_180, No flip
    10. Rotate_180, Flip_x = True
    11. Rotate_180, Flip_y = True
    12. Rotate_180, Flip_x==Flip_y==True
    13. Rotate_270, No flip
    14. Rotate_270, Flip_x = True
    15. Rotate_270, Flip_y = True
    16. Rotate_270, Flip_x==Flip_y==True
    \"""
    num_classes = 4
    dim = aug_images.shape[1]
    input_type = 'b/w'

    train_images, test_images, train_labels, test_labels = train_test_split( \
        aug_images[:, :dim, :dim], aug_labels, test_size=0.25, random_state=42)
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    if input_type == 'rgb':
        model = models.Alexnet(dim=dim, num_classes=num_classes)
    else:
        train_images = train_images.reshape((train_images.shape[0], train_images.shape[1], train_images.shape[2], 1))
        test_images = test_images.reshape((test_images.shape[0], test_images.shape[1], test_images.shape[2], 1))
        model = models.Alexnet_bw_input(dim=dim, num_classes=num_classes)

    X, y = train_images, train_labels


    BATCH_SIZE = 5
    EPOCHS = 15

    p = np.random.permutation(len(train_images))
    #with tf.device("/device:cpu:0"):

    start = now()
    history = model.fit(X, y, validation_data=(test_images, test_labels), batch_size=BATCH_SIZE, epochs=EPOCHS)
    print("Total training time in %.3f" % (now() - start))

        # evaluate the model
    with tf.device("/device:cpu:0"):
        _, train_acc = model.evaluate(train_images, train_labels, verbose=0)
        _, test_acc = model.evaluate(test_images, test_labels, verbose=0)
        print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

    # plot loss during training
    pyplot.subplot(211)
    pyplot.title('Loss')
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()
    # plot accuracy during training
    pyplot.subplot(212)
    pyplot.title('Accuracy')
    pyplot.plot(history.history['accuracy'], label='train')
    pyplot.plot(history.history['val_accuracy'], label='test')
    pyplot.legend()
    pyplot.show()
    """

