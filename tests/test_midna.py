import importlib.metadata
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from unittest.mock import Mock

from midna import checker, installer, parser, uninstaller


class TestMidnaFunctionality(unittest.TestCase):

    def test_read_requirements_valid_file(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            temp_path = f.name
            content = (
                "requests>=2.25.0\nnumpy>=1.20.0\n"
                "# This is a comment\n\npandas>=1.3.0"
            )
            f.write(content)

        try:
            packages = parser.read_requirements(temp_path)
            self.assertEqual(len(packages), 3)
            self.assertIn("requests>=2.25.0", packages)
            self.assertIn("numpy>=1.20.0", packages)
            self.assertIn("pandas>=1.3.0", packages)
        finally:
            try:
                os.unlink(temp_path)
            except (OSError, PermissionError):
                pass

    def test_read_requirements_nonexistent_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            parser.read_requirements("nonexistent_file.txt")

    def test_parse_package_name(self) -> None:
        self.assertEqual(
            parser.parse_package_name("requests>=2.25.0"), "requests"
        )
        self.assertEqual(parser.parse_package_name("numpy==1.20.0"), "numpy")
        self.assertEqual(parser.parse_package_name("pandas"), "pandas")
        self.assertEqual(parser.parse_package_name("scipy<=1.5.0"), "scipy")

    def test_check_installed_packages(self) -> None:
        # Test with an empty list
        missing, installed = checker.check_installed_packages([])
        self.assertIsInstance(missing, list)
        self.assertIsInstance(installed, list)


class TestMidnaCLI(unittest.TestCase):

    def test_midna_version_command(self) -> None:
        # Get the actual version from package metadata
        version = importlib.metadata.version("midna")
        result = subprocess.run(
            [sys.executable, "-m", "midna", "--version"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn(version, result.stdout)

    def test_midna_help_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "midna", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())

    def test_midna_dry_run_with_sample_file(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            temp_path = f.name
            f.write(
                "fake-package-that-doesnt-exist>=1.0.0\n"
                "another-fake-package>=2.0.0\n"
            )

        try:
            result = subprocess.run(
                [sys.executable, "-m", "midna", "--dry-run", temp_path],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("DRY RUN", result.stdout.upper())
            self.assertIn("Would install", result.stdout)

        finally:
            try:
                os.unlink(temp_path)
            except (OSError, PermissionError):
                pass

    def test_midna_nonexistent_file(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "midna", "nonexistent.txt"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


class TestMidnaInstaller(unittest.TestCase):

    @unittest.mock.patch("subprocess.run")
    def test_install_packages_success(self, mock_run: Mock) -> None:
        """Test successful package installation."""
        mock_run.return_value = unittest.mock.MagicMock(returncode=0)
        result = installer.install_packages(["requests", "numpy"])
        self.assertEqual(result, 0)
        mock_run.assert_called_once_with(
            ["pip", "install", "requests", "numpy"],
            check=True,
            capture_output=True,
            shell=False,
        )

    @unittest.mock.patch("subprocess.run")
    def test_install_packages_failure(self, mock_run: Mock) -> None:
        """Test failed package installation."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "pip")
        result = installer.install_packages(["fake-package"])
        self.assertEqual(result, 1)
        mock_run.assert_called_once_with(
            ["pip", "install", "fake-package"],
            check=True,
            capture_output=True,
            shell=False,
        )

    def test_install_packages_empty_list(self) -> None:
        """Test installing empty package list."""
        result = installer.install_packages([])
        self.assertEqual(result, 0)

    def test_install_packages_dry_run(self) -> None:
        """Test dry run installation."""
        result = installer.install_packages(["requests"], dry_run=True)
        self.assertEqual(result, 0)


class TestMidnaUninstaller(unittest.TestCase):

    def test_check_packages_to_uninstall_with_valid_file(self) -> None:
        """Test checking packages to uninstall with valid file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            temp_path = f.name
            f.write("setuptools>=40.0.0\npip>=20.0.0\n# Comment\n")

        try:
            to_uninstall, not_installed = (
                uninstaller.check_packages_to_uninstall(temp_path)
            )
            self.assertIsInstance(to_uninstall, list)
            self.assertIsInstance(not_installed, list)
            # At least one of setuptools or pip should be found
            package_names = [
                pkg.split(">=")[0].lower() for pkg in to_uninstall
            ]
            self.assertTrue(
                any(name in ["setuptools", "pip"] for name in package_names)
            )
        finally:
            try:
                os.unlink(temp_path)
            except (OSError, PermissionError):
                pass

    def test_check_packages_to_uninstall_nonexistent_file(self) -> None:
        """Test checking packages to uninstall with nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            uninstaller.check_packages_to_uninstall("nonexistent_file.txt")

    def test_uninstall_packages_dry_run(self) -> None:
        """Test uninstall packages in dry run mode."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            temp_path = f.name
            f.write("fake-package-that-doesnt-exist>=1.0.0\n")

        try:
            # This should not raise an exception and should handle dry run
            result = uninstaller.uninstall_packages(temp_path, dry_run=True)
            # Should return 0 for successful dry run
            self.assertEqual(result, 0)
        finally:
            try:
                os.unlink(temp_path)
            except (OSError, PermissionError):
                pass

    @unittest.mock.patch("subprocess.run")
    def test_uninstall_package_list_success(self, mock_run: Mock) -> None:
        """Test successful package uninstallation."""
        mock_run.return_value = unittest.mock.MagicMock(returncode=0)
        result = uninstaller._uninstall_package_list(["requests", "numpy"])
        self.assertEqual(result, 0)
        mock_run.assert_called_once_with(
            ["pip", "uninstall", "-y", "requests", "numpy"],
            check=True,
            capture_output=True,
            shell=False,
        )

    @unittest.mock.patch("subprocess.run")
    def test_uninstall_package_list_failure(self, mock_run: Mock) -> None:
        """Test failed package uninstallation."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "pip")
        result = uninstaller._uninstall_package_list(["fake-package"])
        self.assertEqual(result, 1)
        mock_run.assert_called_once_with(
            ["pip", "uninstall", "-y", "fake-package"],
            check=True,
            capture_output=True,
            shell=False,
        )


class TestMidnaUninstallCLI(unittest.TestCase):

    def test_midna_uninstall_help(self) -> None:
        """Test that uninstall option appears in help."""
        result = subprocess.run(
            [sys.executable, "-m", "midna", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--uninstall", result.stdout)
        self.assertIn("-u", result.stdout)

    def test_midna_uninstall_dry_run_with_sample_file(self) -> None:
        """Test uninstall command with dry run flag."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            temp_path = f.name
            f.write(
                "fake-package-that-doesnt-exist>=1.0.0\n"
                "another-fake-package>=2.0.0\n"
            )

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "midna",
                    "--uninstall",
                    "--dry-run",
                    temp_path,
                ],
                capture_output=True,
                text=True,
            )

            # Should succeed even if no packages to uninstall
            self.assertEqual(result.returncode, 0)
            self.assertIn("No packages to uninstall", result.stdout)

        finally:
            try:
                os.unlink(temp_path)
            except (OSError, PermissionError):
                pass

    def test_midna_uninstall_nonexistent_file(self) -> None:
        """Test uninstall command with nonexistent file."""
        result = subprocess.run(
            [sys.executable, "-m", "piko", "--uninstall", "nonexistent.txt"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
