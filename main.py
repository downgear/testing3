"""
Main Test Runner for Feature 1 and Feature 8 Tests
Provides interactive menu to run tests at different levels with optional filtering.
"""

import sys
import subprocess
from pathlib import Path


def get_test_module_name(level, feature, test_type):
    """
    Construct the test module name based on level, feature, and test type.
    Dynamically finds script files matching the pattern.

    Args:
        level (int): 1 or 2
        feature (int): Feature number
        test_type (str): 'standard', 'scenario', or 'all'

    Returns:
        tuple: (module_name, script_path)
    """
    base_path = Path(__file__).parent / f"Level-{level}" / f"Feature-{feature}"

    if not base_path.exists():
        return None, base_path

    # Find script files dynamically
    scripts = {
        'standard': None,
        'scenario': None
    }

    for script_file in base_path.glob(f"Feature-{feature}-script-*.py"):
        name = script_file.name
        # Check if it's standard tests (numeric range like 001-033) or scenario (like 034-036)
        if 'script-001' in name or 'script-00' in name:
            # Could be standard or scenario, check the range
            if 'script-001-0' in name or 'script-001-03' in name or 'script-001-1' in name:
                scripts['standard'] = script_file
            elif any(f'script-0{i}' in name for i in range(3, 10)):  # 034-039 for scenarios
                scripts['scenario'] = script_file
        # Alternative: scenario tests often start from higher numbers
        elif any(f'script-{i}' in name for i in range(34, 40)):
            scripts['scenario'] = script_file

    # Fallback: match by common patterns
    if not scripts['standard']:
        for script_file in sorted(base_path.glob(f"Feature-{feature}-script-001*.py")):
            scripts['standard'] = script_file
            break

    if not scripts['scenario']:
        for script_file in sorted(base_path.glob(f"Feature-{feature}-script-03*.py")):
            scripts['scenario'] = script_file
            break

    if test_type == 'all':
        return None, base_path

    script_path = scripts.get(test_type)
    if script_path:
        return script_path.name.replace('.py', ''), script_path

    return None, None


