import json
import openai
from config import ***REMOVED***, OPENAI_API_BASE

openai.api_key = ***REMOVED***
openai.api_base = OPENAI_API_BASE

def generate_listings(num_listings=10):
    """
    Generates a specified number of real estate listings using the OpenAI API.

    Args:
        num_listings (int): The number of listings to generate.

    Returns:
        list: A list of generated real estate listings.
    """
    prompt = f"""
    Generate {num_listings} diverse real estate listings in valid JSON format. Each listing should be an object with the following fields:
    - "neighborhood": string
    - "price": integer
    - "bedrooms": integer
    - "bathrooms": integer
    - "house_size": integer (in square feet)
    - "description": string
    - "neighborhood_description": string

    Example:
    {{
        "neighborhood": "Green Oaks",
        "price": 800000,
        "bedrooms": 3,
        "bathrooms": 2,
        "house_size": 2000,
        "description": "Welcome to this eco-friendly oasis nestled in the heart of Green Oaks. This charming 3-bedroom, 2-bathroom home boasts energy-efficient features such as solar panels and a well-insulated structure. Natural light floods the living spaces, highlighting the beautiful hardwood floors and eco-conscious finishes. The open-concept kitchen and dining area lead to a spacious backyard with a vegetable garden, perfect for the eco-conscious family. Embrace sustainable living without compromising on style in this Green Oaks gem.",
        "neighborhood_description": "Green Oaks is a close-knit, environmentally-conscious community with access to organic grocery stores, community gardens, and bike paths. Take a stroll through the nearby Green Oaks Park or grab a cup of coffee at the cozy Green Bean Cafe. With easy access to public transportation and bike lanes, commuting is a breeze."
    }}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a real estate listing generator. Your output should be a valid JSON array of listings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        listings_text = response.choices[0].message['content']
        listings = json.loads(listings_text)
        return listings
    except Exception as e:
        print(f"Error generating listings: {e}")
        return None

if __name__ == "__main__":
    generated_listings = generate_listings(10)
    if generated_listings:
        with open("listings.json", "w") as f:
            json.dump(generated_listings, f, indent=4)
        print("Successfully generated and saved 10 real estate listings to listings.json.")