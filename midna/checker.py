"""Package installation checker for Midna"""

import logging
import subprocess
from typing import List, Set, Tuple

from .parser import parse_package_name


def check_installed_packages(
    packages: List[str],
) -> Tuple[List[str], List[str]]:
    """Check which packages are installed and which are missing.

    Args:
        packages: List of package names to check

    Returns:
        Tuple of two lists: (missing_packages, already_installed)

    Raises:
        subprocess.CalledProcessError: If pip list command fails
    """
    logger = logging.getLogger("midna")
    logger.info("Checking installed packages...")

    try:
        # Get list of installed packages
        result = subprocess.run(
            ["pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        )

        installed_raw = (
            result.stdout.strip().split("\n") if result.stdout.strip() else []
        )
        installed_packages: Set[str] = set()

        for package in installed_raw:
            if "==" in package:
                name = package.split("==")[0].lower()
                installed_packages.add(name)

        logger.debug(f"Found {len(installed_packages)} installed packages")

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get installed packages: {e}")
        print("ERROR: Failed to check installed packages")
        raise

    missing_packages = []
    already_installed = []

    for package in packages:
        package_name = parse_package_name(package).lower()

        if package_name in installed_packages:
            already_installed.append(package)
            logger.debug(f"Already installed: {package}")
        else:
            missing_packages.append(package)
            logger.debug(f"Missing: {package}")

    logger.info(
        f"Missing packages: {len(missing_packages)}, "
        f"Already installed: {len(already_installed)}"
    )
    return missing_packages, already_installed
