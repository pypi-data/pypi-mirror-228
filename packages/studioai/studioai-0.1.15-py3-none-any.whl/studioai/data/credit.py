#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/data/credit.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 23rd 2023 05:56:02 am                                              #
# Modified   : Sunday August 27th 2023 08:19:36 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

import pandas as pd

from studioai.data.dataset import Dataset


# ------------------------------------------------------------------------------------------------ #
class CreditScoreDataset(Dataset):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df=df)

    @property
    def summary(self) -> pd.DataFrame:
        return (
            self._df[["Gender", "Education", "Marital Status", "Own", "Credit Rating"]]
            .value_counts()
            .reset_index()
        )
