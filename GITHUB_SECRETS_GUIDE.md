# GitHub Secrets for iOS IPA Builds

The workflow at `.github/workflows/ios-build-ipa.yml` imports four secrets to sign and export the `split-instant` IPA. This guide explains why each secret matters, how to generate it, and how to store it in GitHub.

> **Tip:** Add secrets in **Repository Settings -> Secrets and variables -> Actions**. Use the exact names below; missing values cause the workflow to stop before archiving.

---

## 1. `IOS_TEAM_ID`

| Aspect | Details |
| --- | --- |
| **Meaning** | 10-character Team ID assigned to your Apple Developer Program membership (example: `A1B2C3D4E5`). |
| **Workflow usage** | Passed to `xcodebuild archive` and the export plist so the runner signs as your team. |
| **How to obtain** | 1. Sign in at [developer.apple.com/account](https://developer.apple.com/account/). 2. Open **Membership** and copy **Team ID**. |
| **Double-check** | Run `xcodebuild -showBuildSettings | grep DEVELOPMENT_TEAM` locally; the value should match. |

---

## 2. `BUILD_CERTIFICATE_BASE64`

This is the base64-encoded `.p12` that contains your Apple Distribution (or Development) certificate plus its private key.

### Why the workflow needs it
`apple-actions/import-codesign-certs@v2` imports the certificate so `xcodebuild` can sign the archive. Without it, the exported IPA cannot be installed.

### Create and export the certificate
1. **Create/download the cert**
   - Xcode: *Settings -> Accounts -> Manage Certificates -> + -> Apple Distribution* (or Development).
   - Web: [Certificates, IDs & Profiles](https://developer.apple.com/account/resources/certificates/list) -> plus button -> follow the prompts.
2. **Export as `.p12`**
   - Keychain Access -> *My Certificates* -> right-click the certificate -> **Export** -> choose `.p12` -> set a strong password (remember it for `P12_PASSWORD`).

### Convert `.p12` to base64
- **macOS/Linux:** `base64 -i split-instant-dist.p12 | pbcopy`
- **Windows PowerShell:** `[Convert]::ToBase64String([IO.File]::ReadAllBytes("split-instant-dist.p12")) | Set-Clipboard`

Paste the single-line string into the `BUILD_CERTIFICATE_BASE64` secret.

---

## 3. `P12_PASSWORD`

| Aspect | Details |
| --- | --- |
| **Meaning** | Password set while exporting the `.p12`. |
| **Workflow usage** | Supplied to the certificate import action so the runner can unlock the private key. |
| **Notes** | Whenever you export a new `.p12`, update both `BUILD_CERTIFICATE_BASE64` and `P12_PASSWORD`. |

---

## 4. `PROVISIONING_PROFILE_BASE64`

The provisioning profile binds `com.split.instant` to your certificate, entitlements, and (optionally) device UDIDs.

### Choose the right profile type
- **App Store**: For TestFlight/App Store submissions.
- **Ad Hoc / Release Testing**: For distributing signed builds outside the store.
- **Development**: For debugging builds that run on registered devices.

### Create/download the profile
1. Visit [Certificates, IDs & Profiles -> Profiles](https://developer.apple.com/account/resources/profiles/list).
2. Click **+**, pick the profile type, select the `com.split.instant` App ID, choose the same certificate used in the `.p12`, pick devices if prompted, name the profile, and download the `.mobileprovision`.

### Encode to base64
- **macOS/Linux:** `base64 -i SplitInstant_Profile.mobileprovision | pbcopy`
- **Windows PowerShell:** `[Convert]::ToBase64String([IO.File]::ReadAllBytes("SplitInstant_Profile.mobileprovision")) | Set-Clipboard`

Paste the encoded string into `PROVISIONING_PROFILE_BASE64`.

---

## Add the secrets in GitHub

1. Open the repository in a browser.
2. Go to **Settings -> Secrets and variables -> Actions -> New repository secret**.
3. Add each entry:

| Secret | Value |
| --- | --- |
| `IOS_TEAM_ID` | Team ID string (10 characters). |
| `BUILD_CERTIFICATE_BASE64` | Base64 string of the `.p12`. |
| `P12_PASSWORD` | Password used when exporting the `.p12`. |
| `PROVISIONING_PROFILE_BASE64` | Base64 string of the `.mobileprovision`. |

4. Push to `main` or trigger the **iOS IPA Build** workflow manually to confirm the secrets are read successfully.

---

## Troubleshooting reference

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Security: SecKeychainItemImport: User interaction is not allowed` | `P12_PASSWORD` is wrong or blank. | Re-export the `.p12`, update both secrets. |
| `No profiles for 'com.split.instant' were found` | Provisioning profile lacks the bundle ID or was encoded incorrectly. | Regenerate the profile and re-encode it. |
| `Provisioning profile "profile" doesn't include signing certificate` | Profile references a different certificate than the `.p12`. | Create a new profile selecting the matching certificate. |

Keep this file up to date whenever certificates, profiles, or Apple accounts change so future contributors can refresh the CI signing assets quickly.
