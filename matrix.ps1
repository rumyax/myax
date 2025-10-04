$pythonScript = Join-Path $PSScriptRoot 'matrix.py'
python $pythonScript @args
exit $LASTEXITCODE
