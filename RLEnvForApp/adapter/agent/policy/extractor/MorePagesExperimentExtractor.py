# MorePagesExperimentExtractor
from RLEnvForApp.adapter.agent.policy.extractor.IExtractor import IExtractor
import tensorflow as tf

from RLEnvForApp.logger.logger import Logger


class MorePagesExperimentExtractor(IExtractor):

    @staticmethod
    def getExtractor(scaled_images, **kwargs):
        Logger().info(scaled_images)
        labelNameFeature, tagNameFeature, tagTypeFeature = tf.split(scaled_images, [300, 300, 300], 2)
        labelNameFeatureResize = tf.squeeze(labelNameFeature, squeeze_dims=[1, 3])
        tagNameFeatureResize = tf.squeeze(tagNameFeature, squeeze_dims=[1, 3])
        tagTypeFeatureResize = tf.squeeze(tagTypeFeature, squeeze_dims=[1, 3])

        focusElementFeatureConcat = tf.concat([labelNameFeatureResize, tagNameFeatureResize], axis=1)

        output = tf.contrib.layers.fully_connected(focusElementFeatureConcat, 64)

        return output

