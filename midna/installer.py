"""Package installer for Midna"""

import logging
import subprocess
from typing import List


def install_packages(packages: List[str], dry_run: bool = False) -> int:
    """Install packages using pip.

    Args:
        packages: List of package names to install
        dry_run: If True, only preview without installing (default: False)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    logger = logging.getLogger("midna")

    if not packages:
        print("No packages to install.")
        logger.info("No packages to install")
        return 0

    if dry_run:
        print("DRY RUN: Would install the following packages:")
        for package in packages:
            print(f"  - {package}")
        logger.info(
            f"Dry run completed. Would install {len(packages)} packages"
        )
        return 0

    print(f"Installing {len(packages)} packages...")
    logger.info(f"Starting installation of {len(packages)} packages")

    # Install packages
    cmd = ["pip", "install"] + packages
    logger.debug(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, shell=False
        )
        logger.info("Installation completed successfully")
        print("Installation completed successfully!")
        return result.returncode

    except subprocess.CalledProcessError as e:
        logger.error(f"Installation failed with exit code {e.returncode}")
        print(f"ERROR: Installation failed with exit code {e.returncode}")
        return e.returncode

    except KeyboardInterrupt:
        logger.warning("Installation interrupted by user")
        print("\nWARNING: Installation interrupted by user")
        return 130
