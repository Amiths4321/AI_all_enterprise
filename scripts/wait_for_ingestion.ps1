$expectedVectors = 2540
$expectedParents = 635

while ($true) {
    Clear-Host

    Write-Host "============================================================"
    Write-Host "ENTERPRISE RAG - INGESTION MONITOR"
    Write-Host "============================================================"
    Write-Host ""

    python scripts\check_multivector.py

    Write-Host ""

    $output = python scripts\check_multivector.py | Out-String

    if (
        $output -match "Total vectors:\s+$expectedVectors/$expectedVectors" -and
        $output -match "Unique parents represented:\s+$expectedParents/$expectedParents"
    ) {
        Write-Host ""
        Write-Host "============================================================"
        Write-Host "INGESTION COMPLETE"
        Write-Host "============================================================"
        Write-Host ""
        Write-Host "You can now run:"
        Write-Host ""
        Write-Host "python scripts\validate_multivector.py"
        Write-Host "python scripts\validate_benchmark_dataset.py"
        Write-Host "python scripts\run_full_benchmark.py"
        Write-Host ""
        break
    }

    Write-Host ""
    Write-Host "Checking again in 30 seconds..."
    Start-Sleep -Seconds 30
}