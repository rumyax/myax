$pythonScript = Join-Path $PSScriptRoot 'myax.py'
python $pythonScript @args
exit $LASTEXITCODE
