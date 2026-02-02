"""Requirements file parser for Midna"""

import logging
import os
import sys
from typing import List

if sys.version_info >= (3, 11):
    from tomllib import load as _toml_load
else:
    from tomli import load as _toml_load


def read_requirements(file_path: str) -> List[str]:
    """Read and parse requirements from a file.

    Args:
        file_path: Path to requirements file (txt, toml, etc.)

    Returns:
        List of package specifications

    Raises:
        FileNotFoundError: If the requirements file doesn't exist
    """
    logger = logging.getLogger("midna")
    logger.info(f"Reading requirements from: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Requirements file not found: {file_path}")
        raise FileNotFoundError(f"Requirements file '{file_path}' not found.")

    # Handle TOML files
    if file_path.endswith(".toml"):
        try:
            return parse_toml_requirements(file_path)
        except ImportError as e:
            logger.warning(f"Failed to read {file_path}: {e}")
            # Fall back to treating it as a regular text file

    # Handle regular requirements files
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Error reading requirements file: {e}")
        raise

    packages = []
    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Handle -r includes (recursive requirements)
        if line.startswith("-r "):
            include_file = line[3:].strip()
            if not os.path.isabs(include_file):
                # Make relative path relative to current requirements file
                include_file = os.path.join(
                    os.path.dirname(file_path), include_file
                )

            logger.info(f"Found include: {include_file}")
            try:
                included_packages = read_requirements(include_file)
                packages.extend(included_packages)
            except FileNotFoundError:
                logger.warning(f"Included file not found: {include_file}")
                msg = (
                    f"WARNING: Included requirements file not found: "
                    f"{include_file}"
                )
                print(msg)
            continue

        # Skip other pip options
        if line.startswith("-"):
            logger.debug(f"Skipping pip option at line {line_num}: {line}")
            continue

        packages.append(line)
        logger.debug(f"Added package: {line}")

    logger.info(f"Found {len(packages)} packages in {file_path}")
    return packages


def parse_toml_requirements(file_path: str) -> List[str]:
    """Parse requirements from a TOML file (pyproject.toml).

    Args:
        file_path: Path to TOML file

    Returns:
        List of package specifications

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If TOML parsing fails
    """
    """Parse requirements from a TOML file (pyproject.toml)"""
    logger = logging.getLogger("midna")

    with open(file_path, "rb") as f:
        try:
            toml_data = _toml_load(f)
        except Exception as e:
            logger.error(f"Error parsing TOML file: {e}")
            raise

    packages = []

    # Get project dependencies
    project_data = toml_data.get("project", {})
    dependencies = project_data.get("dependencies", [])
    if dependencies:
        if isinstance(dependencies, list):
            packages.extend(dependencies)

    # Get optional dependencies
    optional_deps = project_data.get("optional-dependencies", {})
    for group, deps in optional_deps.items():
        if isinstance(deps, list):
            packages.extend(deps)

    # Get build system requirements
    build_system = toml_data.get("build-system", {})
    build_requires = build_system.get("requires", [])
    if build_requires:
        if isinstance(build_requires, list):
            packages.extend(build_requires)

    # Filter out any non-package entries (like keywords)
    # Keep basic requirements (pip, setuptools, wheel) and versioned packages
    packages = [
        pkg
        for pkg in packages
        if pkg in ["pip", "setuptools", "wheel"]
        or any(op in pkg for op in [">=", "==", "<=", "<", ">"])
    ]

    logger.info(f"Found {len(packages)} packages in TOML file")
    return packages


def parse_package_name(package_spec: str) -> str:
    """Extract package name from a package specification.

    Args:
        package_spec: Package specification (e.g., 'requests>=2.0.0', 'numpy==1.19.0')

    Returns:
        Package name without version specifiers
    """
    """Extract package name from package specification"""
    import re

    # Remove comments
    if "#" in package_spec:
        package_spec = package_spec.split("#")[0].strip()

    # Extract package name (everything before version specifiers)
    # Handle cases like: package>=1.0, package==1.0, package[extra]>=1.0
    pattern = r"^([a-zA-Z0-9_-]+(?:\[[a-zA-Z0-9_,-]+\])?)"
    match = re.match(pattern, package_spec)

    if match:
        return match.group(1).split("[")[0]  # Remove extras

    # Fallback: split on common version specifiers
    for separator in [">=", "<=", "==", "!=", ">", "<", "~="]:
        if separator in package_spec:
            return package_spec.split(separator)[0].strip()

    return package_spec.strip()
