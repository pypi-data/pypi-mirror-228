
# # Raga CLI (rc) - Data Version Control Tool

Raga CLI (rc) is a command-line tool built in Python for managing data version control. It allows you to track changes to datasets and models, create checkpoints, and manage repositories to ensure smooth collaboration and reproducibility in data-related projects.

## Installation

To install Raga CLI, make sure you have Python installed, and then run the following command:

```bash
pip install raga-cli
```

## Usage

Raga CLI provides several commands to help you manage your data version control tasks. Here are the available commands:

1. **Create a New Repository**
   ```bash
   rc repo create -n <repo_name> -tag <model/dataset>
   ```
   This command creates a new repository with the specified name and tags it as a model or dataset repository.

2. **Clone an Existing Repository**
   ```bash
   rc repo clone -n <repo_name>
   ```
   Use this command to clone an existing repository by providing the repository name.

3. **Show Repository Current Local Version**
   ```bash
   rc repo version
   ```
   Displays the current local version of the repository.

4. **Show Repository Information**
   ```bash
   rc repo info
   ```
   Provides information about the repository, including its name, type, and current version.

5. **Upload Files and Create Checkpoint**
   ```bash
   rc put -m "<commit message>"
   ```
   Uploads tracked files or directories to remote storage and creates a checkpoint with the specified commit message.

6. **Download Tracked Files or Directories**
   ```bash
   rc get
   ```
   Downloads files or directories that are tracked by Raga CLI.

7. **Download Files or Directories of a Specific Repo Version**
   ```bash
   rc get -repo-version <repo_version>
   ```
   Downloads files or directories of a particular version of the repository.

### Additional Flags

- `-h`, `--help`: Prints the usage/help message and exits.
- `-q`, `--quiet`: Suppresses standard output. Exits with 0 if no problems arise; otherwise, exits with 1.
- `-v`, `--verbose`: Displays detailed tracing information.

## Contributing

Contributions to Raga CLI are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/whoosh-labs/rctl).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---
