# !/usr/bin/env python
# coding: utf-8

from gaiaframework.base.pipeline.predictables.predictable import DS_Predictable
from ..artifacts.shared_artifacts import generatedProjectNameSharedArtifacts
from gaiaframework.base.common.output_logger import OutputLogger

##
# @file
# @brief Predictable class, implements DS_Predictable base class.
class generatedClass(DS_Predictable):
    """! generatedClass class inherits from DS_Predictable.

    Predictable objects are basically a list of objects which is transferred between different components
    of the pipline.

    See the following example to understand better its usage:
    @code{.py}
    self.predictables = self.preprocess(**kwargs)
    for c in self.components:
        self.predictables = c.execute(self.predictables)
    return self.postprocess(self.predictables)
    @endcode
    """

    def __init__(self, artifacts: generatedProjectNameSharedArtifacts=None) -> None:
        """! Initializer for generatedClass"""
        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)
        self.logger = OutputLogger('generatedClass', log_level='INFO')
        if self.artifacts.log_level:
            self.logger.set_log_level(self.artifacts.log_level)

