# Contribution Guidelines

1. Repo forks and clones
2. Make sure you have `git-flow` installed and initialized your repo using `git flow init`
3. Create features, bugfixes, etc.

    ```
    git flow feature start awesome-feature
    ```

4. Install dependencies

    ```
    poetry install
    ```

5. Initialize your repo with a pre-commit

    ```
    pre-commit install
    ```

6. Commit and publish your branch to the remote repository

    ```
    git flow feature publish awesome-feature
    ```

5. Create a pull request.
