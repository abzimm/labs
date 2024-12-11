from typing import List, Set, Tuple, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
import sys

@dataclass(frozen=True)
class CodeAnalysis:
    total_lines: int
    imports: frozenset[str]
    classes: frozenset[str]
    functions: frozenset[str]
    docstrings: Dict[str, Optional[str]]
    missing_types: frozenset[str]
    bad_camelcase: frozenset[str]
    bad_snakecase: frozenset[str]

def read_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        return f.readlines()

def analyze_imports(lines: List[str]) -> frozenset[str]:
    return frozenset(
        line.split()[1] for line in lines 
        if line.strip().startswith(('import ', 'from '))
    )

def find_definitions(lines: List[str]) -> Tuple[frozenset[str], frozenset[str]]:
    classes: Set[str] = set()
    functions: Set[str] = set()
    
    indent_stack = [0]
    in_class = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        indent = len(line) - len(line.lstrip())
        
        while indent < indent_stack[-1]:
            indent_stack.pop()
            if len(indent_stack) == 1:
                in_class = False
                
        if stripped.startswith('class '):
            class_name = stripped.split('class ')[1].split('(')[0].strip(':')
            classes.add(class_name)
            in_class = True
            indent_stack.append(indent)
            
        elif stripped.startswith('def ') and not in_class:
            func_name = stripped.split('def ')[1].split('(')[0]
            functions.add(func_name)
            
    return frozenset(classes), frozenset(functions)

def extract_docstrings(lines: List[str]) -> Dict[str, Optional[str]]:
    docstrings: Dict[str, Optional[str]] = {}
    indent_stack = [0]
    current_class = ""
    
    def get_docstring(start_idx: int) -> Optional[str]:
        for i in range(start_idx, len(lines)):
            line = lines[i].strip()
            if '"""' in line:
                if line.count('"""') == 2:
                    return line.split('"""')[1].strip()
                else:
                    doc_lines = []
                    i += 1
                    while i < len(lines) and '"""' not in lines[i]:
                        doc_lines.append(lines[i].strip())
                        i += 1
                    return ' '.join(doc_lines)
            elif not line or line.startswith(('def', 'class')):
                return None
        return None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
            
        indent = len(line) - len(line.lstrip())
        
        while indent < indent_stack[-1]:
            indent_stack.pop()
            if len(indent_stack) == 1:
                current_class = ""
                
        if stripped.startswith('class '):
            name = stripped.split('class ')[1].split('(')[0].strip(':')
            current_class = name
            indent_stack.append(indent)
            docstrings[name] = get_docstring(i + 1)
            
        elif stripped.startswith('def '):
            name = stripped.split('def ')[1].split('(')[0]
            full_name = f"{current_class}.{name}" if current_class else name
            docstrings[full_name] = get_docstring(i + 1)
            
    return docstrings

def check_type_annotations(lines: List[str]) -> frozenset[str]:
    missing: Set[str] = set()
    indent_stack = [0]
    current_class = ""
    
    def lacks_annotations(func_def: str) -> bool:
        params = func_def.split('(')[1].split(')')[0]
        has_params = all(':' in p for p in params.split(',') 
                        if p.strip() and 'self' not in p)
        return '->' not in func_def or not has_params
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        indent = len(line) - len(line.lstrip())
        
        while indent < indent_stack[-1]:
            indent_stack.pop()
            if len(indent_stack) == 1:
                current_class = ""
                
        if stripped.startswith('class '):
            current_class = stripped.split('class ')[1].split('(')[0].strip(':')
            indent_stack.append(indent)
            
        elif stripped.startswith('def '):
            name = stripped.split('def ')[1].split('(')[0]
            full_name = f"{current_class}.{name}" if current_class else name
            if lacks_annotations(stripped):
                missing.add(full_name)
                
    return frozenset(missing)

def check_naming_conventions(lines: List[str]) -> Tuple[frozenset[str], frozenset[str]]:
    bad_camel: Set[str] = set()
    bad_snake: Set[str] = set()
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('class '):
            name = stripped.split('class ')[1].split('(')[0].strip(':')
            if not (name[0].isupper() and '_' not in name):
                bad_camel.add(name)
                
        elif stripped.startswith('def '):
            name = stripped.split('def ')[1].split('(')[0]
            if not (name.islower() and 
                   all(c.islower() or c.isdigit() or c == '_' for c in name)):
                bad_snake.add(name)
                
    return frozenset(bad_camel), frozenset(bad_snake)

def generate_report(analysis: CodeAnalysis) -> str:
    sections = []
    
    sections.extend([
        "FILE STRUCTURE",
        "-" * 50,
        f"\nTotal lines of code: {analysis.total_lines}"
    ])
    
    if analysis.imports:
        sections.extend([
            "\nImported packages:",
            *[f"- {imp}" for imp in sorted(analysis.imports)]
        ])
        
    if analysis.classes:
        sections.extend([
            "\nClasses defined:",
            *[f"- {cls}" for cls in sorted(analysis.classes)]
        ])
        
    if analysis.functions:
        sections.extend([
            "\nStandalone functions:",
            *[f"- {func}" for func in sorted(analysis.functions)]
        ])
    
    sections.extend([
        "\nDOCSTRING ANALYSIS",
        "-" * 50
    ])
    
    for name, docstring in sorted(analysis.docstrings.items()):
        kind = "Class" if '.' not in name else "Method"
        if '.' not in name and not any(c in name for c in analysis.classes):
            kind = "Function"
            
        if docstring:
            sections.extend([
                f"\n{kind} {name} docstring:",
                docstring
            ])
        else:
            sections.append(f"\n{name}: DocString not found.")
    
    sections.extend([
        "\nTYPE ANNOTATION CHECK",
        "-" * 50
    ])
    
    if analysis.missing_types:
        sections.extend([
            "\nFunctions/methods missing type annotations:",
            *[f"- {name}" for name in sorted(analysis.missing_types)]
        ])
    else:
        sections.append("\nAll functions and methods have type annotations.")
    
    sections.extend([
        "\nNAMING CONVENTION CHECK",
        "-" * 50
    ])
    
    if analysis.bad_camelcase:
        sections.extend([
            "\nClasses not following CamelCase convention:",
            *[f"- {name}" for name in sorted(analysis.bad_camelcase)]
        ])
        
    if analysis.bad_snakecase:
        sections.extend([
            "\nFunctions/methods not following snake_case convention:",
            *[f"- {name}" for name in sorted(analysis.bad_snakecase)]
        ])
        
    if not (analysis.bad_camelcase or analysis.bad_snakecase):
        sections.append("\nAll names adhere to the specified naming conventions.")
    
    return '\n'.join(sections)

def analyze_code(filepath: str) -> CodeAnalysis:
    lines = read_file(filepath)
    classes, functions = find_definitions(lines)
    bad_camel, bad_snake = check_naming_conventions(lines)
    
    return CodeAnalysis(
        total_lines=len(lines),
        imports=analyze_imports(lines),
        classes=classes,
        functions=functions,
        docstrings=extract_docstrings(lines),
        missing_types=check_type_annotations(lines),
        bad_camelcase=bad_camel,
        bad_snakecase=bad_snake
    )

def main() -> None:
    if len(sys.argv) != 2:
        filepath = input("Enter the path to the Python file to analyze: ").strip()
    else:
        filepath = sys.argv[1]
        
    try:
        analysis = analyze_code(filepath)
        report = generate_report(analysis)
        
        output_path = Path(filepath).parent / f"style_report_{Path(filepath).stem}.txt"
        with open(output_path, 'w') as f:
            f.write(report)
            
        print("Style report generated successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()