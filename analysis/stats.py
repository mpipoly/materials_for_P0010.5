#-*- coding:utf-8 -*-

"""
This file is part of P0010.5.

P0010.5 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0010.5 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0010.5.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import warnings
import numpy as np
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt
from exparser.RBridge import RBridge
from exparser.DataMatrix import DataMatrix
from exparser.Cache import cachedDataMatrix
from analysis.constants import *
import analysis

def effectSlope(dm, dv='salFrom'):

	"""
	desc:
		Determines the slope of the partial effect of pupilSize on saliency.

	arguments:
		dm:
			desc:	Data.
			type:	DataMatrix

	keywords:
		dv:
			desc:	A custom dependent variable.
			type:	[str, unicode]

	returns:
		desc:	A (slope, t, ci96lo, ci95up) tuple.
		type:	tuple
	"""

	R.load(dm)
	_dm = R.lmer(formula(dm, dv=dv))
	_dm = _dm.select('effect == "pupilSize"', verbose=False)
	est = _dm['est'][0]
	t  = _dm['t'][0]
	se = _dm['se'][0]
	lo = est-se
	hi = est+se
	return est, t, lo, hi

def fixedEffects():

	"""
	desc:
		Specifies the fixed effects for the model, which depend on the
		experiment.

	returns:
		desc:	A list of fixed effects.
		type:	list
	"""

	if exp == 'exp1':
		return ['trialId', 'saccNr', 'lumFrom', 'eccFrom', 'fromX', 'fromY',
			'iSacc', 'size']
	if exp == 'exp2':
		return ['trialId', 'saccNr', 'lumFrom', 'eccFrom', 'fromX', 'fromY',
			'size']
	if exp == 'exp3':
		return ['trialId', 'saccNr', 'lumFrom', 'eccFrom', 'fromX', 'fromY',
			'iSacc', 'size']

def formula(dm, dv='salFrom', partial=True):

	"""
	desc:
		Generates the R formula for the current experiment.

	arguments:
		dm:
			desc:	Data.
			type:	DataMatrix

	keywords:
		dv:
			desc:	A custom dependent variable.
			type:	[str, unicode]
		partial:
			desc:	Indicates whether other fixed effects should be included
					for the purpose of partialling.
			type:	bool

	returns:
		desc:	A string with the R formula.
		type:	str
	"""

	if partial:
		# Make sure that we only include fixed effects that actually occur multiple
		# times in the data.
		lfe = []
		for fe in fixedEffects():
			if dm.count(fe) > 1:
				lfe.append(fe)
			else:
				print 'Excluding %s as fixed effect' % fe
		f = '%s ~ %s + pupilSize + %s' % (dv, ' + '.join(lfe),
			modelRandomEffects)
	else:
		f = '%s ~ pupilSize + %s' % (dv, modelRandomEffects)
	print 'Formula = %s' % f
	return f

# Start the connection to R
R = RBridge()
