param(
    [ValidateSet('status', 'ingest', 'publish', 'run', 'test')]
    [string]$Action = 'status',
    [string[]]$Resource = @(),
    [switch]$Resume
)
# Windows PowerShell turns native stderr (including dbt INFO messages) into error
# records when output is redirected. Judge Docker by its exit code instead.
$ErrorActionPreference = 'Continue'
Push-Location (Split-Path $PSScriptRoot -Parent) -ErrorAction Stop
try {
    if ($Action -eq 'status') {
        docker compose exec -T airflow python -m farol.expenses.status
        if ($LASTEXITCODE -ne 0) { throw 'Cannot read lakehouse status.' }
    }
    if ($Action -eq 'test') {
        docker compose exec -T airflow python -m pytest /opt/lakehouse/tests -q -p no:cacheprovider
        if ($LASTEXITCODE -ne 0) { throw 'Expense tests failed.' }
    }
    if ($Action -in @('ingest', 'run')) {
        $expenseArgs = @()
        foreach ($item in $Resource) { $expenseArgs += @('--resource', $item) }
        if ($Resume) { $expenseArgs += '--resume' }
        docker compose exec -T airflow python -m farol.expenses.pipeline @expenseArgs
        if ($LASTEXITCODE -eq 2) {
            Write-Warning 'Partial coverage: inspect blocked/quarantined resources in status or the coverage dashboard.'
        } elseif ($LASTEXITCODE -ne 0) {
            throw 'Ingestion infrastructure failed. Publication was not attempted.'
        }
    }
    if ($Action -in @('publish', 'run')) {
        docker compose exec -T airflow python -m farol.expenses.publish
        if ($LASTEXITCODE -ne 0) { throw 'Gold checks failed. Previous release remains published.' }
        docker compose exec -T superset python -m farol.expenses.dashboard
        if ($LASTEXITCODE -ne 0) { throw 'Dashboard publication failed. Gold release remains ready for retry.' }
    }
} finally {
    Pop-Location
}
