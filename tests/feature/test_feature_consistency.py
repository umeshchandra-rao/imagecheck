"""
Test feature extraction consistency.
Verifies that the same image always produces the same feature vector.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ml.unified_feature_extractor import UnifiedFeatureExtractor


@pytest.fixture(scope="module")
def extractor():
    return UnifiedFeatureExtractor(feature_dim=512)


def _random_rgb_image():
    """Generate a deterministic synthetic RGB image for testing."""
    from PIL import Image

    rng = np.random.RandomState(123)
    arr = rng.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


class TestFeatureConsistency:
    def test_same_image_same_features(self, extractor):
        """Extracting features from the same image twice should give identical results."""
        image = _random_rgb_image()
        features_a = extractor.extract_features(image)
        features_b = extractor.extract_features(image)
        np.testing.assert_allclose(features_a, features_b, atol=1e-6)

    def test_feature_vector_is_normalized(self, extractor):
        """Feature vectors should be L2-normalized."""
        image = _random_rgb_image()
        features = np.array(extractor.extract_features(image))
        norm = np.linalg.norm(features)
        assert abs(norm - 1.0) < 1e-5, f"Expected unit norm, got {norm}"

    def test_output_dimension(self, extractor):
        """Output dimension should match the configured feature_dim."""
        image = _random_rgb_image()
        features = extractor.extract_features(image)
        assert len(features) == extractor.feature_dim

    def test_different_images_different_features(self, extractor):
        """Distinct images should produce distinct feature vectors."""
        from PIL import Image

        img_a = _random_rgb_image()
        rng2 = np.random.RandomState(456)
        arr2 = rng2.randint(0, 256, (224, 224, 3), dtype=np.uint8)
        img_b = Image.fromarray(arr2, "RGB")

        fa = np.array(extractor.extract_features(img_a))
        fb = np.array(extractor.extract_features(img_b))
        similarity = float(np.dot(fa, fb))
        assert similarity < 0.99, (
            f"Distinct images should not be near-identical (similarity={similarity})"
        )
