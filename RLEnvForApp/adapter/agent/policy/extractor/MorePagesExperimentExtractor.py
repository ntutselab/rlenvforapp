# MorePagesExperimentExtractor
import tensorflow as tf
from RLEnvForApp.adapter.agent.policy.extractor.IExtractor import IExtractor
from RLEnvForApp.logger.logger import Logger


class MorePagesExperimentExtractor(IExtractor):

    @staticmethod
    def get_extractor(scaled_images, **kwargs):
        Logger().info(scaled_images)
        label_name_feature, tagNameFeature, tagTypeFeature = tf.split(
            scaled_images, [300, 300, 300], 2)
        label_name_feature_resize = tf.squeeze(
            label_name_feature, squeeze_dims=[1, 3])
        tag_name_feature_resize = tf.squeeze(tagNameFeature, squeeze_dims=[1, 3])
        tag_type_feature_resize = tf.squeeze(tagTypeFeature, squeeze_dims=[1, 3])

        focus_element_feature_concat = tf.concat(
            [label_name_feature_resize, tag_name_feature_resize], axis=1)

        output = tf.contrib.layers.fully_connected(
            focus_element_feature_concat, 64)

        return output
