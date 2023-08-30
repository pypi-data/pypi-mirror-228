from __future__ import annotations

import os.path

import attrs


@attrs.frozen
class FileSystem:
    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def read_content(self, path: str) -> str:
        try:
            with open(path) as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def read_lines(self, path: str) -> list[str]:
        return self.read_content(path).splitlines(keepends=True)

    def write_file(
            self,
            path: str, content: str,
            is_executable: bool,
    ) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

        if is_executable:
            os.chmod(path, 0o744)


class DryRunFileWriter(FileSystem):
    def write_file(self, path: str, content: str, is_executable: bool) -> None:
        pass
