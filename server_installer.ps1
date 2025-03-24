$global:PythonCommand = ""
$global:defaultPath = "C:/Program Files/ASC Timer Server"
$global:defaultPort = "80"
# Ensure script is running as Administrator
function Check-Admin {
    $currentUser = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
    $isAdmin = $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    $response = Read-Host "Detected non-administrative priviliges. If installed without administrative privileges, 
    the server will not be able to host the app on port 80 or 443 and you will need to specify a different port.
    Would you like me to elevate permissions (Y) or continue with installation as a non-administrative user (N)?"
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Output "Restarting with elevated permissions..."
        Start-Process powershell -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
        exit
    }
    else {
        Write-Output "updating default path to AppData/Local..."
        $global:defaultPath = (Join-Path $env:LOCALAPPDATA "") + "ASC Timer Server"
        Write-Output "updating default port to 8000..."
        $global:defaultPort = "8000"
    }
}

function Install-Python {
    Write-Output "Checking for Python 3.12 or above..."
    
    $pythonVersion = python --version 2>&1
    $global:PythonCommand = "python.exe"

    if ($pythonVersion -notmatch "Python (\d+)\.(\d+)\.(\d+)") {
        $pythonVersion = python3.exe --version 2>&1
        $global:PythonCommand = "python3.exe"
    }

    if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 12)) {
            Write-Output "Python $pythonVersion is installed and meets the requirement. Using $global:PythonCommand."
            return
        } else {
            Write-Output "Python version $pythonVersion is below the required 3.12."
        }
    } else {
        Write-Output "Python not found or not correctly installed."
    }

    $response = Read-Host "Would you like to download and install Python 3.12? (Y/N)"
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Output "Downloading and installing Python 3.12..."
        $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe"
        $installerPath = "$env:TEMP\python-installer.exe"
        Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath
        Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        Write-Output "Python 3.12 installed successfully."
        $global:PythonCommand = "python.exe"
    } else {
        Write-Output "Python installation skipped. Exiting."
        exit 1
    }
} 

function Setup-VenvAndDependencies {
    $response = Read-Host "Would you like to use the default virtual environment path ($defaultPath)? (Y/N)"

    if ($response -eq 'Y' -or $response -eq 'y') {
        $global:VenvPath = $defaultPath
    } else {
        do {
            $global:VenvPath = Read-Host "Enter your desired path for the virtual environment"
            if (-Not (Test-Path $global:VenvPath)) {
                try {
                    New-Item -ItemType Directory -Path $global:VenvPath -Force
                    Write-Output "Directory created: $global:VenvPath"
                } catch {
                    Write-Output "Failed to create directory. Please enter a valid path."
                    $global:VenvPath = ""
                }
            }
        } while (-Not (Test-Path $global:VenvPath))
    }

    Write-Output "Setting up virtual environment at $global:VenvPath..."
    & $global:PythonCommand -m venv "$global:VenvPath"

    Write-Output "Modifying script execution policy for this process to enable virtual environment activation script..."
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
    Write-Output "Activating virtual environment and installing dependencies..."
    & "$global:VenvPath/Scripts/Activate.ps1"
    & pip install -r requirements.txt
    Write-Output "Virtual environment setup complete."
    deactivate
}



# Main Execution
Write-Output "Starting Installer..."
Check-Admin
Install-Python
Setup-VenvAndDependencies
# Configure-App
Write-Output "Installation and configuration complete! You can now run your Django server."



# Configure Application
function Configure-App {
    Write-Output "Configuring the application..."
    $configPath = ".\config.json"
    if (-not (Test-Path $configPath)) {
        Write-Output "Template config.json not found. Creating from default..."
        @"
{
  "DATABASE_HOST": "<DATABASE_HOST>",
  "DATABASE_PORT": "<DATABASE_PORT>",
  "DATABASE_USER": "<DATABASE_USER>",
  "DATABASE_PASSWORD": "<DATABASE_PASSWORD>"
}
"@ | Out-File -FilePath $configPath
    }

    $config = Get-Content $configPath | ConvertFrom-Json

    $config.DATABASE_HOST = Read-Host "Enter Database Host (e.g., localhost)"
    $config.DATABASE_PORT = Read-Host "Enter Database Port (e.g., 5432)"
    $config.DATABASE_USER = Read-Host "Enter Database User"
    $config.DATABASE_PASSWORD = Read-Host "Enter Database Password"

    $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
    Write-Output "Configuration saved to config.json."
}

