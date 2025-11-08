# Firestore Setup Guide

This guide will help you set up Firestore credentials for the Canvas TA-Bot project.

## Prerequisites

- Google Cloud Platform (GCP) account
- A GCP project with Firestore enabled
- Service account with Firestore permissions

---

## Option 1: Service Account Key (Recommended for Development)

### Step 1: Create a Service Account

1. Go to [GCP Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **IAM & Admin > Service Accounts**
4. Click **Create Service Account**
5. Enter a name (e.g., "canvas-tabot-firestore")
6. Click **Create and Continue**

### Step 2: Grant Firestore Permissions

Add these roles to your service account:
- **Cloud Datastore User** (for Firestore in Datastore mode)
- OR **Cloud Firestore User** (for Firestore in Native mode)

### Step 3: Create and Download Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key > Create new key**
4. Choose **JSON** format
5. Click **Create**
6. Save the downloaded file as `service-account.json` in your project root

### Step 4: Update Environment Variables

Edit your `.env` file:

```bash
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=service-account.json
```

### Step 5: Test the Connection

Run the Firestore service test:

```bash
python app/services/firestore_service.py
```

You should see output similar to:
---

## Option 2: Application Default Credentials (ADC)

This is useful if you're running on your local machine and already authenticated with `gcloud`.

### Step 1: Install Google Cloud SDK

Download from: https://cloud.google.com/sdk/docs/install

### Step 2: Authenticate

```bash
gcloud auth application-default login
```

This will open a browser for authentication.

### Step 3: Set Your Project

```bash
gcloud config set project YOUR_PROJECT_ID
```

### Step 4: Update Environment Variables

Edit your `.env` file:

```bash
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
# No need to set GOOGLE_APPLICATION_CREDENTIALS
```

### Step 5: Test the Connection

```bash
python app/services/firestore_service.py
```

---

## Enable Firestore in Your GCP Project

If you haven't enabled Firestore yet:

1. Go to [Firestore Console](https://console.cloud.google.com/firestore)
2. Click **Select Native Mode** (recommended) or **Datastore Mode**
3. Choose a location (e.g., `us-central`)
4. Click **Create Database**

---

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Solution:** Make sure either:
- Your service account JSON file exists at the path specified in `GOOGLE_APPLICATION_CREDENTIALS`
- OR you've run `gcloud auth application-default login`

### Error: "Permission denied"

**Solution:** Your service account needs these permissions:
- `datastore.entities.create`
- `datastore.entities.get`
- `datastore.entities.update`
- `datastore.entities.delete`

Add the **Cloud Datastore User** or **Cloud Firestore User** role.

### Error: "Project not found"

**Solution:** Make sure `GOOGLE_CLOUD_PROJECT` in `.env` matches your actual GCP project ID.

### Error: "Service account JSON not found"

**Solution:** 
```bash
# Check if file exists
ls service-account.json

# If not, make sure you downloaded it to the right location
# The path in .env should be relative to project root
```

---

## Verify Your Setup

Run this command to verify everything is working:

```bash
python -c "from app.services import firestore_service; print('Firestore DB:', firestore_service.db)"
```

If successful, you'll see the Firestore client object printed.

---

## Security Best Practices

1. **Never commit service account keys to Git**
   - Add `service-account.json` to `.gitignore` (already done)
   - Use environment variables for sensitive data

2. **Use minimal permissions**
   - Only grant the permissions your app actually needs
   - For production, use separate service accounts for different environments

3. **Rotate keys regularly**
   - Create new keys every 90 days
   - Delete old keys after rotation

4. **For production deployment**
   - Use Workload Identity (GKE)
   - Or use Cloud Run's built-in service account
   - Never use downloaded key files in production

---

## Next Steps

Once Firestore is set up:

1. ✅ Test the connection: `python app/services/firestore_service.py`
2. ✅ Run the initialization test: `python test_quick.py`
3. ✅ Start the Flask app: `python run.py`

---

## Quick Reference

### Environment Variables Needed

```bash
GOOGLE_CLOUD_PROJECT=your-project-id          # Required
GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json  # Optional if using ADC
```

### Test Command

```bash
python app/services/firestore_service.py
```

### Service Account Roles

- **Cloud Firestore User** (Native mode)
- **Cloud Datastore User** (Datastore mode)
