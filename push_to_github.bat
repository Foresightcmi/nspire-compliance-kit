@echo off
echo ========================================================
echo   HUD NSPIRE Compliance Kit - Autonomous GitHub Push
echo ========================================================
echo.
echo Pushing branch 'main' to https://github.com/Foresightcmi/nspire-compliance-kit.git ...
git push -u origin main
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Repository pushed to GitHub successfully!
    echo Next step: Connect repository to Vercel or Cloudflare Pages for instant $0/mo deployment.
) else (
    echo.
    echo [NOTICE] If the push failed because the repository does not exist yet:
    echo 1. Open: https://github.com/new?name=nspire-compliance-kit
    echo 2. Click 'Create repository' (leave everything blank).
    echo 3. Run this script again!
)
pause