def run_tests(level, feature, test_type):
    """
    Run the specified tests by executing test scripts directly.
    Dynamically discovers and runs available test scripts.

    Args:
        level (int): 1 or 2
        feature (int): Feature number
        test_type (str): 'standard', 'scenario', or 'all'
    """
    base_path = Path(__file__).parent / f"Level-{level}" / f"Feature-{feature}"

    if not base_path.exists():
        print(f"\nError: Path does not exist: {base_path}")
        return False

    print(f"\n{'=' * 70}")
    print(f"Running Feature {feature} Level {level} - {test_type.upper()} Tests")
    print(f"{'=' * 70}\n")

    # Find script files
    scripts_to_run = []

    if test_type == 'all':
        # Find both standard and scenario scripts
        scripts_to_run = sorted(base_path.glob(f"Feature-{feature}-script-*.py"))
    else:
        # Find specific test type
        if test_type == 'standard':
            # Standard tests typically start with 001-0xx
            candidates = sorted(base_path.glob(f"Feature-{feature}-script-001*.py"))
        else:  # scenario
            # Scenario tests typically start with higher numbers (034+)
            candidates = sorted(base_path.glob(f"Feature-{feature}-script-03*.py"))
            if not candidates:
                candidates = sorted(base_path.glob(f"Feature-{feature}-script-[3-9]*.py"))

        scripts_to_run = candidates

    if not scripts_to_run:
        print(f"No test scripts found for Feature {feature} Level {level}")
        return False

    all_passed = True

    for script_path in scripts_to_run:
        script_name = script_path.name

        print(f"Running: {script_name}")
        print("-" * 70)

        try:
            # Run the test script directly using subprocess
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(base_path),
                capture_output=False
            )

            if result.returncode != 0:
                all_passed = False
                print(f"{script_name} returned exit code {result.returncode}")
            else:
                print(f"{script_name} completed.")

        except Exception as e:
            print(f"Error running {script_name}: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

        print()

    print(f"{'=' * 70}\n")
    return all_passed


def display_main_menu():
    """Display main menu and get user choice."""
    print("\n" + "=" * 70)
    print("TEST RUNNER - Feature 1 & Feature 8 Test Suites")
    print("=" * 70)
    print("\nSelect Level:")
    print("  1) Level 1 (Original with hardcoded selectors)")
    print("  2) Level 2 (Configuration-driven with externalized selectors)")
    print("  0) Exit")

    choice = input("\nEnter choice (0-2): ").strip()
    return choice


def get_available_features(level):
    """Get list of available features for a given level."""
    base_path = Path(__file__).parent / f"Level-{level}"
    features = []

    if base_path.exists():
        for feature_dir in base_path.iterdir():
            if feature_dir.is_dir() and feature_dir.name.startswith("Feature-"):
                feature_num = feature_dir.name.replace("Feature-", "")
                features.append(feature_num)

        # Sort numerically by converting to int
        features.sort(key=lambda x: int(x))

    return features


def get_feature_description(feature):
    """Get description for a feature."""
    descriptions = {
        "1": "User Registration",
        "3": "Browse Products",
        "8": "Gift Certificate Purchase",
        "9": "Search Functionality"
    }
    return descriptions.get(feature, f"Feature {feature}")


def display_feature_menu(level):
    """Display feature menu and get user choice."""
    features = get_available_features(level)

    if not features:
        print(f"\nNo features available for Level {level}")
        return "0"

    print(f"\nSelect Feature (Level {level}):")
    for idx, feature in enumerate(features, 1):
        desc = get_feature_description(feature)
        print(f"  {idx}) Feature {feature} ({desc})")
    print(f"  0) Back to Main Menu")

    choice = input(f"\nEnter choice (0-{len(features)}): ").strip()

    # Convert menu index to feature number
    if choice == "0":
        return "0"

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(features):
            return features[idx]
    except ValueError:
        pass

    return None


def count_test_scripts(level, feature):
    """Count how many test scripts are available for a feature."""
    base_path = Path(__file__).parent / f"Level-{level}" / f"Feature-{feature}"
    if not base_path.exists():
        return 0
    return len(list(base_path.glob(f"Feature-{feature}-script-*.py")))


def display_test_type_menu(level, feature):
    """Display test type menu based on available scripts."""
    script_count = count_test_scripts(level, feature)

    if script_count <= 1:
        # Single script: show minimal menu
        print("\nThis feature has a single test script.")
        print("  1) Run Tests")
        print("  0) Back to Previous Menu")
        choice = input("\nEnter choice (0-1): ").strip()

        if choice == "1":
            return "all"
        else:
            return "0"
    else:
        # Multiple scripts: show full menu
        print("\nSelect Test Type:")
        print("  1) Standard Tests (Core functionality)")
        print("  2) Scenario Tests (Complex workflows)")
        print("  3) All Tests (Standard + Scenario)")
        print("  0) Back to Previous Menu")

        choice = input("\nEnter choice (0-3): ").strip()
        return choice


def main():
    """Main entry point with interactive menu."""
    while True:
        level_choice = display_main_menu()

        if level_choice == '0':
            print("\nExiting. Goodbye!\n")
            sys.exit(0)
        elif level_choice not in ['1', '2']:
            print("\nInvalid choice. Please try again.")
            continue

        level = int(level_choice)

        while True:
            feature_choice = display_feature_menu(level)

            if feature_choice == "0":
                break
            elif feature_choice is None:
                print("\nInvalid choice. Please try again.")
                continue

            feature = int(feature_choice)

            while True:
                test_type_choice = display_test_type_menu(level, feature)

                if test_type_choice == '0':
                    break
                elif test_type_choice == '1':
                    test_type = 'standard'
                elif test_type_choice == '2':
                    test_type = 'scenario'
                elif test_type_choice == '3' or test_type_choice == 'all':
                    test_type = 'all'
                else:
                    print("\nInvalid choice. Please try again.")
                    continue

                # Run tests
                success = run_tests(level, feature, test_type)

                if not success:
                    print("\nSome tests failed or errors occurred.")
                else:
                    print("\nAll tests run!")

                input("Press Enter to continue...")
                break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
