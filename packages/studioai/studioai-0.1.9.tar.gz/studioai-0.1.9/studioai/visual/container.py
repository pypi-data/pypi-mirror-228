#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/visual/container.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 09:31:46 am                                               #
# Modified   : Saturday August 26th 2023 09:37:39 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
from dependency_injector import containers, providers

from studioai.visual.seaborn import SeabornCanvas, Visualizer


# ------------------------------------------------------------------------------------------------ #
#                                    VISUALIZER CONTAINER                                          #
# ------------------------------------------------------------------------------------------------ #
class VisualizerContainer(containers.DeclarativeContainer):
    canvas = providers.Factory(SeabornCanvas)
    seaborn = providers.Factory(Visualizer, canvas=canvas)
