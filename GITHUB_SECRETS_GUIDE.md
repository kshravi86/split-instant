# GitHub Secrets for iOS IPA Builds (Windows Workflow)

The IPA is produced on GitHub Actions' macOS runners, so you can prepare everything from a Windows laptop. Your only local chores are downloading signing assets from the Apple Developer portal and converting those files to base64 strings with PowerShell/OpenSSL.

> Add secrets in **Repository Settings -> Secrets and variables -> Actions**. Use the exact names below so the workflow can read them.

---

## 1. `IOS_TEAM_ID`

| Aspect | Details |
| --- | --- |
| **Meaning** | 10-character Team ID from your Apple Developer Program membership (example: `A1B2C3D4E5`). |
| **Workflow usage** | Passed to `xcodebuild archive` and export options so the signed archive belongs to your team. |
| **How to obtain** | Sign in at [developer.apple.com/account](https://developer.apple.com/account/), open **Membership**, copy **Team ID**. |
| **Double-check** | Anyone with Xcode can run `xcodebuild -showBuildSettings | findstr DEVELOPMENT_TEAM` to verify the same ID. |

---

## 2. `BUILD_CERTIFICATE_BASE64`

This is the base64 representation of a `.p12` file that bundles your Apple Distribution (or Development) certificate plus its private key. Everything below can be done in Windows PowerShell.

1. **Install OpenSSL**  
   Download a Windows build (for example from [SLProWeb](https://slproweb.com/products/Win32OpenSSL.html)) and ensure `openssl.exe` is on `PATH`.

2. **Generate a CSR and private key**
   ```powershell
   openssl req -new -newkey rsa:2048 -nodes `
     -keyout splitinstant.key `
     -out splitinstant.csr `
     -subj "/CN=split-instant"
   ```

3. **Request the certificate**
   - Go to [Certificates, IDs & Profiles](https://developer.apple.com/account/resources/certificates/list) -> **+**.
   - Choose **Apple Distribution** (or **Apple Development**), upload `splitinstant.csr`, download the resulting `.cer`.

4. **Convert `.cer` + key into `.p12`**
   ```powershell
   openssl x509 -inform DER -in splitinstant.cer -out splitinstant.pem
   openssl pkcs12 -export -inkey splitinstant.key -in splitinstant.pem -out splitinstant.p12
   ```
   Set a strong export password when prompted; you will store it as `P12_PASSWORD`.

5. **Encode the `.p12` for GitHub**
   ```powershell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("splitinstant.p12")) | Set-Clipboard
   ```
   Paste the clipboard contents into the `BUILD_CERTIFICATE_BASE64` secret.

---

## 3. `P12_PASSWORD`

| Aspect | Details |
| --- | --- |
| **Meaning** | Password entered while running `openssl pkcs12 -export`. |
| **Workflow usage** | Unlocks the `.p12` when `apple-actions/import-codesign-certs@v2` runs on GitHub Actions. |
| **Tip** | Whenever you regenerate the `.p12`, update both this secret and `BUILD_CERTIFICATE_BASE64`. |

---

## 4. `PROVISIONING_PROFILE_BASE64`

Provisioning profiles bind the `com.split.instant` bundle identifier to your certificate (and devices, for development/ad-hoc builds).

1. **Create/download the profile**
   - Visit [Certificates, IDs & Profiles -> Profiles](https://developer.apple.com/account/resources/profiles/list).
   - Click **+**, pick the profile type:
     - *App Store* for TestFlight/App Store releases.
     - *Ad Hoc / Release Testing* for sideload builds.
     - *Development* for device debugging.
   - Select the `com.split.instant` App ID and the same certificate used in `splitinstant.p12`.
   - Download the `.mobileprovision` file.

2. **Encode the profile on Windows**
   ```powershell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("SplitInstant_Profile.mobileprovision")) | Set-Clipboard
   ```
   Paste the clipboard contents into the `PROVISIONING_PROFILE_BASE64` secret.

---

## Add the secrets in GitHub

1. Open the repository in a browser.  
2. Go to **Settings -> Secrets and variables -> Actions -> New repository secret**.  
3. Create these entries:

| Secret | Value |
| --- | --- |
| `IOS_TEAM_ID` | 10-character Team ID string. |
| `BUILD_CERTIFICATE_BASE64` | Base64 output from `splitinstant.p12`. |
| `P12_PASSWORD` | Export password from the OpenSSL step. |
| `PROVISIONING_PROFILE_BASE64` | Base64 output from the `.mobileprovision`. |

Trigger the **iOS IPA Build** workflow (push to `main` or run manually) to make sure the secrets are wired correctly.

---

## Troubleshooting reference

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Security: SecKeychainItemImport: User interaction is not allowed` | `P12_PASSWORD` does not match the `.p12`. | Re-export the `.p12` and update both related secrets. |
| `No profiles for 'com.split.instant' were found` | Provisioning profile missing the bundle ID or encoded incorrectly. | Recreate/download the profile and re-run the PowerShell base64 command. |
| `Provisioning profile "profile" doesn't include signing certificate` | Profile references a different certificate than `splitinstant.p12`. | Generate a new profile selecting the matching certificate. |

Keep this guide updated whenever certificates, profiles, or Apple accounts change so Windows users can refresh CI credentials without touching Xcode.
