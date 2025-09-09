import json
import os
from unittest.mock import patch

import pytest

from database import HomeMatchDB

# Define a temporary listings file for testing
TEST_LISTINGS_FILE = "test_listings.json"
TEST_DB_PATH = "./test_chroma_db"


@pytest.fixture(scope="module")
def setup_test_listings():
    test_data = [
        {
            "neighborhood": "Quiet Meadows",
            "price": 500000,
            "bedrooms": 3,
            "bathrooms": 2,
            "house_size": 1800,
            "description": "A cozy family home in a peaceful neighborhood with a large backyard.",
            "neighborhood_description": "Quiet Meadows is known for its excellent schools and family-friendly parks."
        },
        {
            "neighborhood": "City Central",
            "price": 750000,
            "bedrooms": 2,
            "bathrooms": 2,
            "house_size": 1200,
            "description": "Modern downtown apartment with great city views, perfect for urban living.",
            "neighborhood_description": "City Central offers vibrant nightlife, restaurants, and easy access to public transport."
        }
    ]
    with open(TEST_LISTINGS_FILE, "w") as f:
        json.dump(test_data, f, indent=4)
    yield
    os.remove(TEST_LISTINGS_FILE)


@pytest.fixture(scope="module")
def homedb_instance():
    # Clean up any previous test DB
    if os.path.exists(TEST_DB_PATH):
        import shutil
        shutil.rmtree(TEST_DB_PATH)
    db = HomeMatchDB(path=TEST_DB_PATH)
    yield db
    # Clean up after tests
    if os.path.exists(TEST_DB_PATH):
        import shutil
        shutil.rmtree(TEST_DB_PATH)


def test_db_initialization(homedb_instance):
    assert homedb_instance.client is not None
    assert homedb_instance.collection is not None
    assert homedb_instance.model is not None


@patch('database.SentenceTransformer')
def test_add_listings(mock_sentence_transformer, homedb_instance, setup_test_listings):
    # Mock the SentenceTransformer to prevent actual model loading during this test
    mock_sentence_transformer.return_value.encode.return_value = [0.1, 0.2, 0.3]  # Dummy embedding

    homedb_instance.add_listings(listings_file=TEST_LISTINGS_FILE)

    # Verify listings were added
    count = homedb_instance.collection.count()
    assert count == 2

    # Verify content of one added listing (check metadata)
    results = homedb_instance.collection.get(ids=["listing_0"], include=['metadatas'])
    assert results['metadatas'][0]['neighborhood'] == "Quiet Meadows"


@patch('database.SentenceTransformer')
def test_search_listings(mock_sentence_transformer, homedb_instance, setup_test_listings):
    # Ensure listings are added before searching
    mock_sentence_transformer.return_value.encode.return_value = [0.1, 0.2, 0.3]  # Dummy embedding
    homedb_instance.add_listings(listings_file=TEST_LISTINGS_FILE)

    # Mock the embedding for the query
    mock_sentence_transformer.return_value.encode.return_value = [0.1, 0.2, 0.3]  # Dummy embedding for query

    query = "family home with a big backyard"
    search_results = homedb_instance.search_listings(query, n_results=1)

    assert len(search_results['metadatas'][0]) == 1
    assert search_results['metadatas'][0][0]['neighborhood'] == "Quiet Meadows"
