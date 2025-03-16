# CLAUDE.md - Repository Guide

## Commands
- No build commands required (Python only)
- Run scripts: `python3 <script_name>.py`
- No testing framework implemented

## Code Style Guidelines
- Follow PEP 8 style conventions
- Indentation: 4 spaces
- Variable/function naming: snake_case
- Constants: UPPER_CASE
- Docstrings: Triple quotes with Args/Returns sections
- Imports: Standard library first, then third-party, then local
- Error handling: Use try/except blocks with specific exceptions
- Comments: Explain complex algorithms and logic
- Progress reporting for long-running operations

## Data Processing Patterns
- Use chunked processing for large files
- Validate geographic coordinates with try/except
- Define data structures at the top of files
- Properly close file handles with context managers

This repository contains scripts for processing GeoJSON data of world cities, specifically for filtering and extracting European cities.