import os
from datetime import datetime, timezone, timedelta
import git

def read_date_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            date_str = file.readline().strip()
            return datetime.strptime(date_str, '%m/%d/%Y').date()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except ValueError:
        print(f"Invalid date format in the file {file_path}. Expected MM/DD/YYYY format.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def commit_to_git(repo_path, file_to_commit, commit_message, author_date):
    try:
        repo = git.Repo(repo_path)
        index = repo.index
        index.add([file_to_commit])

        author_date = author_date.replace(tzinfo=timezone.utc)

        index.commit(commit_message, author_date=author_date)
        print(f"Committed changes to '{file_to_commit}' with message: '{commit_message}' and timestamp: {author_date}")
    except git.exc.InvalidGitRepositoryError:
        print(f"The path '{repo_path}' is not a valid Git repository.")
    except Exception as e:
        print(f"An error occurred while committing to Git: {e}")

if __name__ == "__main__":
    date_file_path = 'date'
    repo_path = '.'
    file_to_commit = 'artwork'
    commit_message = ''
    author_date = None

    with open(file_to_commit, 'r') as file:
        lines = file.readlines()

    max_length = max(len(line) for line in lines)

    columns = [[] for _ in range(max_length)]

    for line in lines:
        for i, char in enumerate(line):
            columns[i].append(char if i < len(line) else ' ')

    characters = [char for column in columns for char in column]

    characters = [item for item in characters if "\n" not in item]

    date = read_date_from_file(date_file_path)

    if date:
        author_date = datetime.combine(date, datetime.min.time())
        commit_to_git(repo_path, "commit.py", "init commit", author_date)
        commit_to_git(repo_path, "date", "date commit", author_date)
        for char in characters:
            commit_message = f"Committing changes for {file_to_commit} on {author_date}"
            if char == '*':
                commit_to_git(repo_path, file_to_commit, commit_message, author_date)
            author_date += timedelta(days=1)
