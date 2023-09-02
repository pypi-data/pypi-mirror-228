# pylint: skip-file
import logging
import os
import pathlib
import urllib.parse
import requests
from tqdm import tqdm


class DataLoader:
    """

    The DataLoader class is responsible for downloading files from GitLab and GitHub.

    Attributes:
    - logger: A logger instance for logging messages.
    - headers: A dictionary containing the headers for the HTTP requests.

    Methods:
    - __init__(self): Initializes a new instance of the DataLoader class.
    - gitlab_download(self, host, project_id, branch_name, file_path):
        Downloads a file from GitLab and saves it to the local filesystem.
    - github_download(self, host, project_id, branch_name, file_path):
        Downloads a file from GitHub and saves it to the local filesystem.
    - __file_write(self, destination, response):
        Writes the response content to a file specified by the destination path.
    - __make_request(self, lfs_url): Sends a GET request to the specified URL and returns the response object.

    """

    def __init__(self):
        """
        Initializes a new instance of the DataLoader class.
        """
        self.logger = logging.getLogger(__name__)

        self.headers = {
            "Private-Token": os.getenv("GITLAB_ACCESS_TOKEN")
        }
        if not self.headers["Private-Token"]:
            self.logger.warning("Access token didn't set")

    def gitlab_download(self, host: str, project_id: int, branch_name: str, file_path: str) -> str | None:
        """
            Downloads a file from GitLab and saves it to the local filesystem.

            :param host: The URL of the GitLab server.
            :param project_id: The ID of the GitLab project.
            :param branch_name: The name of the branch in the GitLab project.
            :param file_path: The path to the file in the GitLab project.
            :return: The local path of the downloaded file if successful, otherwise None.
        """

        try:
            destination = pathlib.Path.home().joinpath(f".local/datasets/{str(project_id)}/{branch_name}/{file_path}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temp_destination = pathlib.Path.home().joinpath(
                f".local/datasets/{project_id}/{branch_name}/{file_path}.temp")
            if destination.exists():
                return str(destination)
            self.logger.debug(f"Downloading from {host}/{project_id}/{branch_name}/{file_path}...")
            lfs_url = f"{host}/api/v4/projects/{str(project_id)}/" \
                      f"repository/files/{urllib.parse.quote_plus(file_path)}" \
                      f"/raw?ref={branch_name}&lfs=True"
            response = self.__make_request(lfs_url)
            if response.status_code == 200:
                self.logger.debug("Request successful!")
                self.__file_write(temp_destination, response)
            else:
                self.logger.debug(
                    f"Request failed with status code: {response.status_code}\nResponse Text: {response.text}")
            os.rename(temp_destination, destination)
            return str(destination)
        except Exception as exception:
            self.logger.debug(
                f"Downloading from {host}/{project_id}/{branch_name}/{file_path} failed", exception)
            return None

    def github_download(self, host: str, project_id: int, branch_name: str, file_path: str) -> str | None:
        """
        Downloads a file from a GitHub repository.

        Args:
            host (str): The GitHub host, e.g. "https://github.com".
            project_id (int): The project ID or repository name.
            branch_name (str): The branch name.
            file_path (str): The path to the file relative to the root directory of the repository.

        Returns:
            str | None: The local file path if the download is successful, else None.

        """
        pass

    @staticmethod
    def __file_write(destination: pathlib.Path, response: requests.Response):
        """
        Writes the response content to a file specified by the destination path.

        :param destination: The path of the file to write to.
        :param response: The response object containing the content to write.
        :return: None
        """
        with open(destination, 'wb') as dest_file:
            total_length = int(response.headers.get('content-length'))
            chunks = tqdm(response.iter_content(chunk_size=1024), total=(total_length / 1024) + 1)
            for chunk in filter(None, chunks):
                dest_file.write(chunk)
                dest_file.flush()

    def __make_request(self, lfs_url: str) -> requests.Response:
        """
        Sends a GET request to the specified URL and returns the response object.

        :param lfs_url: The URL to which the request will be sent.
        :type lfs_url: str
        :return: The response object of the GET request.
        :rtype: requests.Response
        """
        return requests.get(lfs_url, headers=self.headers, stream=True)
