import os
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse

from loguru import logger
from DB.models.documents import RepositoryDocument
from .baseCrawler import BaseCrawler

class GithubCrawler(BaseCrawler):
    model = RepositoryDocument

    def __init__(self, ignore=(".git", ".toml", ".lock", ".png")) -> None:
        super().__init__()
        self._ignore = ignore

    @staticmethod
    def is_repo_url(link: str) -> bool:
        """Check if GitHub URL points to a repo (not profile)."""
        p = urlparse(link)
        if "github.com" not in p.netloc:
            return False
        parts = [seg for seg in p.path.split("/") if seg]
        return len(parts) >= 2

    def extract(self, link: str, **kwargs) -> None:
        if not self.is_repo_url(link):
            logger.warning(f"Skipping non-repo GitHub URL: {link}")
            return

        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Repository already exists in the database: {link}")
            return

        logger.info(f"Starting scrapping GitHub repository: {link}")

        repo_name = link.rstrip("/").split("/")[-1]

        local_temp = tempfile.mkdtemp(prefix="github_repo_")
        try:
            repo_process = subprocess.run(
                ["git", "clone", link],
                cwd=local_temp,
                capture_output=True,
                text=True
            )

            if repo_process.returncode != 0:
                logger.error(f"Git clone failed for {link}: {repo_process.stderr.strip()}")
                return

            repo_dir = os.path.join(local_temp, os.listdir(local_temp)[0])

            tree = {}
            for root, _, files in os.walk(repo_dir):
                rel_dir = os.path.relpath(root, repo_dir)
                if any(rel_dir.startswith(ignore) for ignore in self._ignore):
                    continue

                for file in files:
                    if file.endswith(self._ignore):
                        continue
                    file_path = os.path.join(rel_dir, file)
                    try:
                        with open(os.path.join(root, file), "r", errors="ignore") as f:
                            tree[file_path] = f.read().replace(" ", "")
                    except Exception:
                        logger.warning(f"Skipping unreadable file: {file_path}")

            user = kwargs["user"]
            instance = self.model(
                content=tree,
                name=repo_name,
                link=link,
                platform="github",
                author_id=user.id,
                author_full_name=user.full_name,
            )
            instance.save()

        except Exception as e:
            logger.exception(f"Failed to extract repository {link}: {e}")
        finally:
            shutil.rmtree(local_temp, ignore_errors=True)

        logger.info(f"Finished scrapping GitHub repository: {link}")
