#!/usr/bin/env python

"""
Nonconformity functions.
"""

# Authors: Henrik Linusson

from __future__ import division

import numpy as np

# -----------------------------------------------------------------------------
# Classification error functions
# -----------------------------------------------------------------------------
def inverse_probability(prediction, y):
	prob = np.zeros(y.size, dtype=np.float32)
	for i, y_ in enumerate(y):
		prob[i] = prediction[i, y[i]]
	return 1 - prob

def margin(prediction, y):
	prob = np.zeros(y.size, dtype=np.float32)
	for i, y_ in enumerate(y):
		prob[i] = prediction[i, y[i]]
		prediction[i, y[i]] = -np.inf
	return 0.5 - ((prob - prediction.max(axis=1)) / 2)

# -----------------------------------------------------------------------------
# Regression error functions
# -----------------------------------------------------------------------------
def absolute_error(prediction, y):
	return np.abs(prediction - y)

def absolute_error_inverse(prediction, nc, significance):
	nc = np.sort(nc)[::-1]
	border = int(np.floor(significance * (nc.size + 1))) - 1
	# TODO: should probably warn against too few calibration examples
	border = max(border, 0)
	return np.vstack([prediction - nc[border], prediction + nc[border]]).T

def signed_error(prediction, y):
	return prediction - y

def signed_error_inverse(prediction, nc, significance):
	nc = np.sort(nc)[::-1]
	upper = int(np.floor((significance / 2) * (nc.size + 1)))
	lower = int(np.floor((1 - significance / 2) * (nc.size + 1)))
	# TODO: should probably warn against too few calibration examples
	upper = max(upper, 0)
	lower = min(lower, nc.size - 1)
	return np.vstack([prediction + nc[lower], prediction + nc[upper]]).T

# -----------------------------------------------------------------------------
# Classification nonconformity functions
# -----------------------------------------------------------------------------
class ProbEstClassifierNc(object):
	"""Nonconformity function using an underlying class probability estimating
	model.

	Parameters
	----------
	model_class : class
		The model_class should be implement the fit(x, y) and predict_proba(x)
		functions, as used by the classification models present in the
		scikit-learn library.

	err_func : callable
		Scorer callable object with signature ``score(estimator, x, y)``.

	model_params : dict, optional
		Dict containing parameters to pass to model_class upon
		initialization.

	Attributes
	----------

	See also
	--------

	References
	----------

	Examples
	--------
	"""
	def __init__(self, model_class, err_func, model_params=None):
		self.last_x, self.last_y = None, None
		self.last_prediction = None
		self.clean = False
		self.err_func = err_func

		self.model_class = model_class
		self.model_params = model_params if model_params else {}

		self.model = self.model_class(**self.model_params)

	def fit(self, x, y):
		self.model.fit(x, y)
		self.clean = False

	def underlying_predict(self, x):
		if (not self.clean or
			self.last_x is None or
		    not np.array_equal(self.last_x, x)):

			self.last_x = x
			self.last_prediction = self.model.predict_proba(x)
			self.clean = True

		return self.last_prediction.copy()

	def calc_nc(self, x, y):
		prediction = self.underlying_predict(x)
		return self.err_func(prediction, y)

# -----------------------------------------------------------------------------
# Regression nonconformity functions
# -----------------------------------------------------------------------------
class RegressorNc(object):
	"""
	Nonconformity function based on a simple regression model.
	"""
	def __init__(self,
	             model_class,
	             err_func,
	             inverse_err_func,
	             model_params=None):
		self.last_x, self.last_y = None, None
		self.last_prediction = None
		self.clean = False
		self.err_func = err_func
		self.inverse_err_func = inverse_err_func

		self.model_class = model_class
		self.model_params = model_params if model_params else {}

		self.model = self.model_class(**self.model_params)

	def fit(self, x, y):
		self.model.fit(x, y)
		self.clean = False

	def underlying_predict(self, x):
		if (not self.clean or
			self.last_x is None or
		    not np.array_equal(self.last_x, x)):

			self.last_x = x
			self.last_prediction = self.model.predict(x)
			self.clean = True

		return self.last_prediction.copy()

	def calc_nc(self, x, y):
		prediction = self.underlying_predict(x)
		return self.err_func(prediction, y)

	def predict(self, x, nc, significance):
		prediction = self.underlying_predict(x)
		return self.inverse_err_func(prediction, nc, significance)