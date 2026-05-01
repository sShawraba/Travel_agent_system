#!/usr/bin/env python3
"""
Smart Travel Planner - Project Statistics & Summary
Run this to see complete project stats
"""

import os
import json
from pathlib import Path
from collections import defaultdict

def count_lines(filepath):
    """Count lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def analyze_project(root_path):
    """Analyze the project structure."""
    
    stats = {
        'total_files': 0,
        'total_lines': 0,
        'by_type': defaultdict(lambda: {'count': 0, 'lines': 0}),
        'by_directory': defaultdict(lambda: {'count': 0, 'lines': 0}),
        'files_list': []
    }
    
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build', '.egg-info'}
    ignore_patterns = {'.pyc', '.pyo', '.egg', '.DS_Store', 'Thumbs.db'}
    
    for root, dirs, files in os.walk(root_path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        for file in files:
            # Skip ignored patterns
            if any(file.endswith(pattern) for pattern in ignore_patterns):
                continue
            if file.startswith('.'):
                continue
            
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_path)
            
            # Get file extension
            if '.' in file:
                ext = file.split('.')[-1]
            else:
                ext = 'no_extension'
            
            # Count lines
            lines = count_lines(filepath)
            
            # Get directory
            directory = os.path.dirname(rel_path).split('/')[0] if '/' in rel_path else 'root'
            
            # Update stats
            stats['total_files'] += 1
            stats['total_lines'] += lines
            stats['by_type'][ext]['count'] += 1
            stats['by_type'][ext]['lines'] += lines
            stats['by_directory'][directory]['count'] += 1
            stats['by_directory'][directory]['lines'] += lines
            
            stats['files_list'].append({
                'path': rel_path,
                'type': ext,
                'lines': lines
            })
    
    return stats

def print_report(stats):
    """Print a formatted report."""
    print("\n" + "="*70)
    print("🎉 SMART TRAVEL PLANNER - PROJECT STATISTICS")
    print("="*70)
    
    print(f"\n📊 OVERALL STATISTICS")
    print(f"   Total Files: {stats['total_files']}")
    print(f"   Total Lines of Code: {stats['total_lines']:,}")
    print(f"   Average Lines per File: {stats['total_lines'] // max(stats['total_files'], 1)}")
    
    print(f"\n📁 BY FILE TYPE")
    print(f"   {'Type':<15} {'Files':<10} {'Lines':<10}")
    print(f"   {'-'*35}")
    for ext in sorted(stats['by_type'].keys()):
        info = stats['by_type'][ext]
        print(f"   {ext:<15} {info['count']:<10} {info['lines']:<10}")
    
    print(f"\n📂 BY DIRECTORY")
    print(f"   {'Directory':<20} {'Files':<10} {'Lines':<10}")
    print(f"   {'-'*40}")
    for dir_name in sorted(stats['by_directory'].keys()):
        info = stats['by_directory'][dir_name]
        print(f"   {dir_name:<20} {info['count']:<10} {info['lines']:<10}")
    
    print(f"\n📄 KEY FILES")
    key_files = [
        'backend/app/main.py',
        'backend/app/services/agent_service.py',
        'backend/app/services/llm_service.py',
        'frontend/src/App.jsx',
        'docker-compose.yml'
    ]
    for key_file in key_files:
        for f in stats['files_list']:
            if f['path'] == key_file:
                print(f"   {f['path']:<40} {f['lines']:<5} lines")
                break
    
    print(f"\n✅ COMPLETE DELIVERABLE")
    print(f"   ✓ Backend: FastAPI + LangGraph")
    print(f"   ✓ Frontend: React + Vite")
    print(f"   ✓ Infrastructure: Docker + docker-compose")
    print(f"   ✓ Documentation: 10 comprehensive guides")
    print(f"   ✓ Testing: Backend tests + validation scripts")
    print(f"   ✓ Type Safety: Pydantic throughout")
    print(f"   ✓ Error Handling: Graceful degradation")
    print(f"   ✓ Observability: LangSmith tracing")
    
    print(f"\n🚀 READY TO RUN")
    print(f"   1. Set API keys in backend/.env")
    print(f"   2. Run: docker-compose up --build")
    print(f"   3. Visit: http://localhost:3000")
    
    print(f"\n📚 DOCUMENTATION")
    docs = [
        ('QUICKSTART.md', 'Get running in 5 minutes'),
        ('README.md', 'Project overview'),
        ('SETUP.md', 'Detailed setup guide'),
        ('API_REFERENCE.md', 'API endpoint documentation'),
        ('AGENT_FLOW.md', 'How the agent works'),
        ('ARCHITECTURE.md', 'System design'),
        ('PROJECT_SUMMARY.md', 'Code organization'),
        ('TESTING_GUIDE.md', 'Testing procedures'),
        ('DEPLOYMENT_CHECKLIST.md', 'Production readiness'),
        ('FILE_INVENTORY.md', 'Complete file list'),
    ]
    for doc, desc in docs:
        print(f"   • {doc:<30} - {desc}")
    
    print(f"\n🔑 REQUIRED KEYS")
    print(f"   • GOOGLE_API_KEY (from makersuite.google.com)")
    print(f"   • LANGCHAIN_API_KEY (from smith.langchain.com)")
    
    print(f"\n" + "="*70)
    print("✨ Happy Traveling! ✈️")
    print("="*70 + "\n")

def main():
    """Main function."""
    root = Path(__file__).parent
    stats = analyze_project(root)
    print_report(stats)

if __name__ == '__main__':
    main()
