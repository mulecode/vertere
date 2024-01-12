"""
Module to handle git repository operations
"""
import os
from os import path

from git import Repo


class GitRepository(object):
    """
    Class to handle git repository operations
    """

    def __init__(self):
        self.git_repository = Repo('.git')

    def validate_git_initialised(self) -> None:
        """
        Validate if git is initialized
        """
        pwd = os.getcwd()
        git_initialised = path.exists(f"{pwd}/.git")
        if not git_initialised:
            raise GitRepositoryNotInitialisedException(f"Path for {pwd}/.git not initialized.")

    def get_tags(self):
        tags = self.git_repository.tags
        return list(tags)

    def get_head_commit(self) -> str:
        """
        Get head commit
        :return: Commit hash
        """
        try:
            return str(self.git_repository.head.commit)
        except Exception as e:
            raise GitRepositoryHeadCommitException(f"Failed to retrieve head commit - {e}")

    def is_tag_head(self, tag_name: str):
        head_commit = self.get_head_commit()
        commit_by_tag = self.git_repository.commit(tag_name)
        if str(head_commit) == str(commit_by_tag):
            return True
        return False

    def tag(self, tag_name: str):
        self.git_repository.create_tag(tag_name, force=True)
        remote = self.git_repository.remote(name='origin')
        remote.push(refspec=tag_name)
        print(f'Tag {tag_name} pushed.')

    def delete_tag(self, tag_name: str):
        try:
            self.git_repository.delete_tag(tag_name)
            remote = self.git_repository.remote(name='origin')
            remote.push(refspec=f':{tag_name}')
            print(f'Tag {tag_name} deleted.')
        except Exception as e:
            print(f'Error deleting the tag - {e}')


class GitRepositoryNotInitialisedException(Exception):
    """Git not initialized"""
    pass


class GitRepositoryHeadCommitException(Exception):
    """Head commit not found"""
    pass
