"""Auto-discovery for Midna - find requirements automatically"""

import ast
import logging
import os
from pathlib import Path
from typing import List, Set, Tuple

from .package_classifier import classify_packages


def find_requirements_files(directory: str = ".") -> List[str]:
    """Find requirements files in the given directory.

    Args:
        directory: Path to directory to search (default: current directory)

    Returns:
        List of paths to found requirements files
    """
    logger = logging.getLogger("midna")

    # Common requirements file patterns
    patterns = [
        "requirements.txt",
        "requirements*.txt",
        "pyproject.toml",
        "setup.py",
        "Pipfile",
        "environment.yml",
        "conda.yml",
    ]

    found_files = []
    dir_path = Path(directory)

    # Look for requirements files
    for pattern in patterns:
        if "*" in pattern:
            for file_path in dir_path.glob(pattern):
                if file_path.is_file():
                    found_files.append(str(file_path))
                    logger.info(f"Found requirements file: {file_path}")
        else:
            file_path = dir_path / pattern
            if file_path.exists():
                found_files.append(str(file_path))
                logger.info(f"Found requirements file: {file_path}")

    return found_files


def extract_imports_from_file(file_path: str) -> Set[str]:
    """Extract import statements from a Python file.

    Args:
        file_path: Path to the Python file to analyze

    Returns:
        Set of imported top-level package names
    """
    logger = logging.getLogger("midna")
    imports: Set[str] = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError as e:
                logger.warning(f"Syntax error in {file_path}: {e}")
                return imports

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Get the top-level package name
                    package = alias.name.split(".")[0]
                    imports.add(package)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Get the top-level package name
                    package = node.module.split(".")[0]
                    imports.add(package)

    except Exception as e:
        logger.warning(f"Error reading {file_path}: {e}")

    return imports


def find_python_files(directory: str = ".") -> List[str]:
    """Find all Python files in directory and subdirectories.

    Args:
        directory: Root directory to search (default: current directory)

    Returns:
        List of paths to Python (.py) files, excluding common build/cache directories
    """
    python_files = []

    # Skip common directories that shouldn't be scanned
    skip_dirs = {
        ".git",
        ".svn",
        ".hg",  # VCS
        "__pycache__",
        ".pytest_cache",  # Cache
        ".venv",
        "venv",
        "env",  # Virtual environments
        "node_modules",  # JS dependencies
        ".tox",
        ".mypy_cache",  # Tools
        "build",
        "dist",
        ".eggs",  # Build artifacts
    }

    for root, dirs, files in os.walk(directory):
        # Remove skip directories from dirs list
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def analyze_project_imports(directory: str = ".") -> Set[str]:
    """Analyze all Python files in project to find imported packages.

    Args:
        directory: Root directory to analyze (default: current directory)

    Returns:
        Set of third-party package names found in imports
    """
    logger = logging.getLogger("midna")
    logger.info(f"Analyzing Python files in: {directory}")

    all_imports = set()
    python_files = find_python_files(directory)

    logger.info(f"Found {len(python_files)} Python files to analyze")

    for file_path in python_files:
        imports = extract_imports_from_file(file_path)
        all_imports.update(imports)
        if imports:
            logger.debug(f"Imports from {file_path}: {imports}")

    # Filter out standard library modules
    filtered_imports = filter_standard_library(all_imports)

    logger.info(
        f"Found {len(filtered_imports)} potential third-party packages"
    )
    return filtered_imports


def filter_standard_library(imports: Set[str]) -> Set[str]:
    """Filter out Python standard library modules.

    Args:
        imports: Set of import names to filter

    Returns:
        Set of non-stdlib package names
    """

    # Common standard library modules (not exhaustive but covers most)
    stdlib_modules = {
        "os",
        "sys",
        "json",
        "re",
        "math",
        "random",
        "datetime",
        "time",
        "pathlib",
        "collections",
        "itertools",
        "functools",
        "operator",
        "typing",
        "dataclasses",
        "enum",
        "abc",
        "contextlib",
        "logging",
        "argparse",
        "configparser",
        "subprocess",
        "shutil",
        "tempfile",
        "glob",
        "fnmatch",
        "linecache",
        "pickle",
        "copy",
        "pprint",
        "textwrap",
        "string",
        "io",
        "codecs",
        "locale",
        "calendar",
        "hashlib",
        "hmac",
        "secrets",
        "uuid",
        "urllib",
        "http",
        "email",
        "html",
        "xml",
        "csv",
        "sqlite3",
        "zlib",
        "gzip",
        "bz2",
        "lzma",
        "zipfile",
        "tarfile",
        "threading",
        "multiprocessing",
        "concurrent",
        "queue",
        "socket",
        "ssl",
        "asyncio",
        "unittest",
        "doctest",
        "trace",
        "pdb",
        "profile",
        "warnings",
        "inspect",
        "dis",
        "importlib",
        "pkgutil",
        "platform",
        "ctypes",
        "struct",
        "array",
        "weakref",
        "gc",
        "types",
    }

    return {
        imp
        for imp in imports
        if imp not in stdlib_modules and not imp.startswith("_")
    }


def auto_discover_requirements(
    directory: str = ".",
) -> Tuple[List[Tuple[str, str]], str]:
    """Auto-discover requirements using multiple strategies.

    Tries the following strategies in order:
    1. Look for existing requirements files
    2. Analyze Python files for imports
    3. Return empty if nothing found

    Args:
        directory: Root directory to analyze (default: current directory)

    Returns:
        Tuple of (packages_list, discovery_method) where packages_list contains
        tuples of (package_name, version) for third-party packages
    """
    logger = logging.getLogger("midna")
    logger.info("Starting auto-discovery of requirements...")

    # Strategy 1: Look for existing requirements files
    req_files = find_requirements_files(directory)

    if req_files:
        # Prefer requirements.txt if available
        preferred_file = None
        for file_path in req_files:
            if "requirements.txt" in os.path.basename(file_path):
                preferred_file = file_path
                break

        if not preferred_file:
            preferred_file = req_files[0]

        logger.info(f"Using requirements file: {preferred_file}")

        # Import here to avoid circular imports
        from .parser import read_requirements

        try:
            packages = [(pkg, "") for pkg in read_requirements(preferred_file)]
            return packages, f"requirements file: {preferred_file}"
        except Exception as e:
            logger.warning(f"Failed to read {preferred_file}: {e}")

    # Strategy 2: Analyze Python files for imports
    logger.info("No requirements files found, analyzing Python imports...")
    discovered_imports = analyze_project_imports(directory)

    if discovered_imports:
        # Classify the discovered packages
        stdlib, project, third_party = classify_packages(
            discovered_imports, directory
        )
        logger.info(f"Found {len(stdlib)} stdlib packages")
        logger.info(f"Found {len(project)} project packages")
        logger.info(f"Found {len(third_party)} third-party packages")

        return third_party, "import analysis"

    # Strategy 3: No packages found
    logger.info("No packages discovered")
    return [], "no packages found"


def get_discovery_mode_choice() -> str:
    """Ask user which discovery mode to use.

    Returns:
        User's choice as a string
    """
    print("\nMidna Auto-Discovery Options:")
    print("1. Search for requirements files (requirements.txt, etc.)")
    print("2. Analyze Python files for imported packages")
    print("3. Both (requirements files first, then import analysis)")

    while True:
        try:
            choice = input(
                "\nSelect discovery mode (1-3, default=3): "
            ).strip()
            if choice == "" or choice == "3":
                return "both"
            elif choice == "1":
                return "files"
            elif choice == "2":
                return "imports"
            else:
                print("Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\nOperation cancelled")
            return "cancelled"
