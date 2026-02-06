#!/bin/bash

# Script to manage different phases in separate git branches

case $1 in
  "phase_1")
    git checkout main
    if ! git rev-parse --verify phase_1 >/dev/null 2>&1; then
      echo "Creating new branch for phase_1..."
      git checkout -b phase_1
    else
      echo "Switching to phase_1 branch..."
      git checkout phase_1
    fi
    ;;
  "phase_2")
    git checkout main
    if ! git rev-parse --verify phase_2 >/dev/null 2>&1; then
      echo "Creating new branch for phase_2..."
      git checkout -b phase_2
    else
      echo "Switching to phase_2 branch..."
      git checkout phase_2
    fi
    ;;
  "phase_3")
    git checkout main
    if ! git rev-parse --verify phase_3 >/dev/null 2>&1; then
      echo "Creating new branch for phase_3..."
      git checkout -b phase_3
    else
      echo "Switching to phase_3 branch..."
      git checkout phase_3
    fi
    ;;
  "phase_4")
    git checkout main
    if ! git rev-parse --verify phase_4 >/dev/null 2>&1; then
      echo "Creating new branch for phase_4..."
      git checkout -b phase_4
    else
      echo "Switching to phase_4 branch..."
      git checkout phase_4
    fi
    ;;
  "list")
    echo "Available branches:"
    git branch -a
    ;;
  "status")
    echo "Current branch:"
    git branch --show-current
    echo "Git status:"
    git status
    ;;
  *)
    echo "Usage: $0 {phase_1|phase_2|phase_3|phase_4|list|status}"
    echo ""
    echo "Commands:"
    echo "  phase_1   - Switch to or create phase_1 branch"
    echo "  phase_2   - Switch to or create phase_2 branch"
    echo "  phase_3   - Switch to or create phase_3 branch"
    echo "  phase_4   - Switch to or create phase_4 branch"
    echo "  list      - List all branches"
    echo "  status    - Show current branch and status"
    ;;
esac