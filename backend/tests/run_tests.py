#!/usr/bin/env python3
"""
Comprehensive test runner with formatted output for Character Chatbot API tests
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print test suite header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}  Character Chatbot API - Test Suite{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    print(f"Started at: {Colors.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'─'*70}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'─'*70}{Colors.ENDC}")

def run_tests(test_file=None, verbose=False, markers=None):
    """Run pytest with formatted output"""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-v" if verbose else "-q",
        "--tb=short",
        "--color=yes"
    ]
    
    if markers:
        cmd += ["-m", markers]
    
    if test_file:
        cmd.append(str(test_file))
    else:
        # Run all tests in tests directory
        cmd.append(str(Path(__file__).parent))
    
    print(f"\n{Colors.YELLOW}Running: {' '.join(cmd)}{Colors.ENDC}\n")
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def print_footer(success):
    """Print test suite footer"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    
    if success:
        print(f"{Colors.GREEN}{Colors.BOLD}  ✓ ALL TESTS PASSED{Colors.ENDC}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}  ✗ SOME TESTS FAILED{Colors.ENDC}")
    
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"Finished at: {Colors.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

def print_test_categories():
    """Print available test categories"""
    print(f"\n{Colors.YELLOW}Available test categories:{Colors.ENDC}")
    print(f"  {Colors.CYAN}1{Colors.ENDC} - All tests (default)")
    print(f"  {Colors.CYAN}2{Colors.ENDC} - API endpoint tests")
    print(f"  {Colors.CYAN}3{Colors.ENDC} - Integration tests")
    print(f"  {Colors.CYAN}4{Colors.ENDC} - Character tests")
    print(f"  {Colors.CYAN}5{Colors.ENDC} - Chat tests")
    print(f"  {Colors.CYAN}6{Colors.ENDC} - Feed tests")
    print(f"  {Colors.CYAN}7{Colors.ENDC} - Voice tests")

def main():
    """Main test runner"""
    print_header()
    
    test_dir = Path(__file__).parent
    
    # Ask user for test selection
    print_test_categories()
    
    choice = input(f"\n{Colors.BOLD}Select test category (default: 1): {Colors.ENDC}").strip() or "1"
    
    test_map = {
        "1": (None, False, None, "All Tests"),
        "2": (None, False, "api", "API Endpoint Tests"),
        "3": (None, False, "integration", "Integration Tests"),
        "4": (test_dir / "test_character.py", True, None, "Character Tests"),
        "5": (test_dir / "test_chat.py", True, None, "Chat Tests"),
        "6": (test_dir / "test_feed.py", True, None, "Feed Tests"),
        "7": (test_dir / "test_voice.py", True, None, "Voice Tests"),
    }
    
    if choice not in test_map:
        print(f"{Colors.RED}Invalid choice. Running all tests.{Colors.ENDC}")
        test_file, verbose, markers, category = test_map["1"]
    else:
        test_file, verbose, markers, category = test_map[choice]
    
    print_section(f"Running {category}")
    
    success = run_tests(test_file=test_file, verbose=verbose, markers=markers)
    print_footer(success)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
