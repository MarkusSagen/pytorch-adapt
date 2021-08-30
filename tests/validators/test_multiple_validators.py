import unittest

import torch

from pytorch_adapt.validators import (
    DeepEmbeddedValidator,
    MultipleValidators,
    SilhouetteScoreValidator,
)


class TestMultipleValidators(unittest.TestCase):
    def test_multiple_validators(self):
        v1 = SilhouetteScoreValidator()
        v2 = DeepEmbeddedValidator()

        for i, weights in enumerate([None, [1, 5]]):
            validator = MultipleValidators([v1, v2], weights)
            required_data = validator.required_data
            self.assertTrue(
                set(required_data) == {"target_train", "src_train", "src_val"}
            )
            self.assertTrue(len(required_data) == len(set(required_data)))

            dataset_size = 1000
            features = torch.randn(dataset_size, 512)
            src_train = {"features": features}

            features = torch.randn(dataset_size, 512)
            logits = torch.randn(dataset_size, 10)
            labels = torch.randint(0, 10, (dataset_size,))
            src_val = {"features": features, "logits": logits, "labels": labels}

            features = torch.randn(dataset_size, 512)
            logits = torch.randn(dataset_size, 10)
            target_train = {"features": features, "logits": logits}

            validator.score(
                epoch=i, src_train=src_train, src_val=src_val, target_train=target_train
            )

            actual_weights = weights
            if actual_weights is None:
                actual_weights = [1, -1]
            self.assertTrue(
                validator.latest_score
                == (
                    v1.latest_score * actual_weights[0]
                    + v2.latest_score * actual_weights[1]
                )
            )
