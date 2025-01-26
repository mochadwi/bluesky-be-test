# Pokemon API Project

A FastAPI-based Pokemon API that scrapes data from PokeAPI and provides endpoints to manage Pokemon information.

## Project Overview

This project implements a Pokemon API service that:
- Scrapes Pokemon data from the official PokeAPI
- Stores Pokemon information in a SQLite database
- Provides REST API endpoints to manage Pokemon data

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLite**: Lightweight database for storing Pokemon data
- **httpx**: Async HTTP client for making API requests
- **Poetry**: Python dependency management

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── database.py    # Database operations and schema
│   ├── main.py        # FastAPI application and routes
│   ├── model.py       # Data models
│   └── scraper.py     # Pokemon data scraper
├── poetry.lock
├── pyproject.toml
├── pokemon.db         # SQLite database
└── pokemon_api_collection.json  # API collection for testing
```

## Database Schema

### Tables

1. **pokemon**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT NOT NULL UNIQUE)

2. **types**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT NOT NULL UNIQUE)

3. **pokemon_types** (Junction Table)
   - pokemon_id (INTEGER, FK)
   - type_id (INTEGER, FK)
   - slot (INTEGER NOT NULL)

## API Endpoints

1. **GET /** 
   - Health check endpoint
   - Returns: `{"message": "Hi this is Pokemon API"}`

2. **GET /api/pokemon**
   - Retrieves all Pokemon with their types
   - Returns: List of Pokemon with their attributes

3. **POST /api/pokemon/scrape**
   - Triggers Pokemon data scraping from PokeAPI
   - Query Parameter: `limit` (default: 100)
   - Returns: Success message

## Setup Instructions

1. **Prerequisites**
   - Python 3.7+
   - Poetry

2. **Installation**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd bluesky_fullstack_test

   # Install dependencies
   poetry install

   # Activate virtual environment
   poetry shell
   ```

3. **Running the Application**
   ```bash
   # Start the FastAPI server
   uvicorn src.main:app --reload
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints for better code readability
   - Document functions and classes with docstrings

2. **Database Operations**
   - Use context managers for database connections
   - Implement proper error handling and rollbacks
   - Maintain referential integrity

3. **API Development**
   - Follow REST principles
   - Implement proper error handling
   - Use Pydantic models for request/response validation

## Assumptions

1. **Data Source**
   - PokeAPI is the primary data source
   - API rate limits are respected
   - Basic Pokemon information (id, name, types) is sufficient

2. **Performance**
   - SQLite is sufficient for the current scale
   - Async operations for external API calls
   - Batch processing for data scraping

## Limitations

1. **Database**
   - SQLite might not be suitable for high concurrency
   - No built-in backup mechanism
   - Limited to basic Pokemon information

2. **API**
   - No authentication/authorization
   - Limited error handling
   - No pagination for large datasets

## Future Improvements

1. **Features**
   - Add authentication/authorization
   - Implement rate limiting
   - Add more Pokemon attributes (stats, abilities, etc.)
   - Add CRUD operations for Pokemon

2. **Technical**
   - Migrate to a more robust database (PostgreSQL)
   - Add API versioning
   - Implement caching
   - Add comprehensive test suite
   - Add CI/CD pipeline

3. **Documentation**
   - Add API documentation examples
   - Include performance metrics
   - Add deployment guide

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.