from unittest import TestCase

import numpy as np
from scipy.stats import chi2

from alea.utils import (
    MAX_FLOAT,
    get_analysis_space,
    formatted_to_asterisked,
    asymptotic_critical_value,
    within_limits,
    clip_limits,
    can_expand_grid,
    expand_grid_dict,
    deterministic_hash,
)


class TestUtils(TestCase):
    """Test of the alea.utils."""

    def test_get_analysis_space(self):
        """Test of the get_analysis_space function."""
        analysis_space = [
            {"a": "np.arange(3)"},
            {"b": [0, 1, 2]},
            {"c": "0, 1, 2"},
            {"d": "0 1 2"},
        ]
        get_analysis_space(analysis_space)

    def test_formatted_to_asterisked(self):
        """Test of the formatted_to_asterisked function."""
        self.assertEqual(formatted_to_asterisked("a_{a:.2f}_b_{b:d}"), "a_*_b_*")
        self.assertEqual(formatted_to_asterisked("a_{a:.2f}_b_{b:d}", wildcards="a"), "a_*_b_{b:d}")

    def test_asymptotic_critical_value(self):
        """Test of the asymptotic_critical_value function."""
        confidence_level = 0.9
        critical_value = chi2(1).isf(2 * (1.0 - confidence_level))
        self.assertEqual(asymptotic_critical_value("lower", confidence_level), critical_value)
        self.assertEqual(asymptotic_critical_value("upper", confidence_level), critical_value)

    def test_within_limits(self):
        """Test of the within_limits function."""
        self.assertTrue(within_limits(MAX_FLOAT, clip_limits(None)))
        self.assertTrue(within_limits(MAX_FLOAT, clip_limits([0, None])))
        self.assertTrue(within_limits(MAX_FLOAT, clip_limits([None, MAX_FLOAT])))

    def test_can_expand_grid(self):
        """Test of the can_expand_grid function."""
        self.assertTrue(can_expand_grid({"a": [1, 2], "b": [3, 4]}))

    def test_expand_grid_dict(self):
        """Test of the expand_grid_dict function."""
        self.assertEqual(
            expand_grid_dict(["free", {"a": 1, "b": 3}, {"a": [1, 2], "b": [3, 4]}]),
            [
                "free",
                {"a": 1, "b": 3},
                {"a": 1, "b": 3},
                {"a": 1, "b": 4},
                {"a": 2, "b": 3},
                {"a": 2, "b": 4},
            ],
        )

    def test_deterministic_hash(self):
        """Test of the deterministic_hash function."""
        self.assertEqual(deterministic_hash([0, 1]), "si3ifpvg2u")
        self.assertEqual(deterministic_hash(np.array([0, 1])), "si3ifpvg2u")
        self.assertEqual(deterministic_hash({"a": 1, "b": 2}), "shhkapn4q7")
        self.assertEqual(
            deterministic_hash({"a": np.array([0, 1]), "b": np.array([0, 1])}), "anxefavaju"
        )
