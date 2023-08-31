import unittest

from tsaugmentation.preprocessing.subsample_dataset import CreateGroups

from gpforecaster.model.gpf import GPF
from gpforecaster.visualization import plot_predictions_vs_original


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.groups = CreateGroups(
            dataset_name=self.dataset_name, sample_perc=0.9, freq="Q"
        ).read_subsampled_groups()
        groups_orig = CreateGroups(
            dataset_name=self.dataset_name, freq="Q"
        ).read_original_groups()
        self.n = self.groups["predict"]["n"]
        self.s = self.groups["train"]["s"]
        self.gpf = GPF(self.dataset_name, self.groups, gp_type="exact90")
        self.gpf_scaled = GPF(
            self.dataset_name, self.groups, gp_type="exact90", scale_x_values=True
        )
        self.groups["predict"] = groups_orig["predict"]

    def test_calculate_metrics_dict(self):
        model, like = self.gpf.train(epochs=10)
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_complete=self.gpf.complete_x,
            x_original=self.gpf.train_x.numpy(),
            x_test=self.gpf.test_x.numpy(),
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res["mase"]["bottom"], 20)

    def test_calculate_metrics_dict_x_scaled(self):
        model, like = self.gpf_scaled.train(epochs=10)
        preds, preds_scaled = self.gpf_scaled.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_complete=self.gpf.complete_x,
            x_original=self.gpf.train_x.numpy(),
            x_test=self.gpf.test_x.numpy(),
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res["mase"]["bottom"], 20)
