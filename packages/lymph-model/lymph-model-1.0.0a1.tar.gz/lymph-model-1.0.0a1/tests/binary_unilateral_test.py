"""Test the binary unilateral system."""
import unittest
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import scipy as sp

from lymph.descriptors import diagnose_times
from lymph.descriptors.modalities import Clinical, Modality, Pathological
from lymph.graph import LymphNodeLevel, Tumor
from lymph.models import Unilateral


class ModelFixtureMixin:
    """Mixin class for simple binary model fixture creation."""

    def setUp(self):
        """Initialize a simple binary model."""
        large_graph = {
            ("tumor", "T"): ["I", "II", "III", "IV", "V", "VII"],
            ("lnl", "I"): [],
            ("lnl", "II"): ["I", "III", "V"],
            ("lnl", "III"): ["IV", "V"],
            ("lnl", "IV"): [],
            ("lnl", "V"): [],
            ("lnl", "VII"): [],
        }
        medium_graph = {
            ("tumor", "T"): ["II", "III", "V"],
            ("lnl", "II"): ["III", "V"],
            ("lnl", "III"): ["V"],
            ("lnl", "V"): [],
        }
        small_graph = {
            ("tumor", "T"): ["II", "III"],
            ("lnl", "II"): ["III"],
            ("lnl", "III"): [],
        }
        self.graph_dict = small_graph
        self.model = Unilateral(graph_dict=self.graph_dict)

    def create_random_params(self, seed: int = 42) -> dict[str, float]:
        """Create random parameters for the model."""
        rng = np.random.default_rng(seed)
        return {name: rng.random() for name in self.model.graph.edge_params.keys()}

    def create_modalities(self) -> dict[str, Modality]:
        """Add modalities to the model."""
        return {
            "CT": Clinical(specificity=0.81, sensitivity=0.86),
            "FNA": Pathological(specificity=0.95, sensitivity=0.81),
        }


class InitTestCase(ModelFixtureMixin, unittest.TestCase):
    """Test the initialization of a binary model."""

    def test_num_nodes(self):
        """Check number of nodes initialized."""
        num_nodes = len(self.graph_dict)
        num_tumor = len({name for kind, name in self.graph_dict if kind == "tumor"})
        num_lnls = len({name for kind, name in self.graph_dict if kind == "lnl"})

        self.assertEqual(len(self.model.graph.nodes), num_nodes)
        self.assertEqual(len(self.model.graph._tumors), num_tumor)
        self.assertEqual(len(self.model.graph._lnls), num_lnls)

    def test_num_edges(self):
        """Check number of edges initialized."""
        num_edges = sum(len(receiving_nodes) for receiving_nodes in self.graph_dict.values())
        num_tumor_edges = sum(
            len(receiving_nodes) for (kind, _), receiving_nodes in self.graph_dict.items()
            if kind == "tumor"
        )
        num_lnl_edges = sum(
            len(receiving_nodes) for (kind, _), receiving_nodes in self.graph_dict.items()
            if kind == "lnl"
        )

        self.assertEqual(len(self.model.graph.edges), num_edges)
        self.assertEqual(len(self.model.graph._tumor_edges), num_tumor_edges)
        self.assertEqual(len(self.model.graph._lnl_edges), num_lnl_edges)
        self.assertEqual(len(self.model.graph._growth_edges), 0)

    def test_tumor(self):
        """Make sure the tumor has been initialized correctly."""
        tumor = self.model.graph.find_node("T")
        state = tumor.state
        self.assertIsInstance(tumor, Tumor)
        self.assertListEqual(tumor.allowed_states, [state])

    def test_lnls(self):
        """Test they are all binary lymph node levels."""
        for lnl in self.model.graph._lnls:
            self.assertIsInstance(lnl, LymphNodeLevel)
            self.assertTrue(lnl.is_binary)

    def test_tumor_to_lnl_edges(self):
        """Make sure the tumor to LNL edges have been initialized correctly."""
        tumor = self.model.graph.find_node("T")
        receiving_lnls = self.graph_dict[("tumor", "T")]
        connecting_edge_names = [f"{tumor.name}_to_{lnl}" for lnl in receiving_lnls]

        for edge in self.model.graph._tumor_edges:
            self.assertEqual(edge.parent.name, "T")
            self.assertIn(edge.child.name, receiving_lnls)
            self.assertTrue(edge.is_tumor_spread)
            self.assertIn(edge.name, connecting_edge_names)


