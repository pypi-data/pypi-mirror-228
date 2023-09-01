#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /studioai/stats/inferential/chisquare.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday May 29th 2023 03:00:39 am                                                    #
# Modified   : Friday September 1st 2023 03:36:51 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd
from scipy import stats
from dependency_injector.wiring import inject, Provide

from studioai.container import StudioAIContainer
from studioai.visual.seaborn import Visualizer
from studioai.stats.inferential.profile import StatTestProfile
from studioai.stats.inferential.base import (
    StatTestResult,
    StatisticalTest,
)


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class ChiSquareIndependenceResult(StatTestResult):
    dof: int = None
    data: pd.DataFrame = None
    a: str = None
    b: str = None
    visualizer: Visualizer = None

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[StudioAIContainer.seaborn]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.x2testplot(
            statistic=self.value, dof=self.dof, result=self.result, alpha=self.alpha
        )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class ChiSquareIndependenceTest(StatisticalTest):
    """Chi-Square Test of Independence

    The Chi-Square test of independence is used to determine if there is a significant relationship between two nominal (categorical) variables.  The frequency of each category for one nominal variable is compared across the categories of the second nominal variable.
    """

    __id = "x2ind"

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        a: str = None,
        b: str = None,
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

        n = len(self._data)

        obs = stats.contingency.crosstab(self._data[self._a], self._data[self._b])

        statistic, pvalue, dof, exp = stats.chi2_contingency(obs[1])

        result = self._report_results(statistic=statistic, pvalue=pvalue, dof=dof, n=n)

        if pvalue > self._alpha:  # pragma: no cover
            inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against independence of {self._a} and {self._b} is not significant."
        else:
            inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against independence of {self._a} and {self._b} is significant."

        # Create the result object.
        self._result = ChiSquareIndependenceResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic="X\u00b2",
            hypothesis=self._profile.hypothesis,
            dof=dof,
            value=statistic,
            pvalue=pvalue,
            result=result,
            data=self._data,
            a=self._a,
            b=self._b,
            inference=inference,
            alpha=self._alpha,
        )

    def _report_results(self, statistic: float, pvalue: float, dof: float, n: int) -> str:
        return f"X\u00b2 Test of Independence\n{self._a.capitalize()} and {self._b.capitalize()}\nX\u00b2({dof}, N={n})={round(statistic,2)}, {self._report_pvalue(pvalue)}."
