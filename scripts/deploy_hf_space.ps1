# Deploy Button Switch Module to Hugging Face Spaces
# Usage: $env:HF_TOKEN="hf_..."; .\scripts\deploy_hf_space.ps1

param(
    [string]$SpaceId = "DJKang-IM/button-switch-module",
    [string]$Token = $env:HF_TOKEN
)

if (-not $Token) {
    Write-Error "HF_TOKEN not set. Get a write token from https://huggingface.co/settings/tokens"
    exit 1
}

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$SpaceDir = Join-Path $Root "hf-space"

Write-Host "Logging in to Hugging Face..."
hf auth login --token $Token

Write-Host "Creating Space: $SpaceId ..."
python -c @"
from huggingface_hub import HfApi
api = HfApi(token='$Token')
try:
    api.create_repo(
        repo_id='$SpaceId',
        repo_type='space',
        space_sdk='gradio',
        private=False,
        exist_ok=True,
    )
    print('Space ready.')
except Exception as e:
    print(f'create_repo: {e}')
"@

Write-Host "Pushing Space files..."
Push-Location $SpaceDir
if (-not (Test-Path ".git")) { git init -b main }
git add -A
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "Deploy BSM documentation Space"
}
git remote remove origin 2>$null
git remote add origin "https://DJKang-IM:$Token@huggingface.co/spaces/$SpaceId"
git push -u origin main --force
Pop-Location

Write-Host "Done: https://huggingface.co/spaces/$SpaceId"