class ParameterAssignmentTestCase(ModelFixtureMixin, unittest.TestCase):
    """Test the assignment of parameters in a binary model."""

    def test_edge_params_assignment_via_lookup(self):
        """Make sure the spread parameters are assigned correctly."""
        params_to_set = self.create_random_params(seed=42)
        for name, value in params_to_set.items():
            self.model.graph.edge_params[name].set_param(value)
            self.assertEqual(self.model.graph.edge_params[name].get_param(), value)

    def test_edge_params_assignment_via_method(self):
        """Make sure the spread parameters are assigned correctly."""
        params_to_set = self.create_random_params(seed=43)
        self.model.assign_params(**params_to_set)
        for name, value in params_to_set.items():
            self.assertEqual(self.model.graph.edge_params[name].get_param(), value)

    def test_direct_assignment_raises_error(self):
        """Make sure direct assignment of parameters raises an error."""
        with self.assertRaises(TypeError):
            self.model.graph.edge_params["spread_T_to_I"] = 0.5

    def test_transition_matrix_deletion(self):
        """Check if the transition matrix gets deleted when a parameter is set.

        NOTE: This test is disabled because apparently, the `model` instance is
        changed during the test and the `_transition_matrix` attribute is deleted on
        the wrong instance. I have no clue why, but generally, the method works.
        """
        first_lnl_name = self.model.graph._lnls[0].name
        _ = self.model.transition_matrix
        self.assertTrue(hasattr(self.model, "_transition_matrix"))
        self.model.graph.edge_params[f"spread_T_to_{first_lnl_name}"].set_param(0.5)
        self.assertFalse(hasattr(self.model, "_transition_matrix"))


class TransitionMatrixTestCase(ModelFixtureMixin, unittest.TestCase):
    """Test the generation of the transition matrix in a binary model."""

    def setUp(self):
        """Initialize a simple binary model."""
        super().setUp()

        params_to_set = self.create_random_params(seed=42)
        self.model.assign_params(**params_to_set)

    def test_shape(self):
        """Make sure the transition matrix has the correct shape."""
        num_lnls = len({name for kind, name in self.graph_dict if kind == "lnl"})
        self.assertEqual(self.model.transition_matrix.shape, (2**num_lnls, 2**num_lnls))

    def test_is_probabilistic(self):
        """Make sure the rows of the transition matrix sum to one."""
        row_sums = np.sum(self.model.transition_matrix, axis=1)
        self.assertTrue(np.allclose(row_sums, 1.))

    @staticmethod
    def is_recusively_upper_triangular(mat: np.ndarray) -> bool:
        """Return `True` is `mat` is recursively upper triangular."""
        if mat.shape == (1, 1):
            return True

        if not np.all(np.equal(np.triu(mat), mat)):
            return False

        half = mat.shape[0] // 2
        for i in [0, 1]:
            for j in [0, 1]:
                return TransitionMatrixTestCase.is_recusively_upper_triangular(
                    mat[i * half:(i + 1) * half, j * half:(j + 1) * half]
                )

    def test_is_recusively_upper_triangular(self) -> None:
        """Make sure the transition matrix is recursively upper triangular."""
        self.assertTrue(self.is_recusively_upper_triangular(self.model.transition_matrix))


class ObservationMatrixTestCase(ModelFixtureMixin, unittest.TestCase):
    """Test the generation of the observation matrix in a binary model."""

    def setUp(self):
        """Initialize a simple binary model."""
        super().setUp()
        self.model.modalities = self.create_modalities()

    def test_shape(self):
        """Make sure the observation matrix has the correct shape."""
        num_lnls = len(self.model.graph._lnls)
        num_modalities = len(self.model.modalities)
        expected_shape = (2**num_lnls, 2**(num_lnls + num_modalities))
        self.assertEqual(self.model.observation_matrix.shape, expected_shape)

    def test_is_probabilistic(self):
        """Make sure the rows of the observation matrix sum to one."""
        row_sums = np.sum(self.model.observation_matrix, axis=1)
        self.assertTrue(np.allclose(row_sums, 1.))


class LoadDataFixtureMixin(ModelFixtureMixin):
    """Mixin for model with loaded data."""

    def setUp(self):
        super().setUp()
        self.model.modalities = self.create_modalities()

        test_data_dir = Path(__file__).parent / "data"
        self.patient_data = pd.read_csv(
            test_data_dir / "2021-usz-oropharynx.csv",
            header=[0,1,2],
        )

        # Don't pollute the test output with performance warnings
        warnings.simplefilter("ignore", category=pd.errors.PerformanceWarning)
        self.model.load_patient_data(self.patient_data, side="ipsi")

        # Initialize some fixed diagnose time distributions
        self.init_diag_time_dists(["early", "late", "foo"])

    def init_diag_time_dists(self, t_stages: list[str], seed: int = 42) -> None:
        """Initialize some fixed diagnose time distributions."""
        rng = np.random.default_rng(seed)
        for t_stage in t_stages:
            self.model.diag_time_dists[t_stage] = rng.uniform(
                low=0., high=1., size=self.model.max_time + 1
            )


