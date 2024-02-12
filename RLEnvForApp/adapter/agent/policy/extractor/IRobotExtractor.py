import tensorflow as tf

from RLEnvForApp.adapter.agent.layer.CustomLayerFactoryService import \
    CustomLayerFactoryService
from RLEnvForApp.adapter.agent.policy.extractor.IExtractor import IExtractor


class IRobotExtractor(IExtractor):
    @staticmethod
    def getExtractor(scaled_images, **kwargs):
        DOMFeature, branchCoverageVectorFeature, focusIndexFeature = tf.split(scaled_images, [
                                                                              130100, 1036, 150], 2)

        branchCoverageVectorFeatureInt = tf.to_int32(
            branchCoverageVectorFeature)
        branchCoverageVectorResize = tf.squeeze(
            branchCoverageVectorFeatureInt, squeeze_dims=[1, 3])
        branchCoverageVectorFeatureFloat = tf.to_float(
            branchCoverageVectorResize)

        focusIndexFeatureInt = tf.to_int32(focusIndexFeature)
        focusIndexFeatureResize = tf.squeeze(
            focusIndexFeatureInt, squeeze_dims=[1, 3])
        focusIndexFeatureFloat = tf.to_float(focusIndexFeatureResize)

        DOMFeatureFlatten = CustomLayerFactoryService.createIRobotCNNLayer(
            inputLayer=DOMFeature)

        concatenation = tf.concat(
            [DOMFeatureFlatten, branchCoverageVectorFeatureFloat, focusIndexFeatureFloat], axis=1)

        return tf.contrib.layers.fully_connected(concatenation, 51)
