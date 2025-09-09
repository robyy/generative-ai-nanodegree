class PreferenceParser:
    def __init__(self):
        self.questions = [
            "How big do you want your house to be?",
            "What are 3 most important things for you in choosing this property?",
            "Which amenities would you like?",
            "Which transportation options are important to you?",
            "How urban do you want your neighborhood to be?",
        ]
        self.answers = [
            "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
            "A quiet neighborhood, good local schools, and convenient shopping options.",
            "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
            "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
            "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
        ]

    def get_preferences(self):
        # In a real application, this would be interactive input from the user.
        # For now, we use hardcoded answers as per the project description.
        return dict(zip(self.questions, self.answers))

    def get_query_string(self):
        preferences = self.get_preferences()
        query_parts = []
        for q, a in preferences.items():
            query_parts.append(f"{q} {a}")
        return " ".join(query_parts)


if __name__ == "__main__":
    parser = PreferenceParser()
    preferences = parser.get_preferences()
    print("Buyer Preferences:")
    for q, a in preferences.items():
        print(f"- {q}\n  {a}")

    query_string = parser.get_query_string()
    print(f"\nCombined Query String: {query_string}")
