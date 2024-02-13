import tensorflow as tf

from RLEnvForApp.adapter.agent.layer.CustomLayerFactoryService import \
    CustomLayerFactoryService
from RLEnvForApp.adapter.agent.policy.extractor.IExtractor import IExtractor


class IRobotExtractor(IExtractor):
    @staticmethod
    def get_extractor(scaled_images, **kwargs):
        dom_feature, branchCoverageVectorFeature, focusIndexFeature = tf.split(scaled_images, [
                                                                              130100, 1036, 150], 2)

        branch_coverage_vector_feature_int = tf.to_int32(
            branchCoverageVectorFeature)
        branch_coverage_vector_resize = tf.squeeze(
            branch_coverage_vector_feature_int, squeeze_dims=[1, 3])
        branch_coverage_vector_feature_float = tf.to_float(
            branch_coverage_vector_resize)

        focus_index_feature_int = tf.to_int32(focusIndexFeature)
        focus_index_feature_resize = tf.squeeze(
            focus_index_feature_int, squeeze_dims=[1, 3])
        focus_index_feature_float = tf.to_float(focus_index_feature_resize)

        dom_feature_flatten = CustomLayerFactoryService.create_i_robot_cnn_layer(
            inputLayer=dom_feature)

        concatenation = tf.concat(
            [dom_feature_flatten, branch_coverage_vector_feature_float, focus_index_feature_float], axis=1)

        return tf.contrib.layers.fully_connected(concatenation, 51)