class PatientDataTestCase(LoadDataFixtureMixin, unittest.TestCase):
    """Test loading the patient data."""

    def test_load_patient_data(self):
        """Make sure the patient data is loaded correctly."""
        self.assertEqual(len(self.model.patient_data), len(self.patient_data))
        self.assertRaises(
            ValueError, self.model.load_patient_data, self.patient_data, side="foo"
        )

    def test_t_stages(self):
        """Make sure all T-stages are present."""
        t_stages_in_data = self.model.patient_data["_model", "#" ,"t_stage"].unique()
        t_stages_in_diag_time_dists = self.model.diag_time_dists.keys()
        t_stages_in_model = list(self.model.t_stages)
        t_stages_intersection = set(t_stages_in_data).intersection(t_stages_in_diag_time_dists)

        self.assertNotIn("foo", t_stages_in_model)
        self.assertEqual(len(t_stages_in_diag_time_dists), 3)
        self.assertEqual(len(t_stages_intersection), 2)
        self.assertEqual(len(t_stages_intersection), len(t_stages_in_model))

        for t_stage in t_stages_in_model:
            self.assertIn(t_stage, t_stages_in_data)
            self.assertIn(t_stage, t_stages_in_diag_time_dists)


    def test_data_matrices(self):
        """Make sure the data matrices are generated correctly."""
        for t_stage in ["early", "late"]:
            has_t_stage = self.patient_data["tumor", "1", "t_stage"].isin({
                "early": [0,1,2],
                "late": [3,4],
            }[t_stage])
            data_matrix = self.model.data_matrices[t_stage]

            self.assertTrue(t_stage in self.model.data_matrices)
            self.assertEqual(
                data_matrix.shape[0],
                self.model.observation_matrix.shape[1],
            )
            self.assertEqual(
                data_matrix.shape[1],
                has_t_stage.sum(),
            )

        self.assertRaises(
            AttributeError,
            lambda: setattr(self.model, "data_matrices", "foo")
        )

    def test_diagnose_matrices(self):
        """Make sure the diagnose matrices are generated correctly."""
        for t_stage in ["early", "late"]:
            has_t_stage = self.patient_data["tumor", "1", "t_stage"].isin({
                "early": [0,1,2],
                "late": [3,4],
            }[t_stage])
            diagnose_matrix = self.model.diagnose_matrices[t_stage]

            self.assertTrue(t_stage in self.model.diagnose_matrices)
            self.assertEqual(
                diagnose_matrix.shape[0],
                self.model.transition_matrix.shape[1],
            )
            self.assertEqual(
                diagnose_matrix.shape[1],
                has_t_stage.sum(),
            )
            self.assertTrue(np.all(np.less_equal(diagnose_matrix, 1.)))

        self.assertRaises(
            AttributeError,
            lambda: setattr(self.model, "diagnose_matrices", "foo")
        )


class LikelihoodTestCase(LoadDataFixtureMixin, unittest.TestCase):
    """Test the likelihood of a model."""

    def setUp(self):
        super().setUp()
        self.model.diag_time_dists["early"] = self.create_frozen_diag_time_dist(seed=42)
        self.model.diag_time_dists["late"] = self.create_parametric_diag_time_dist(seed=42)
        self.model.assign_params(**self.create_random_params(seed=42))

    def create_random_params(self, seed: int = 42) -> dict[str, float]:
        """Create random parameters."""
        rng = np.random.default_rng(seed)
        random_params = super().create_random_params(seed=seed)
        random_params["late_p"] = rng.uniform(low=0., high=1.)
        return random_params

    def create_frozen_diag_time_dist(self, seed: int = 42) -> np.ndarray:
        """Create a frozen diagnose time distribution."""
        rng = np.random.default_rng(seed)
        unnormalized = rng.uniform(low=0., high=1., size=self.model.max_time + 1)
        return unnormalized / np.sum(unnormalized)

    def create_parametric_diag_time_dist(self, seed: int = 42) -> diagnose_times.Distribution:
        """Create a parametric diagnose time distribution."""
        rng = np.random.default_rng(seed)
        def _pmf(support: np.ndarray, p: float = rng.uniform()) -> np.ndarray:
            return sp.stats.binom.pmf(support, p=p, n=self.model.max_time + 1)

        return diagnose_times.Distribution(
            distribution=_pmf,
            max_time=self.model.max_time,
        )

    def test_likelihood(self):
        """Make sure the likelihood is computed correctly."""
        likelihood = self.model.likelihood(log=True, mode="HMM")
        self.assertLess(likelihood, 0.)
