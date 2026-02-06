# Phase Management Guide

This guide explains how to manage different phases of your project independently using Git branches.

## Problem
Currently, all phases (phase_1, phase_2, phase_3, phase_4) exist as directories in the same repository. When you make commits, they affect the entire repository, potentially mixing changes from different phases.

## Solution
Use separate Git branches for each phase to keep them isolated from each other.

## Scripts Provided

Three scripts are provided to help manage phases:

1. `manage_phases.bat` - For Windows Command Prompt
2. `manage_phases.ps1` - For Windows PowerShell
3. `manage_phases.sh` - For Unix/Linux/Mac systems

## How to Use

### Before committing Phase 1:
```bash
# On Windows
manage_phases.bat phase_1
# Then make your changes and commit
git add .
git commit -m "Update for phase 1"
```

### Before committing Phase 2:
```bash
# On Windows
manage_phases.bat phase_2
# Then make your changes and commit
git add .
git commit -m "Update for phase 2"
```

### Before committing Phase 3:
```bash
# On Windows
manage_phases.bat phase_3
# Then make your changes and commit
git add .
git commit -m "Update for phase 3"
```

### Before committing Phase 4:
```bash
# On Windows
manage_phases.bat phase_4
# Then make your changes and commit
git add .
git commit -m "Update for phase 4"
```

### Check current status:
```bash
manage_phases.bat status
```

### List all phase branches:
```bash
manage_phases.bat list
```

## Benefits

1. **Isolation**: Changes in one phase won't affect others
2. **History**: Each phase has its own commit history
3. **Flexibility**: You can work on any phase independently
4. **Safety**: Mistakes in one phase won't break others

## Best Practices

1. Always switch to the appropriate phase branch before making changes
2. Commit frequently to track progress in each phase
3. Use descriptive commit messages that indicate what was changed
4. Regularly push your phase branches to remote to backup your work

## Alternative Manual Method

If you prefer to manage branches manually:

```bash
# Create and switch to phase-specific branch
git checkout -b phase_1  # First time only
git checkout phase_1     # Subsequent times

# Make your changes to phase_1 directory
# Then commit
git add .
git commit -m "Description of changes to phase 1"

# Repeat for other phases
git checkout -b phase_2  # First time only
git checkout phase_2     # Subsequent times
# ... and so on
```