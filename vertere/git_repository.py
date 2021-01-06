import os
from git import Repo
from os import path


class GitRepository(object):
    def __init__(self):
        self.git_repository = Repo('.git')

    def validate_git_initialised(self):
        pwd = os.getcwd()
        git_initialised = path.exists(f'{pwd}/.git')
        if not git_initialised:
            raise GitRepositoryNotInitialisedException()

    def get_tags(self):
        tags = self.git_repository.tags
        return list(tags)

    def is_tag_head(self, tag_name: str):
        head_commit = self.git_repository.head.commit
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
    """Git not initialised"""
    pass
