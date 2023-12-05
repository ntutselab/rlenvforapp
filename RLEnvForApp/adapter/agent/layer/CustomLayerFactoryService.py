import tensorflow as tf
import params_flow as pf
from stable_baselines.common.policies import nature_cnn


class CustomLayerFactoryService:
    def createIRobotCNNLayer(inputLayer, activation_fn=tf.nn.leaky_relu):
        layer_1 = tf.contrib.layers.conv2d(inputLayer, 32, [1, 7], [1, 4], activation_fn=activation_fn)
        layer_2 = tf.contrib.layers.conv2d(layer_1, 32, [1, 7], [1, 4], activation_fn=activation_fn)
        max_pool = tf.contrib.layers.max_pool2d(layer_2, [1, 4], [1, 4])

        layer_3 = tf.contrib.layers.conv2d(max_pool, 16, [1, 7], [1, 4], activation_fn=activation_fn)
        max_pool2 = tf.contrib.layers.max_pool2d(layer_3, [1, 7], [1, 7])

        layer_4 = tf.contrib.layers.conv2d(max_pool2, 4, [1, 3], 1, activation_fn=activation_fn)
        max_pool3 = tf.contrib.layers.max_pool2d(layer_4, [1, 4], [1, 4])

        flattened = tf.contrib.layers.flatten(max_pool3)
        return flattened

    def createFlattenLayer(inputLayer):
        return tf.contrib.layers.flatten(inputLayer)

    def createReshapeLayer(inputLayer, shape):
        return tf.reshape(inputLayer, shape=shape)

    def createSplitLayer(value, num_or_size_splits, axis=0):
        return tf.split(value, num_or_size_splits, axis)

    def createConcatLayer(values, axis):
        return tf.concat(values, axis)

    def createCNNLayer(inputLayer, extractor=nature_cnn):
        return extractor(inputLayer)

    def createMLPLayer(inputLayer, layers: list = [64, 64], activation_fn=pf.activations.get_activation("gelu")):
        outputLayer = inputLayer

        for layer_size in layers:
            outputLayer = CustomLayerFactoryService.createFullyConnectedLayer(outputLayer, layer_size, activation_fn)

        return outputLayer

    def createFullyConnectedLayer(inputLayer, layer_size, activation_fn):
        return tf.contrib.layers.fully_connected(inputLayer, layer_size, activation_fn)
