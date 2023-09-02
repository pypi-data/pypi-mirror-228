# testing Fibonacci number function
# pylint: skip-file
from ..lfsdata.git_data_loader import DataLoader


def test_download():
    DataLoader().gitlab_download("https://git.arusha.dev", 139, "lfs-lfsdata", "data/lfsdata.gz")
