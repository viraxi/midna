"""Main CLI interface for Midna"""

import importlib.metadata
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .checker import check_installed_packages
from .discovery import auto_discover_requirements
from .installer import install_packages
from .logger import setup_logging
from .parser import read_requirements
from .uninstaller import check_packages_to_uninstall, uninstall_packages


def create_parser() -> ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        ArgumentParser: Configured argument parser with all CLI options
    """
    parser = ArgumentParser(
        description=(
            "Midna - Smart pip requirements installer and package manager.\n"
            "Automatically discovers, manages, and extracts Python package "
            "requirements."
        ),
        epilog=(
            "Examples:\n"
            "Basic usage:\n"
            "  midna                  # Auto-discover and install\n"
            "  midna file.txt         # Use specific requirements file\n"
            "  midna --dry-run        # Preview without installing\n"
            "\nPackage extraction:\n"
            "  midna -o reqs.txt          # Extract auto-discovered packages\n"
            "  midna file.txt -o deps.txt # Extract from specific file\n"
            "\nLogging and verbosity:\n"
            "  midna --log                # Enable logging to file\n"
            "  midna -v                   # Show verbose output\n"
            "  midna -v --log -o reqs.txt # Full output with logs\n"
            "\nOther operations:\n"
            "  midna -u                   # Uninstall mode\n"
            "  midna --version            # Show version"
        ),
        formatter_class=RawDescriptionHelpFormatter,
    )
    # Version
    parser.add_argument(
        "--version", action="store_true", help="Show version and exit"
    )

    # Input options
    parser.add_argument(
        "requirements_file",
        nargs="?",
        help=(
            "Path to requirements.txt or pyproject.toml file "
            "(if not provided, will auto-discover)"
        ),
        metavar="FILE",
    )

    # Output options
    parser.add_argument(
        "--output",
        "-o",
        help=(
            "Extract discovered packages to a requirements file "
            "(no files created unless specified)"
        ),
        metavar="FILE",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Enable logging to ~/.midna/logs/midna.log",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed progress information",
    )

    # Operation modes
    parser.add_argument(
        "--uninstall",
        "-u",
        action="store_true",
        help="Uninstall packages instead of installing them",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Preview actions without making any changes",
    )

    return parser


def main() -> int:
    """Main entry point for Midna CLI.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        try:
            version = importlib.metadata.version("midna")
            print(f"Midna version {version}")
            return 0
        except importlib.metadata.PackageNotFoundError:
            print("Midna version unknown (package not installed)")
            return 1

    logger = setup_logging(args.verbose, args.log)
    if args.log:
        logger.info("Midna started")

    try:
        # Determine how to get packages
        if args.requirements_file:
            # Traditional mode: use specified file
            packages = read_requirements(args.requirements_file)
            source_info = f"file: {args.requirements_file}"
            logger.info(f"Using specified file: {args.requirements_file}")
        else:
            # Auto-discovery mode
            print("Auto-discovering requirements...")
            discovered_items = auto_discover_requirements(".")

            # Convert list of tuples to list of package names
            packages_info, discovery_method = discovered_items
            packages = [pkg[0] for pkg in packages_info]
            source_info = discovery_method

            logger.info(f"Auto-discovery used: {source_info}")

        if not packages:
            if args.requirements_file:
                print("No packages found in requirements file.")
            else:
                print("No packages discovered in current directory.")
                print("Tip: You can:")
                print("  - Create a requirements.txt file")
                print("  - Run 'midna <filename>' to specify a file")
                print("  - Add import statements to your Python files")
            return 0

        print(f"\nFound {len(packages)} packages ({source_info})")

        # Save packages to output file if requested
        if args.output:
            try:
                with open(args.output, "w") as f:
                    for package in packages:
                        f.write(f"{package}\n")
                print(f"\nSaved discovered packages to: {args.output}")
                logger.info(f"Saved packages to: {args.output}")
            except Exception as e:
                print(f"ERROR: Failed to save packages: {e}")
                logger.error(f"Failed to save packages: {e}")
                return 1

        # Show packages that were found
        if args.verbose or not args.requirements_file:
            print("\nDiscovered packages:")
            for package in packages:
                print(f"  + {package}")

        if args.uninstall:
            # Handle uninstall mode
            if args.requirements_file:
                found_packages, not_found_packages = (
                    check_packages_to_uninstall(args.requirements_file)
                )
            else:
                # For auto-discovered packages, create temp file
                import tempfile

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False
                ) as temp_file:
                    temp_file.write("\n".join(packages))
                    temp_path = temp_file.name

                try:
                    found_packages, not_found_packages = (
                        check_packages_to_uninstall(temp_path)
                    )
                finally:
                    import os

                    os.unlink(temp_path)

            if not_found_packages:
                print(f"\nNot installed ({len(not_found_packages)} packages):")
                for package in not_found_packages:
                    print(f"  - {package}")
            if not found_packages:
                print("\nNo packages to uninstall (none are installed)!")
                return 0
            print(f"\nWill uninstall ({len(found_packages)} packages):")
            for package in found_packages:
                print(f"  - {package}")

            # Create temp file for uninstaller
            import tempfile

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as temp_file:
                temp_file.write("\n".join(found_packages))
                temp_path = temp_file.name

            try:
                exit_code = uninstall_packages(temp_path, args.dry_run)
            finally:
                import os

                os.unlink(temp_path)

            return exit_code
        else:
            # Handle install mode
            missing_packages, already_installed = check_installed_packages(
                packages
            )
            if already_installed:
                print(
                    f"\nAlready installed ({len(already_installed)} "
                    f"packages):"
                )
                for package in already_installed:
                    print(f"  + {package}")
            if not missing_packages:
                print("\nAll packages are already installed!")
                return 0
            print(f"\nWill install ({len(missing_packages)} packages):")
            for package in missing_packages:
                print(f"  - {package}")
            exit_code = install_packages(missing_packages, args.dry_run)
            return exit_code

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1
    except KeyboardInterrupt:
        operation = "Uninstallation" if args.uninstall else "Installation"
        print(f"\nWARNING: {operation} interrupted by user")
        return 130
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
