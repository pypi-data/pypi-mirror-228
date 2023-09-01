#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/stats/inferential/pearson.py                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 08:15:08 pm                                                 #
# Modified   : Friday September 1st 2023 03:36:51 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from typing import Union

import numpy as np
import pandas as pd
from scipy import stats
from dependency_injector.wiring import inject, Provide

from studioai.visual.seaborn import Visualizer
from studioai.container import StudioAIContainer
from studioai.stats.inferential.profile import StatTestProfile
from studioai.stats.inferential.base import (
    StatTestResult,
    StatisticalTest,
)


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class PearsonCorrelationResult(StatTestResult):
    data: pd.DataFrame = None
    a: str = None
    b: str = None

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[StudioAIContainer.seaborn]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.regplot(data=self.data, x=self.a, y=self.b, title=self.result)


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class PearsonCorrelationTest(StatisticalTest):
    """Pearson correlation coefficient and p-value for testing non-correlation.

    The Pearson correlation coefficient [1] measures the linear relationship between two
    datasets. Like other correlation coefficients, this one varies between -1 and +1 with 0
    implying no correlation. Correlations of -1 or +1 imply an exact linear relationship.
    Positive correlations imply that as x increases, so does y. Negative correlations imply
    that as x increases, y decreases.

    This function also performs a test of the null hypothesis that the distributions underlying
    the samples are uncorrelated and normally distributed. (See Kowalski [3] for a discussion of
    the effects of non-normality of the input on the distribution of the correlation coefficient.)
    The p-value roughly indicates the probability of an uncorrelated system producing datasets
    that have a Pearson correlation at least as extreme as the one computed from these datasets.

    Args:
        data (pd.DataFrame): DataFrame containing at least two variables. Optional
        x (str): Keys in the DataFrame.
        y (str): Keys in the DataFrame.
        alpha (float): The test significance level. Default=0.05

    """

    __id = "pearson"

    def __init__(
        self,
        data: pd.DataFrame = None,
        a: Union[str, np.ndarray, pd.Series] = None,
        b: Union[str, np.ndarray, pd.Series] = None,
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._data = data
        self._a = a
        self._b = b
        self._alpha = alpha
        self._profile = StatTestProfile.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        try:
            pearson_result = stats.pearsonr(
                x=self._data[self._a].values, y=self._data[self._b].values, alternative="two-sided"
            )
        except Exception as e:
            msg = f"Unable to calculate pearson correlation.\n{e}"
            self._logger.exception(msg)
            raise

        r = pearson_result.statistic
        pvalue = pearson_result.pvalue
        confidence_interval = pearson_result.confidence_interval(0.05)
        self._logger.debug(pearson_result)
        self._logger.debug(confidence_interval)

        dof = len(self._data) - 2

        result = self._report_results(r=r, pvalue=pvalue, dof=dof)

        if pvalue > self._alpha:  # pragma: no cover
            inference = f"The two variables had {self._interpret_r(r)}, r({dof})={round(r,2)}, {self._report_pvalue(pvalue)}.\nHowever, the pvalue, {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}% indicating that the correlation coefficient is not statistically significant."
        else:
            inference = f"The two variables had {self._interpret_r(r)}, r({dof})={round(r,2)}, {self._report_pvalue(pvalue)}.\nFurther, the pvalue, {round(pvalue,2)} is lower than level of significance {int(self._alpha*100)}% indicating that the correlation coefficient is statistically significant."

        # Create the result object.
        self._result = PearsonCorrelationResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            value=r,
            pvalue=pvalue,
            result=result,
            data=self._data,
            a=self._a,
            b=self._b,
            inference=inference,
            alpha=self._alpha,
        )

    def _report_results(self, r: float, pvalue: float, dof: float) -> str:
        return f"Pearson Correlation Test\nr({dof})={round(r,2)}, {self._report_pvalue(pvalue)}\n{self._interpret_r(r=r).capitalize()}"

    def _interpret_r(self, r: float) -> str:  # pragma: no cover
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation."
        elif r >= 0.70:
            return f"high {direction} correlation."
        elif r >= 0.5:
            return f"moderate {direction} correlation."
        elif r >= 0.3:
            return f"low {direction} correlation."
        else:
            return "negligible correlation."
