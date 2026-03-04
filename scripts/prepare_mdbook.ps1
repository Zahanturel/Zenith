# Prepare mdBook src/ by copying index.md and chapters/*.md into src/.
# Run this before 'mdbook build' or 'mdbook serve'.
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BookRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SrcDir = Join-Path $BookRoot "src"
$ChaptersDir = Join-Path $BookRoot "chapters"

New-Item -ItemType Directory -Force -Path $SrcDir | Out-Null

# Copy index.md and fix links for mdBook (chapters/XX -> XX)
$indexPath = Join-Path $BookRoot "index.md"
if (Test-Path $indexPath) {
  (Get-Content $indexPath -Raw) -replace '\]\(chapters/', '](' | Set-Content (Join-Path $SrcDir "index.md") -NoNewline
  Write-Host "Wrote $SrcDir\index.md"
}

# Copy references.md if present
$refPath = Join-Path $BookRoot "references.md"
if (Test-Path $refPath) {
  Copy-Item $refPath (Join-Path $SrcDir "references.md") -Force
  Write-Host "Wrote $SrcDir\references.md"
}

# Copy full-specification.md if present (single-file version for built book)
$fullSpecPath = Join-Path $BookRoot "full-specification.md"
if (Test-Path $fullSpecPath) {
  Copy-Item $fullSpecPath (Join-Path $SrcDir "full-specification.md") -Force
  Write-Host "Wrote $SrcDir\full-specification.md"
}

# Copy all chapter markdown files
Get-ChildItem -Path $ChaptersDir -Filter "*.md" | ForEach-Object {
  Copy-Item $_.FullName (Join-Path $SrcDir $_.Name) -Force
  Write-Host "Wrote $SrcDir\$($_.Name)"
}

Write-Host "Done. Run 'mdbook build' or 'mdbook serve' from the repo root."
