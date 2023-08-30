# dot.py
`dot.py` is a python script to help you manage your dotfiles without overhead

## What does it do
`dot.py` is a little configurable script that you can store next to your dotfiles and run each time you have freshly
installed OS. All you need for this to run is `python3` installation, no additional packages are needed.


> Bit of terminology:  
> **Source** - directory or file that is being copied
> **Destination** - directory or file where files are copied

## Advantages
- _Single-file_. All you need is the script itself and python, which comes pre-installed almost with any linux distro.
- _VCS-friendly_. You don't need any dotfiles managers, because `dot.py` can link files for you. So, you can just edit files
in your repository and the changes will be reflected in destinations.
- When adding new files into your repository, all you need to reflect changes to destinations is to rerun the script.

## How to start.
First things first, you need `bot.py` script. Just copy it from this repository.  
Then, you probably want to check script settings. Open the script in your favorite text editor, you'll see something like
this near the top of the file:

```python
class Settings:
    # Will copy files instead of sym-linking them (not VCS-friendly)
    use_copy = False
    use_gitignore = True  # Ignore files from .gitignore

    # Syntax:
    #  ("source path to file / directory with files", "destination file to file / directory")
    # NOTE:
    #  - Specifying directory as a source will copy children to destination: <src>/* -> <dst dir>/
    #  - Copying file to directory follows the same logic as the `cp` command
    #  - Copying directory to file is not allowed
    paths = [
        (".", "~/.config"),
        (".bashrc", "~"),
    ]
    ignored = []  # Patters to ignore (relative to source directories, follows gitignore format)
```

Everything is pretty easy. The most interesting spot for you is `paths` variable, this tells the script which files to copy and where to copy them. You can copy whole directory or single file

## Running
When you're happy with your config, you can run this script like this:
```bash
./dot.py
# or
python3 dot.py
```

# WARNING
Make sure you back up all the files you have in destination folders because the script will remove any conflicting files