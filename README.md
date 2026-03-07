# ReconFlow (Bug Bounty OS)

ReconFlow is a centralized, lightweight platform designed for Bug Bounty teams to collaborate efficiently, prevent duplicate efforts, and manage targets.

## Features
- **Duplicate Prevention:** Asset locking system using CLI commands.
- **Centralized Dashboard:** Live tracking of assets and team activities.

## Usage (CLI)
- Claim an asset: `python3 cli/hunt.py claim api.target.com`
- Release an asset: `python3 cli/hunt.py release api.target.com`
