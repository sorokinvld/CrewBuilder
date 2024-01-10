import os
import requests
from langchain.tools import tool

class GitHubRepoScanner:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}

    @tool
    def scan_all_files(self) -> dict:
        """
        Scans the GitHub repository and retrieves all files.

        Returns:
        - dict: A dictionary containing the contents of all files in the repository.
        """
        try:
            owner, repo = self.repo_url.split('/')[-2:]
        except IndexError:
            return {"error": "Invalid GitHub repository URL"}

        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        files_to_return = {}

        while True:
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                return {"error": "GitHub API rate limit reached"}
            elif response.status_code != 200:
                return {"error": "Failed to retrieve repository contents"}

            repo_contents = response.json()

            for file in repo_contents:
                if file['type'] == 'file':
                    file_response = requests.get(file['download_url'], headers=self.headers)
                    if file_response.status_code == 200:
                        files_to_return[file['name']] = file_response.text

            # Pagination handling
            if 'next' in response.links:
                api_url = response.links['next']['url']
            else:
                break

        return files_to_return
