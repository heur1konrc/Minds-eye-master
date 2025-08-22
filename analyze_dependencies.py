#!/usr/bin/env python3
"""
Dependency Analysis Script for Mind's Eye Photography
Maps all imports, exports, and dependencies to plan safe SQL conversion
"""

import os
import re
import ast
from collections import defaultdict

def analyze_file(filepath):
    """Analyze a Python file for imports and function definitions"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        tree = ast.parse(content)
        
        imports = []
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append({
                        'type': 'from_import',
                        'module': module,
                        'name': alias.name,
                        'alias': alias.asname
                    })
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return {
            'imports': imports,
            'functions': functions,
            'classes': classes,
            'content': content
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    project_root = './src'
    files_analysis = {}
    
    print("🔍 DEPENDENCY ANALYSIS - Mind's Eye Photography")
    print("=" * 60)
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"📁 Found {len(python_files)} Python files:")
    for f in python_files:
        print(f"   • {f}")
    print()
    
    # Analyze each file
    for filepath in python_files:
        rel_path = os.path.relpath(filepath)
        print(f"🔍 Analyzing: {rel_path}")
        analysis = analyze_file(filepath)
        files_analysis[rel_path] = analysis
        
        if 'error' in analysis:
            print(f"   ❌ Error: {analysis['error']}")
            continue
            
        print(f"   📥 Imports: {len(analysis['imports'])}")
        print(f"   🔧 Functions: {len(analysis['functions'])}")
        print(f"   📦 Classes: {len(analysis['classes'])}")
        print()
    
    # Build dependency map
    print("🗺️  DEPENDENCY MAP")
    print("=" * 60)
    
    # Group by what imports what
    import_map = defaultdict(list)
    model_dependencies = []
    
    for filepath, analysis in files_analysis.items():
        if 'error' in analysis:
            continue
            
        print(f"\n📄 {filepath}:")
        
        for imp in analysis['imports']:
            if imp['type'] == 'from_import':
                import_source = f"{imp['module']}.{imp['name']}"
                import_map[import_source].append(filepath)
                
                # Check for model dependencies
                if 'models' in imp['module']:
                    model_dependencies.append({
                        'file': filepath,
                        'imports': f"{imp['module']}.{imp['name']}"
                    })
                    print(f"   🔗 MODEL DEPENDENCY: {imp['module']}.{imp['name']}")
                else:
                    print(f"   📥 {imp['module']}.{imp['name']}")
            else:
                print(f"   📦 {imp['module']}")
    
    # Critical dependencies analysis
    print(f"\n🚨 CRITICAL MODEL DEPENDENCIES ({len(model_dependencies)}):")
    print("=" * 60)
    
    for dep in model_dependencies:
        print(f"   • {dep['file']} imports {dep['imports']}")
    
    # Conversion plan
    print(f"\n📋 SQL CONVERSION PLAN:")
    print("=" * 60)
    print("1. ✅ Create new SQL models (src/models.py)")
    print("2. 🔧 Update model dependencies:")
    
    for dep in model_dependencies:
        print(f"   • Fix {dep['file']}")
    
    print("3. 🧪 Test all imports locally")
    print("4. 🚀 Deploy in stages")
    
    # Files that need updating
    files_to_update = set(dep['file'] for dep in model_dependencies)
    print(f"\n📝 FILES REQUIRING UPDATES ({len(files_to_update)}):")
    for f in sorted(files_to_update):
        print(f"   • {f}")

if __name__ == "__main__":
    main()
