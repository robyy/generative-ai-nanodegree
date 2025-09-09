import openai

from config import OPENAI_API_KEY, OPENAI_API_BASE


class ListingPersonalizer:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        openai.api_base = OPENAI_API_BASE

    def personalize_listing(self, listing, buyer_preferences_string):
        """
        Personalizes a real estate listing description based on buyer preferences.

        Args:
            listing (dict): The original listing dictionary.
            buyer_preferences_string (str): A string summarizing the buyer's preferences.

        Returns:
            str: The personalized listing description.
        """
        original_description = listing['description']
        neighborhood_description = listing['neighborhood_description']

        prompt = f"""
        You are a real estate agent tasked with personalizing a property description for a potential buyer.
        The buyer's preferences are: {buyer_preferences_string}

        Here is the original property description:
        {original_description}

        Here is the neighborhood description:
        {neighborhood_description}

        Rewrite the property description to highlight aspects most relevant to the buyer's preferences.
        Ensure you do NOT alter any factual information about the property (e.g., number of bedrooms, bathrooms, price, size).
        Focus on emphasizing features that align with the buyer's stated needs and desires.
        The personalized description should be engaging and persuasive.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful real estate agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            personalized_description = response.choices[0].message['content']
            return personalized_description
        except Exception as e:
            print(f"Error personalizing listing: {e}")
            return original_description  # Return original if personalization fails


if __name__ == "__main__":
    # Example Usage (for testing the personalizer independently)
    personalizer = ListingPersonalizer()

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

    personalized_desc = personalizer.personalize_listing(sample_listing, sample_preferences)
    print("\nOriginal Description:")
    print(sample_listing['description'])
    print("\nPersonalized Description:")
    print(personalized_desc)
