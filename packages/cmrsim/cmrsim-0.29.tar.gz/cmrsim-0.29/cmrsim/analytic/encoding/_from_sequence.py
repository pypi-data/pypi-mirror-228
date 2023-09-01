""" This module contains the generic implementation of encoding modules using sequence
 definitions from cmrseq """

__all__ = ["GenericEncoding"]

from typing import Union, Iterable

import tensorflow as tf
import cmrseq

from cmrsim.analytic.encoding.base import BaseSampling


# pylint: disable=abstract-method
class GenericEncoding(BaseSampling):
    """" Interface to use cmr-seq definitions of k-space samples as encoder"""
    def __init__(self, name: str,
                 sequence: Union[cmrseq.Sequence, Iterable[cmrseq.Sequence]],
                 absolute_noise_std: Union[float, Iterable[float]],
                 k_space_segments: int = None,
                 device: str = None):
        """

        :param name: Name of the module
        :param sequence: List or single instance of cmrseq.Sequence that implements the
                            calculate_kspace() function
        :param absolute_noise_std: Noise standard deviation
        :param k_space_segments: If not specified, the number of sequences is used.
        :param device: Name of device that the operation is placed on
        """

        if isinstance(sequence, cmrseq.Sequence):
            sequence = [sequence, ]

        if k_space_segments is None:
            k_space_segments = len(sequence)

        self.sequence_list = sequence
        super().__init__(absolute_noise_std, name, device=device,
                         k_space_segments=tf.constant(k_space_segments, dtype=tf.int32))

    def _calculate_trajectory(self) -> (tf.Tensor, tf.Tensor):
        """ Calls the calculate_kspace() for all entries in self._sequence_list, stacks the k-space
        vectors and flattens the array()
        :return:  kspace-vectors, timing
        """
        k_space, timings = [], []
        for seq in self.sequence_list:
            _, k_adc, t_adc = seq.calculate_kspace()
            k_space.append(k_adc.T)
            timings.append(t_adc)

        # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
        k_space = tf.cast(tf.concat(k_space, axis=0), tf.float32)
        # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
        timings = tf.cast(tf.concat(timings, axis=0), tf.float32)
        return k_space, timings
