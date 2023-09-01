#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/stats/inferential/ttest.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 11:41:00 pm                                                 #
# Modified   : Monday August 28th 2023 07:28:21 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import numpy as np
from scipy import stats
from dependency_injector.wiring import inject, Provide

from studioai.visual.container import VisualizerContainer
from studioai.visual.seaborn import Visualizer
from studioai.stats.inferential.profile import StatTestProfile
from studioai.stats.inferential.base import (
    StatTestResult,
    StatisticalTest,
)

from studioai.stats.descriptive.continuous import ContinuousStats


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class TTestResult(StatTestResult):
    dof: int = None
    homoscedastic: bool = None
    a: np.ndarray = None
    a_name: str = None
    b: np.ndarray = None
    b_name: str = None
    varname: str = None
    a_stats: ContinuousStats = None
    b_stats: ContinuousStats = None

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[VisualizerContainer.seaborn]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.ttestplot(
            statistic=self.value, dof=self.dof, result=self.result, alpha=self.alpha
        )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class TTest(StatisticalTest):
    """Calculate the T-test for the means of two independent samples of scores.

    This is a test for the null hypothesis that 2 independent samples have identical average
    (expected) values. This test assumes that the populations have identical variances by default.

    Args:
        a: (np.ndarray): An array containing the first of two independent samples.
        b: (np.ndarray): An array containing the second of two independent samples.
        alpha (float): The level of statistical significance for inference.
        homoscedastic (bool): If True, perform a standard independent 2 sample test t
            hat assumes equal population variances. If False, perform Welch’s
            t-test, which does not assume equal population variance.

    """

    __id = "t2"

    def __init__(
        self,
        a: np.ndarray,
        b: np.ndarray,
        varname: str = None,
        a_name: str = None,
        b_name: str = None,
        alpha: float = 0.05,
        homoscedastic: bool = True,
    ) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._varname = varname
        self._a_name = a_name
        self._b_name = b_name
        self._alpha = alpha
        self._homoscedastic = homoscedastic
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
        """Executes the TTest."""

        statistic, pvalue = stats.ttest_ind(a=self._a, b=self._b, equal_var=self._homoscedastic)

        a_stats = ContinuousStats.describe(x=self._a, name=self._a_name)
        b_stats = ContinuousStats.describe(x=self._b, name=self._b_name)

        dof = len(self._a) + len(self._b) - 2

        result = self._report_results(a_stats, b_stats, dof, statistic, pvalue)

        if pvalue > self._alpha:  # pragma: no cover
            inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against identical centers for a and b is not significant."
        else:
            inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against identical centers for a and b is significant."

        # Create the result object.
        self._result = TTestResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            homoscedastic=self._homoscedastic,
            dof=dof,
            value=np.abs(statistic),
            pvalue=pvalue,
            result=result,
            a=self._a,
            a_name=self._a_name,
            b=self._b,
            b_name=self._b_name,
            varname=self._varname,
            a_stats=a_stats,
            b_stats=b_stats,
            inference=inference,
            alpha=self._alpha,
        )

    def _report_results(self, a_stats, b_stats, dof, statistic, pvalue) -> str:
        return f"Independent Samples t Test\na: (N = {a_stats.count}, M = {round(a_stats.mean,2)}, SD = {round(a_stats.std,2)})\nb: (N = {b_stats.count}, M = {round(b_stats.mean,2)}, SD = {round(b_stats.std,2)})\nt({dof}) = {round(statistic,2)}, {self._report_pvalue(pvalue)} {self._report_alpha()}"
