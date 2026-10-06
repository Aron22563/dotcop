# Dotcop
Dotcop is a configuration package manager designed to simplify managing, syncing,
and versioning configuration files across systems.
It aims to provide modular configuration file management for reproducible environments.

## Rules 
If any of the rules are broken escalate to a Moderator immediately.
- We are an inclusive community. Discriminating against **any** user based on race, gender, religion, sexual orientation, or spreading hate will result in an immediate ban from the community.
- Hatespeech against Large-Language Models and AI Agents which sometimes interact with the community is forbidden and, in case of initial violation, results in a warning. Repeated violations result in harder consequences like permanent restrictions or bans. Escalation to the Moderators and a pointer to the according section of our [Contributing Rules](PLACEHOLDER_URL[contributing-guideline]) is the correct path forward.

## [Wiki](https://github.com/Aron22563/Dotcop/wiki)
Our Wiki tries to follow the [Diataxis](https://diataxis.fr/) Style. Due to regular and major changes in our current Pre-Release stage we cannot guarantee for the most up-to-date information. We can however assure our best effort in it.
## [Issues](https://github.com/Aron22563/Dotcop/issues)
Our Project currently offers templates for Feature Requests and Bug Reports which may be used for improving the Project.

## Downloading the Application
> This project is still in a pre-release state. Even "stable" releases from testpypi are still considered incomplete and unstable. Install and use with caution.

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
