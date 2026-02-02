"""Package uninstaller for Midna"""

import logging
import subprocess
from typing import List, Tuple

from .parser import parse_package_name, read_requirements


def uninstall_packages(requirements_file: str, dry_run: bool = False) -> int:
    """Uninstall packages from a requirements file using pip.

    Args:
        requirements_file: Path to requirements file
        dry_run: If True, only preview without uninstalling (default: False)

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    logger = logging.getLogger("midna")

    try:
        packages = read_requirements(requirements_file)
    except FileNotFoundError:
        logger.error(f"Requirements file not found: {requirements_file}")
        print(f"ERROR: Requirements file not found: {requirements_file}")
        return 1

    # Only uninstall packages that are actually installed
    found_packages, _ = _check_package_list_to_uninstall(packages)
    return _uninstall_package_list(found_packages, dry_run)


def _uninstall_package_list(packages: List[str], dry_run: bool = False) -> int:
    """Internal function to uninstall a list of packages.

    Args:
        packages: List of package names to uninstall
        dry_run: If True, only preview without uninstalling (default: False)

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    logger = logging.getLogger("midna")

    if not packages:
        print("No packages to uninstall.")
        logger.info("No packages to uninstall")
        return 0

    if dry_run:
        print("DRY RUN: Would uninstall the following packages:")
        for package in packages:
            package_name = parse_package_name(package)
            print(f"  - {package_name}")
        logger.info(
            f"Dry run completed. Would uninstall {len(packages)} packages"
        )
        return 0

    print(f"Uninstalling {len(packages)} packages...")
    logger.info(f"Starting uninstallation of {len(packages)} packages")

    # Extract just the package names (without version specifiers)
    package_names = [parse_package_name(pkg) for pkg in packages]

    # Uninstall packages
    cmd = ["pip", "uninstall", "-y"] + package_names
    logger.debug(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, shell=False
        )
        logger.info("Uninstallation completed successfully")
        print("Uninstallation completed successfully!")
        return result.returncode

    except subprocess.CalledProcessError as e:
        logger.error(f"Uninstallation failed with exit code {e.returncode}")
        print(f"ERROR: Uninstallation failed with exit code {e.returncode}")
        return e.returncode

    except KeyboardInterrupt:
        logger.warning("Uninstallation interrupted by user")
        print("\nWARNING: Uninstallation interrupted by user")
        return 130


def check_packages_to_uninstall(
    requirements_file: str,
) -> Tuple[List[str], List[str]]:
    """Check which packages from a requirements file are installed.

    Args:
        requirements_file: Path to requirements file

    Returns:
        Tuple of two lists: (installed_packages, not_installed_packages)

    Raises:
        FileNotFoundError: If the requirements file doesn't exist
    """
    logger = logging.getLogger("midna")
    logger.info("Checking packages for uninstallation...")

    try:
        packages = read_requirements(requirements_file)
    except FileNotFoundError:
        logger.error(f"Requirements file not found: {requirements_file}")
        raise

    return _check_package_list_to_uninstall(packages)


def _check_package_list_to_uninstall(
    packages: List[str],
) -> Tuple[List[str], List[str]]:
    """Check which packages in a list are installed."""
    logger = logging.getLogger("midna")

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
        installed_packages = set()

        for package in installed_raw:
            if "==" in package:
                name = package.split("==")[0].lower()
                installed_packages.add(name)

        logger.debug(f"Found {len(installed_packages)} installed packages")

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get installed packages: {e}")
        print("ERROR: Failed to check installed packages")
        raise

    found_packages = []
    not_found_packages = []

    for package in packages:
        package_name = parse_package_name(package).lower()

        if package_name in installed_packages:
            found_packages.append(package)
            logger.debug(f"Found for uninstall: {package}")
        else:
            not_found_packages.append(package)
            logger.debug(f"Not installed: {package}")

    logger.info(
        f"Packages found: {len(found_packages)}, "
        f"Not installed: {len(not_found_packages)}"
    )
    return found_packages, not_found_packages
