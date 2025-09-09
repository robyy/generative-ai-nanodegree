from database import HomeMatchDB
from preference_parser import PreferenceParser
from personalizer import ListingPersonalizer

def main():
    print("Welcome to HomeMatch - Your Personalized Real Estate Agent!")

    # Initialize components
    db = HomeMatchDB()
    parser = PreferenceParser()
    personalizer = ListingPersonalizer()

    # 1. Get buyer preferences
    print("\nFirst, let's understand your preferences.")
    buyer_query_string = parser.get_query_string()

    print("\nSearching for properties that match your preferences...")

    # 2. Search for listings based on preferences
    search_results = db.search_listings(buyer_query_string, n_results=3)

    if not search_results or not search_results['metadatas'] or not search_results['metadatas'][0]:
        print("No matching listings found. Please try adjusting your preferences.")
        return

    print("\nHere are some personalized listings for you:")
    for i, listing_metadata in enumerate(search_results['metadatas'][0]):
        print(f"\n--- Personalized Listing {i+1} ---")
        
        # The metadata contains the original listing details
        original_listing = listing_metadata

        # 3. Personalize the listing description
        personalized_description = personalizer.personalize_listing(original_listing, buyer_query_string)

        print(f"Neighborhood: {original_listing['neighborhood']}")
        print(f"Price: ${original_listing['price']:,}")
        print(f"Bedrooms: {original_listing['bedrooms']}")
        print(f"Bathrooms: {original_listing['bathrooms']}")
        print(f"House Size: {original_listing['house_size']:,} sqft")
        print(f"\nPersonalized Description:\n{personalized_description}")
        print(f"\nNeighborhood Description:\n{original_listing['neighborhood_description']}")

if __name__ == "__main__":
    main()