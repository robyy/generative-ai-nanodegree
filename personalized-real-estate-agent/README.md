# HomeMatch: Personalized Real Estate Agent

## Project Introduction
HomeMatch is an innovative application designed to revolutionize the real estate search process by providing personalized property listings. It leverages Large Language Models (LLMs) and vector databases to interpret buyer preferences and tailor property descriptions, making the home-buying journey more engaging and relevant to individual needs.

## Core Components

### 1. Listing Generation (`listing_generator.py`)
This module is responsible for generating synthetic real estate listings using the OpenAI API. These listings are saved to `listings.json` and serve as the data source for the application.

### 2. Storing Listings in a Vector Database (`database.py`)
This module initializes and interacts with ChromaDB, a vector database. It converts the generated real estate listings into embeddings using `sentence-transformers` and stores them in ChromaDB for efficient semantic search.

### 3. Building the User Preference Interface (`preference_parser.py`)
This module defines a set of questions to collect buyer preferences. It then structures these preferences into a query string that can be used to search the vector database. For demonstration purposes, buyer preferences are currently hardcoded.

### 4. Personalizing Listing Descriptions (`personalizer.py`)
For each retrieved listing, this module uses an LLM (OpenAI API) to augment the description. It tailors the description to resonate with the buyer's specific preferences, subtly emphasizing aspects that align with their needs without altering factual information.

### 5. Main Application (`HomeMatch.py`)
This is the main entry point of the application. It orchestrates the entire process: collecting buyer preferences, searching the vector database for matching listings, personalizing their descriptions, and presenting the results to the user.

## Setup and Installation

1.  **Clone the repository (if applicable. No public git repo for this project, just a zip):**
    ```bash
    git clone <repository_url>
    cd personalized-real-estate-agent
    ```

2.  **Create and activate a Python Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure OpenAI API Key:**
    Create a `.env` file in the root directory of the project and add your OpenAI API key and base URL:
    ```
    OPENAI_API_KEY="YOUR_API_KEY"
    OPENAI_API_BASE="https://api.openai.com/v1" # This is a special base URL for the provided key
    ```
    **Note:** The provided API key is a special one and only works with the specified `OPENAI_API_BASE` URL.

## How to Run

1.  **Generate Listings:**
    First, generate the synthetic real estate listings that will populate the database:
    ```bash
    python listing_generator.py
    ```
    This will create a `listings.json` file.

2.  **Initialize Database and Add Listings:**
    Next, initialize ChromaDB and add the generated listings to it. This step will also download the `sentence-transformers` model if it's not already cached.
    ```bash
    python database.py
    ```

3.  **Run the HomeMatch Application:**
    Finally, run the main application to get personalized real estate listings:
    ```bash
    python HomeMatch.py
    ```
    The application will print personalized listing descriptions to your console.

## Running Tests
To run the unit tests and ensure all components are working correctly, use pytest:
```bash
pytest
```

## Technologies Used
*   Python 3.13.5
*   OpenAI API (for LLM interactions)
*   ChromaDB (for vector database)
*   Sentence-Transformers (for embeddings)
*   Pytest (for testing)
*   python-dotenv (for environment variable management)