import pytest
from unittest.mock import MagicMock, patch
from personalizer import ListingPersonalizer

@pytest.fixture
def personalizer_instance():
    return ListingPersonalizer()

def test_personalizer_initialization(personalizer_instance):
    assert personalizer_instance is not None

@patch('openai.ChatCompletion.create')
def test_personalize_listing(mock_chat_completion_create, personalizer_instance):
    # Mock the OpenAI API response
    mock_chat_completion_create.return_value = MagicMock(
        choices=[MagicMock(message={'content': "This is a personalized description."})]
    )

    sample_listing = {
        "neighborhood": "Sunnydale",
        "price": 650000,
        "bedrooms": 3,
        "bathrooms": 2,
        "house_size": 1800,
        "description": "A charming 3-bedroom home with a spacious living area and a small backyard. Located near a bustling downtown.",
        "neighborhood_description": "Sunnydale is known for its vibrant nightlife and diverse restaurants."
    }

    sample_preferences = "I am looking for a quiet neighborhood with good schools and a large backyard for my kids."

    personalized_desc = personalizer_instance.personalize_listing(sample_listing, sample_preferences)

    assert personalized_desc == "This is a personalized description."
    
    # Verify that openai.ChatCompletion.create was called with the correct arguments
    mock_chat_completion_create.assert_called_once()
    args, kwargs = mock_chat_completion_create.call_args
    assert kwargs['model'] == "gpt-3.5-turbo"
    assert "personalizing a property description" in kwargs['messages'][1]['content']
    assert "quiet neighborhood" in kwargs['messages'][1]['content']
