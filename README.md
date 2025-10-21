# Dotcop
Dotcop is a configuration package manager designed to simplify managing, syncing, 
and versioning configuration files across systems. 
It aims to provide modular configuration file management for reproducible environments.


## Downloading the Application
> [!IMPORTANT] This project is still in a pre-release state. Even "stable" releases from testpypi are still considered incomplete and unstable. Install and use with caution.

1. **Dependencies:**
   - `pip`
   - `pipx`

1. Download latest Stable version from testpypi
   ```bash
   pipx install --index-url https://test.pypi.org/simple/ --pip-args="--extra-index-url https://pypi.org/simple/" dotcop
   ```
1. Download the latest Pre-Release version from testpypi
   ```bash
   pipx install --index-url https://test.pypi.org/simple/ --pip-args="--extra-index-url https://pypi.org/simple/ --pre" dotcop
   ```
1. Uninstall dotcop
   ```bash
   pipx uninstall dotcop
   ```
   
## Additional Documentation

For more information please refer to the [Wiki](https://github.com/Aron22563/dotcop/wiki).
