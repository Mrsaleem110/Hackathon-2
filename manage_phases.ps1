# PowerShell script to manage different phases in separate git branches

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("phase_1", "phase_2", "phase_3", "phase_4", "list", "status")]
    [string]$Command
)

switch ($Command) {
    "phase_1" {
        git checkout main
        $branchExists = git branch --list phase_1
        if ([string]::IsNullOrEmpty($branchExists)) {
            Write-Host "Creating new branch for phase_1..."
            git checkout -b phase_1
        } else {
            Write-Host "Switching to phase_1 branch..."
            git checkout phase_1
        }
    }
    "phase_2" {
        git checkout main
        $branchExists = git branch --list phase_2
        if ([string]::IsNullOrEmpty($branchExists)) {
            Write-Host "Creating new branch for phase_2..."
            git checkout -b phase_2
        } else {
            Write-Host "Switching to phase_2 branch..."
            git checkout phase_2
        }
    }
    "phase_3" {
        git checkout main
        $branchExists = git branch --list phase_3
        if ([string]::IsNullOrEmpty($branchExists)) {
            Write-Host "Creating new branch for phase_3..."
            git checkout -b phase_3
        } else {
            Write-Host "Switching to phase_3 branch..."
            git checkout phase_3
        }
    }
    "phase_4" {
        git checkout main
        $branchExists = git branch --list phase_4
        if ([string]::IsNullOrEmpty($branchExists)) {
            Write-Host "Creating new branch for phase_4..."
            git checkout -b phase_4
        } else {
            Write-Host "Switching to phase_4 branch..."
            git checkout phase_4
        }
    }
    "list" {
        Write-Host "Available branches:"
        git branch -a
    }
    "status" {
        Write-Host "Current branch:"
        git branch --show-current
        Write-Host "Git status:"
        git status
    }
}