#!/usr/bin/env python3
"""
Comprehensive code formatting fixer for AutoDevCore
Fixes common formatting issues that cause git problems
"""

import os
import re
import sys
from pathlib import Path

class CodeFormatter:
    """Fixes common code formatting issues."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.files_fixed = 0
        self.issues_fixed = 0

    def should_skip_file(self, file_path):
        """Check if file should be skipped."""
        skip_patterns = [
            "gui_env/",
            "__pycache__/",
            ".git/",
            ".pytest_cache/",
            "node_modules/",
            ".venv/",
            "venv/",
            ".bak",
            ".tmp",
        ]

        file_str = str(file_path)
        return any(pattern in file_str for pattern in skip_patterns)

    def fix_trailing_whitespace(self, content):
        """Remove trailing whitespace from lines."""
        lines = content.split("\n")
        fixed_lines = []
        changes = 0

        for line in lines:
            original_line = line
            # Remove trailing whitespace
            line = line.rstrip()
            if line != original_line:
                changes += 1
            fixed_lines.append(line)

        return "\n".join(fixed_lines), changes

    def fix_line_endings(self, content):
        """Ensure consistent line endings."""
        # Convert Windows line endings to Unix
        content = content.replace("\r\n", "\n")
        # Remove any remaining carriage returns
        content = content.replace("\r", "\n")
        return content, 0

    def fix_final_newline(self, content):
        """Ensure file ends with exactly one newline."""
        if not content:
            return content, 0

        # Remove all trailing newlines
        content = content.rstrip("\n")
        # Add exactly one newline
        content += "\n"
        return content, 1

    def fix_multiple_blank_lines(self, content):
        """Fix multiple consecutive blank lines."""
        # Replace 3+ consecutive newlines with 2 newlines
        fixed_content = re.sub(r"\n{3,}", "\n\n", content)
        changes = 1 if fixed_content != content else 0
        return fixed_content, changes

    def fix_indentation_issues(self, content):
        """Fix basic indentation issues."""
        lines = content.split("\n")
        fixed_lines = []
        changes = 0

        for line in lines:
            original_line = line

            # Convert tabs to 4 spaces (Python standard)
            if "\t" in line:
                line = line.replace("\t", "    ")
                changes += 1

            fixed_lines.append(line)

        return "\n".join(fixed_lines), changes

    def fix_import_spacing(self, content):
        """Fix spacing around imports."""
        lines = content.split("\n")
        fixed_lines = []
        changes = 0
        prev_was_import = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Check if this is an import line
            is_import = (
                stripped.startswith("import ")
                or stripped.startswith("from ")
                or stripped.startswith("#")
                and "import" in stripped
            )

            # Add blank line before first import if needed
            if (
                is_import
                and not prev_was_import
                and i > 0
                and lines[i - 1].strip()
                and not lines[i - 1].strip().startswith("#")
            ):
                if fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append("")
                    changes += 1

            fixed_lines.append(line)
            prev_was_import = is_import

        return "\n".join(fixed_lines), changes

    def fix_file(self, file_path):
        """Fix formatting issues in a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            total_changes = 0

            # Apply all fixes
            content, changes = self.fix_line_endings(content)
            total_changes += changes

            content, changes = self.fix_trailing_whitespace(content)
            total_changes += changes

            content, changes = self.fix_indentation_issues(content)
            total_changes += changes

            content, changes = self.fix_multiple_blank_lines(content)
            total_changes += changes

            content, changes = self.fix_import_spacing(content)
            total_changes += changes

            content, changes = self.fix_final_newline(content)
            total_changes += changes

            # Write back if changes were made
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                self.files_fixed += 1
                self.issues_fixed += total_changes
                print(f"✅ Fixed {total_changes} issues in {file_path}")
                return True

            return False

        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            return False

    def fix_all_python_files(self):
        """Fix all Python files in the project."""
        print("🔧 AutoDevCore Code Formatter")
        print("=" * 50)

        python_files = list(self.project_root.rglob("*.py"))
        total_files = 0

        for file_path in python_files:
            if self.should_skip_file(file_path):
                continue

            total_files += 1
            self.fix_file(file_path)

        print("\n" + "=" * 50)
        print("📊 FORMATTING SUMMARY")
        print("=" * 50)
        print(f"📁 Total Python files checked: {total_files}")
        print(f"🔧 Files fixed: {self.files_fixed}")
        print(f"✨ Total issues fixed: {self.issues_fixed}")

        if self.files_fixed > 0:
            print(f"\n✅ Formatting complete! Fixed {self.files_fixed} files.")
        else:
            print(f"\n✅ All files already properly formatted!")

    def fix_markdown_files(self):
        """Fix basic issues in markdown files."""
        print("\n📝 Fixing Markdown files...")

        md_files = list(self.project_root.rglob("*.md"))
        md_fixed = 0

        for file_path in md_files:
            if self.should_skip_file(file_path):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # Fix trailing whitespace
                content, _ = self.fix_trailing_whitespace(content)

                # Fix line endings
                content, _ = self.fix_line_endings(content)

                # Ensure final newline
                content, _ = self.fix_final_newline(content)

                if content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    md_fixed += 1
                    print(f"✅ Fixed {file_path}")

            except Exception as e:
                print(f"❌ Error fixing {file_path}: {e}")

        print(f"📝 Fixed {md_fixed} Markdown files")

def main():
    """Main function."""
    formatter = CodeFormatter()

    # Fix Python files
    formatter.fix_all_python_files()

    # Fix Markdown files
    formatter.fix_markdown_files()

    print("\n🎯 Formatting complete! Ready for git commit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
