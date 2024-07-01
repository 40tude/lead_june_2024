./secrets.ps1

$runtimeEnvJson = @{
    working_dir = "./"
    pip = @("ray[train]", "tensorflow")
    env_vars = @{
        AWS_ACCESS_KEY_ID = $env:AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = $env:AWS_SECRET_ACCESS_KEY
    }
} | ConvertTo-Json -Compress

$runtimeEnvJsonEscaped = $runtimeEnvJson -replace '"', '\"'

ray job submit --runtime-env-json="$runtimeEnvJsonEscaped" --address="http://127.0.0.1:8265" -- python autonomous_car.py
