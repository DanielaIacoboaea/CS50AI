import cv2
import numpy as np
import os
import sys
import logging
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")



def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    # get the path of the current working directory
    dir = os.getcwd()

    # get the path to the data_dir
    data_path = os.path.join(dir, data_dir)

    # get the list of category directories that hold all images
    categories_dirs = os.listdir(data_path)

    # go through each category directory
    for category in categories_dirs:
        category_path = os.path.join(data_path, category)

        # check if it's a directory 
        if os.path.isdir(category_path):

            # get the list of all images inside the directory
            images_list = os.listdir(category_path)

            # for each image read it as numpy ndarray
            for image in images_list:

                # get the path of the image
                img_path = os.path.join(category_path, image)

                # use the default flag that reads the image with RGB colors
                img = cv2.imread(img_path)

                # set the width and height for resizing the image to IMG_WIDTH and IMG_HEIGHT
                dsize = (IMG_WIDTH, IMG_HEIGHT)

                # resize the image
                output = cv2.resize(img, dsize, interpolation = cv2.INTER_AREA)

                # normalize size
                output = output / 255.0

                # add the resized image to the list of images
                images.append(output)

                # add the label for this image to the list of labels
                labels.append(int(category))

    print("Images loaded")
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # Start a model of convolutional neural network
    model = tf.keras.models.Sequential()

    # Add a Convolutional layer with 32 filters and dropout 0.2
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    # Add a Max-pooling layer to reduce the size of the images
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.2))

    # Add a Second Convolutional layer with an increased number of filters to 64
    # and dropout 0.2
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation="relu"))

    # Add a Max-pooling layer to reduce the size of the images
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.2))

    # Flatten the data before passing it into the neural network
    model.add(tf.keras.layers.Flatten())

    # Add a hidden layer with dropout 0.5
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))

    # Add an output layer with `NUM_CATEGORIES` units
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
