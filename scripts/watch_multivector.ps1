while ($true) {
    Clear-Host

    Write-Host "=============================================="
    Write-Host "MULTI-VECTOR INGESTION MONITOR"
    Write-Host "=============================================="
    Write-Host ""

    python scripts\check_multivector.py

    Write-Host ""
    Write-Host "Target: 2540 vectors / 635 parents"
    Write-Host "Next check in 30 seconds..."
    Write-Host ""

    Start-Sleep -Seconds 30
}