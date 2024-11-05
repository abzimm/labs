from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Set
import os
import sys

@dataclass
class CodeFile:
    filepath: str
    lines: List[str] = None

    def read_file(self) -> None:
        with open(self.filepath, 'r') as file:
            self.lines = file.readlines()

class Analyzer(ABC):
    @abstractmethod
    def analyze(self, code_file: CodeFile) -> str:
        pass

class FileStructure(Analyzer):
    def __init__(self):
        self._imports: Set[str] = set()
        self._classes: Set[str] = set()
        self._functions: Set[str] = set()

    def analyze(self, code_file: CodeFile) -> str:
        self._find_elements(code_file.lines)
        return self._generate_report()

    def _find_elements(self, lines: List[str]) -> None:
        indent_level = 0
        in_class = False
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level:
                in_class = False

            if stripped.startswith('import ') or stripped.startswith('from '):
                self._imports.add(stripped.split()[1])
            elif stripped.startswith('class '):
                class_name = stripped.split('class ')[1].split('(')[0].strip(':')
                self._classes.add(class_name)
                in_class = True
                indent_level = current_indent
            elif stripped.startswith('def ') and not in_class:
                func_name = stripped.split('def ')[1].split('(')[0]
                self._functions.add(func_name)

    def _generate_report(self) -> str:
        report = ["FILE STRUCTURE", "-" * 50]
        
        if self._imports:
            report.extend(["\nImported packages:"] + 
                        [f"- {imp}" for imp in sorted(self._imports)])
        
        if self._classes:
            report.extend(["\nClasses defined:"] + 
                        [f"- {cls}" for cls in sorted(self._classes)])
        
        if self._functions:
            report.extend(["\nStandalone functions:"] + 
                        [f"- {func}" for func in sorted(self._functions)])
            
        return '\n'.join(report)

class DocStringAnalyzer(Analyzer):
    def analyze(self, code_file: CodeFile) -> str:
        report = ["\nDOCSTRING ANALYSIS", "-" * 50]
        indent_level = 0
        in_class = False
        current_class = ""

        for i, line in enumerate(code_file.lines):
            stripped = line.strip()
            if not stripped:
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level:
                in_class = False

            if stripped.startswith('class '):
                current_class = stripped.split('class ')[1].split('(')[0].strip(':')
                in_class = True
                indent_level = current_indent
                doc = self._get_docstring(code_file.lines, i + 1)
                report.append(f"\nClass {current_class} docstring:" if doc 
                            else f"\n{current_class}: DocString not found.")
                if doc:
                    report.append(doc)
            
            elif stripped.startswith('def '):
                func_name = stripped.split('def ')[1].split('(')[0]
                full_name = f"{current_class}.{func_name}" if in_class else func_name
                doc = self._get_docstring(code_file.lines, i + 1)
                report.append(f"\n{'Method' if in_class else 'Function'} {full_name} docstring:" 
                            if doc else f"\n{full_name}: DocString not found.")
                if doc:
                    report.append(doc)

        return '\n'.join(report)

    def _get_docstring(self, lines: List[str], start: int) -> str:
        i = start
        while i < len(lines):
            line = lines[i].strip()
            if '"""' in line:
                if line.count('"""') == 2:
                    return line.split('"""')[1].strip()
                else:
                    docstring = []
                    i += 1
                    while i < len(lines) and '"""' not in lines[i]:
                        docstring.append(lines[i].strip())
                        i += 1
                    return ' '.join(docstring)
            elif not line or line.startswith('def ') or line.startswith('class '):
                break
            i += 1
        return ""

class TypeChecker(Analyzer):
    def analyze(self, code_file: CodeFile) -> str:
        report = ["\nTYPE ANNOTATION CHECK", "-" * 50]
        missing = []
        indent_level = 0
        in_class = False
        current_class = ""

        for line in code_file.lines:
            stripped = line.strip()
            if not stripped:
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level:
                in_class = False

            if stripped.startswith('class '):
                current_class = stripped.split('class ')[1].split('(')[0].strip(':')
                in_class = True
                indent_level = current_indent

            elif stripped.startswith('def '):
                func_name = stripped.split('def ')[1].split('(')[0]
                if not self._has_type_annotations(stripped):
                    name = f"{current_class}.{func_name}" if in_class else func_name
                    missing.append(name)

        if missing:
            report.extend(["\nFunctions/methods missing type annotations:"] +
                        [f"- {name}" for name in sorted(missing)])
        else:
            report.append("\nAll functions and methods have type annotations.")

        return '\n'.join(report)

    def _has_type_annotations(self, func_def: str) -> bool:
        params = func_def.split('(')[1].split(')')[0]
        has_params = all(':' in p for p in params.split(',') if p.strip() and 'self' not in p)
        return '->' in func_def and has_params

class NamingChecker(Analyzer):
    def analyze(self, code_file: CodeFile) -> str:
        report = ["\nNAMING CONVENTION CHECK", "-" * 50]
        bad_classes = []
        bad_functions = []

        for line in code_file.lines:
            stripped = line.strip()
            if stripped.startswith('class '):
                name = stripped.split('class ')[1].split('(')[0].strip(':')
                if not self._is_camel_case(name):
                    bad_classes.append(name)
            elif stripped.startswith('def '):
                name = stripped.split('def ')[1].split('(')[0]
                if not self._is_snake_case(name):
                    bad_functions.append(name)

        if bad_classes:
            report.extend(["\nClasses not following CamelCase convention:"] +
                        [f"- {name}" for name in sorted(bad_classes)])

        if bad_functions:
            report.extend(["\nFunctions/methods not following snake_case convention:"] +
                        [f"- {name}" for name in sorted(bad_functions)])

        if not bad_classes and not bad_functions:
            report.append("\nAll names adhere to the specified naming conventions.")

        return '\n'.join(report)

    def _is_camel_case(self, name: str) -> bool:
        return name[0].isupper() and '_' not in name

    def _is_snake_case(self, name: str) -> bool:
        return name.islower() and all(c.islower() or c.isdigit() or c == '_' for c in name)

class StyleAnalyzer:
    def __init__(self, filepath: str):
        self.code_file = CodeFile(filepath)
        self.code_file.read_file()
        self._analyzers: List[Analyzer] = [
            FileStructure(),
            DocStringAnalyzer(),
            TypeChecker(),
            NamingChecker()
        ]

    def analyze(self) -> None:
        reports = [analyzer.analyze(self.code_file) for analyzer in self._analyzers]
        base_name = os.path.splitext(os.path.basename(self.code_file.filepath))[0]
        report_path = os.path.join(os.path.dirname(self.code_file.filepath), f"style_report_{base_name}.txt")
        with open(report_path, 'w') as file:
            file.write('\n'.join(reports))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python style_checker.py <python_file>")
        sys.exit(1)
        
    analyzer = StyleAnalyzer(sys.argv[1])
    analyzer.analyze()
    print("Style report generated")