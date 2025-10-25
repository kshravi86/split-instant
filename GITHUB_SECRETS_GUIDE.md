# GitHub Secrets for iOS CI/CD

This document explains the purpose of the secrets required for the `ios-build-ipa.yml` GitHub Actions workflow, how to obtain them, and why they are necessary for building and signing an iOS application.

## 1. `IOS_TEAM_ID`

| Aspect | Description |
| :--- | :--- |
| **Purpose** | Identifies your Apple Developer Program team. It is used by Xcode to correctly sign the application. |
| **Why Needed** | Required for manual code signing to specify which development team is responsible for the app. |
| **How to Get** | Log in to the [Apple Developer website](https://developer.apple.com/account/). The Team ID is listed under the **Membership** section. |
| **Diagram** | `Apple Developer Account -> Membership -> Team ID (e.g., A1B2C3D4E5)` |

## 2. `BUILD_CERTIFICATE_BASE64` (P12 File)

| Aspect | Description |
| :--- | :--- |
| **Purpose** | Contains the private key and public certificate used to cryptographically sign your application, proving its origin. This is the base64 encoded content of your `.p12` file. |
| **Why Needed** | Apple requires all apps to be signed with a valid certificate issued by them before they can be installed on a device or submitted to the App Store. |
| **How to Get** | 1. Create a signing certificate (e.g., "Apple Distribution" or "iOS Development") via Xcode or the Apple Developer website. 2. Export the certificate and its private key from your macOS Keychain Access utility as a `.p12` file. 3. Convert the `.p12` file to a base64 string using a command like: `base64 -i your_cert.p12` (on macOS/Linux) or equivalent tool. |
| **Diagram** | `Keychain Access -> Export Certificate + Key -> .p12 file -> base64 encoding -> SECRET` |

## 3. `P12_PASSWORD`

| Aspect | Description |
| :--- | :--- |
| **Purpose** | The password you set when exporting the `.p12` file. |
| **Why Needed** | The `.p12` file is password-protected to secure the private key. The CI/CD process needs this password to unlock and import the certificate into the runner's keychain. |
| **How to Get** | This is the password you chose during the `.p12` export process. |
| **Diagram** | `(User-defined password during .p12 export)` |

## 4. `PROVISIONING_PROFILE_BASE64` (Mobile Provisioning Profile)

| Aspect | Description |
| :--- | :--- |
| **Purpose** | A file that links the App ID, the signing certificate, and the devices (for development/ad-hoc builds). This is the base64 encoded content of your `.mobileprovision` file. |
| **Why Needed** | It authorizes the app to run on specific devices (non-App Store builds) and defines the app's capabilities (entitlements). The CI/CD process needs this to correctly provision the build. |
| **How to Get** | 1. Create a Provisioning Profile (e.g., "App Store," "Ad Hoc," or "Development") on the [Apple Developer website](https://developer.apple.com/account/). 2. Download the `.mobileprovision` file. 3. Convert the `.mobileprovision` file to a base64 string using a command like: `base64 -i your_profile.mobileprovision` (on macOS/Linux) or equivalent tool. |
| **Diagram** | `Apple Developer Account -> Profiles -> Download .mobileprovision -> base64 encoding -> SECRET` |

---

**Final Step:** Store these four values as secrets in your GitHub repository settings under **Settings > Secrets and variables > Actions**.
