
# GitHub Repository Scanner

This tool is designed to scan a GitHub repository and retrieve the contents of all files within it. It's implemented in Python and can be easily integrated into various projects, including CrewAI frameworks.

## Features

- Retrieves all files from a specified GitHub repository.
- Handles pagination for large repositories.
- Includes error handling for rate limits and invalid URLs.

## Requirements

- Python 3
- `requests` library
- A personal access token from GitHub stored as an environment variable `GITHUB_TOKEN`.

## Installation

Ensure you have Python 3 and the `requests` library installed. You can install `requests` using pip:

```bash
pip install requests
```

## Usage

1. **Setting Up the GitHub Token:**
   Set your GitHub personal access token as an environment variable:

   ```bash
   export GITHUB_TOKEN='your_personal_access_token'
   ```

2. **Importing the Class:**
   Import the `GitHubRepoScanner` class from its module.

3. **Instantiating the Scanner:**
   Create an instance of `GitHubRepoScanner` by passing the URL of the GitHub repository you want to scan.

   ```python
   from github_repo_scanner import GitHubRepoScanner

   scanner = GitHubRepoScanner("https://github.com/username/repo_name")
   ```

4. **Scanning the Repository:**
   Call the `scan_all_files` method to retrieve all files from the repository.

   ```python
   result = scanner.scan_all_files()
   print(result)
   ```

## Example

Here's a full example of how to use the tool:

```python
from github_repo_scanner import GitHubRepoScanner

# Instantiate the scanner with the repository URL
scanner = GitHubRepoScanner("https://github.com/username/repo_name")

# Scan the repository
result = scanner.scan_all_files()

# Handle the results
for file_name, content in result.items():
    print(f"File: {file_name}
Content: {content[:100]}...")  # Prints the first 100 characters of each file
```

## Note

- This tool is designed for educational and integration purposes and should be used in compliance with GitHub's API usage policies.
- Ensure that the GitHub token has the necessary permissions to access private repositories if required.

