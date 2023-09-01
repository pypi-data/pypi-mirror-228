""" GlmnetClassifier tests

===============================================================
Author: Rolf Carlson, Carlson Research, LLC <hrolfrc@gmail.com>
License: 3-clause BSD
===============================================================

"""
import pytest
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from glmnet_classifier import GlmnetClassifier


@pytest.fixture
def data():
    return load_iris(return_X_y=True)


def test_GlmnetClassifier(data):
    X, y = data
    clf = GlmnetClassifier().fit(X, y)

    assert hasattr(clf, 'classes_')
    assert hasattr(clf, 'X_')
    assert hasattr(clf, 'y_')

    # =====================================
    # How well glmnet learns the dataset
    y_pred = clf.predict(X)
    assert len(y) == len(y_pred)

    accuracy = accuracy_score(y_true=y, y_pred=y_pred)
    assert round(accuracy, 4) == 0.9533

    # =====================================
    # how well glmnet learns unseen data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        random_state=42
    )

    clf = GlmnetClassifier().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    assert len(y_test) == len(y_pred)

    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    assert round(accuracy, 4) == 0.9737


