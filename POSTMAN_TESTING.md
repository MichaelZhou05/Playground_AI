# Postman API Testing Guide

This guide explains how to test the Canvas TA-Bot API endpoints using Postman.

## Quick Start

### 1. Import the Collection

1. Open Postman
2. Click **Import** (top left)
3. Click **Upload Files**
4. Select `Canvas_TA_Bot_Postman_Collection.json`
5. Click **Import**

You should now see "Canvas TA-Bot API" in your Collections.

---

## 2. Start the Flask Server

Before testing, make sure your Flask app is running:

```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

---

## 3. Test the Endpoints

### 🚀 **Initialize Course** (Main Endpoint)

**What it does:** Creates RAG corpus + Knowledge Graph for a course

**Steps:**
1. Select "Initialize Course" from the collection
2. Update the request body:
   ```json
   {
       "course_id": "YOUR_CANVAS_COURSE_ID",
       "topics": "Machine Learning,Neural Networks,Deep Learning"
   }
   ```
3. Click **Send**

**Expected Response (Success):**
```json
{
    "status": "complete",
    "corpus_id": "projects/.../ragCorpora/...",
    "files_count": 15,
    "uploaded_count": 15
}
```

**Expected Response (Error):**
```json
{
    "error": "Failed to initialize course",
    "message": "No course files found"
}
```

⏱️ **Note:** This is a long-running request (may take 2-5 minutes)

---

### 💬 **Chat with TA Bot**

**What it does:** Ask questions about course materials

**Steps:**
1. Select "Chat with TA Bot" from the collection
2. Update the request body:
   ```json
   {
       "course_id": "12345",
       "query": "What is machine learning?"
   }
   ```
3. Click **Send**

**Expected Response:**
```json
{
    "answer": "Machine learning is a subset of AI...",
    "sources": ["Chapter1.pdf", "Lecture2.pdf"]
}
```

---

### 🕸️ **Get Knowledge Graph**

**What it does:** Retrieves graph data for visualization

**Steps:**
1. Select "Get Knowledge Graph" from the collection
2. Update the query parameter `course_id` to your course ID
3. Click **Send**

**Expected Response:**
```json
{
    "nodes": "[{\"id\":\"topic_1\",\"label\":\"Machine Learning\",...}]",
    "edges": "[{\"from\":\"topic_1\",\"to\":\"file_1\"}]",
    "data": "{\"topic_1\":{\"summary\":\"...\",\"sources\":[...]}}"
}
```

---

### 🎓 **LTI Launch** (Canvas Entry Point)

**What it does:** Simulates Canvas launching the app

**Steps:**
1. Select "LTI Launch (Canvas Entry Point)" from the collection
2. Update form data if needed:
   - `context_id`: Your course ID
   - `roles`: "Instructor" or "Student"
3. Click **Send**

**Expected Response:**
HTML page with the single-page application

---

## Configuration

### Environment Variables

The collection uses these variables (can be changed in Postman):

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `base_url` | `http://localhost:5000` | Flask server URL |
| `course_id` | `12345` | Default course ID for testing |

**To change:**
1. Click on "Canvas TA-Bot API" collection
2. Go to **Variables** tab
3. Update **Current Value**
4. Click **Save**

---

## Common Issues

### ❌ Connection Refused

**Problem:** `Could not send request`

**Solution:** 
- Make sure Flask is running: `python run.py`
- Check the URL is `http://localhost:5000`

### ❌ 400 Bad Request

**Problem:** `{"error": "course_id is required"}`

**Solution:**
- Make sure you're sending JSON with `course_id` in the body
- Check Content-Type header is `application/json`

### ❌ 404 Not Found

**Problem:** Route doesn't exist

**Solution:**
- Check the endpoint URL matches your routes
- Make sure Flask app has registered the routes

### ❌ 500 Internal Server Error

**Problem:** Server crashed

**Solution:**
- Check Flask terminal for error messages
- Verify environment variables are set (`.env` file)
- Check service account credentials exist

---

## Testing Workflow

### Full Test Sequence

1. **Start Flask:**
   ```bash
   python run.py
   ```

2. **Initialize a Course:**
   - Use "Initialize Course" endpoint
   - Wait for completion (2-5 minutes)
   - Note the `corpus_id` from response

3. **Test Chat:**
   - Use "Chat with TA Bot" endpoint
   - Use the same `course_id` from step 2

4. **Get Graph:**
   - Use "Get Knowledge Graph" endpoint
   - Verify nodes/edges/data are returned

---

## Advanced: Using Variables in Requests

Instead of hardcoding values, use Postman variables:

**In URL:**
```
{{base_url}}/api/initialize-course
```

**In Request Body:**
```json
{
    "course_id": "{{course_id}}",
    "topics": "Machine Learning,Deep Learning"
}
```

**Set variables:**
1. Collection → Variables tab
2. Add `course_id` variable
3. Save and use `{{course_id}}` in requests

---

## Troubleshooting

### Enable Postman Console

See detailed request/response logs:
1. View → Show Postman Console (or Ctrl+Alt+C)
2. Send requests and see full details

### Check Flask Logs

Watch the terminal where `python run.py` is running for detailed error messages.

### Verify Environment

Make sure your `.env` file has:
```bash
CANVAS_API_TOKEN=your_token
GOOGLE_CLOUD_PROJECT=your_project
GOOGLE_APPLICATION_CREDENTIALS=service-account.json
```

---

## Example Test Data

### Sample Topics (comma-separated)

```
Machine Learning,Neural Networks,Deep Learning,Computer Vision,Natural Language Processing
```

### Sample Course IDs

Use your actual Canvas course ID from:
- Canvas course URL: `https://canvas.../courses/12345`
- Or from `.env`: `CANVAS_TEST_COURSE_ID`

---

## Next Steps

After testing with Postman:
1. ✅ Verify all endpoints work
2. ✅ Test error handling (invalid course_id, missing fields)
3. ✅ Check Firestore for created documents
4. ✅ Build frontend to call these endpoints
5. ✅ Deploy to production environment

---

## Quick Reference

| Endpoint | Method | Body | Response |
|----------|--------|------|----------|
| `/api/initialize-course` | POST | `{course_id, topics}` | `{status, corpus_id, files_count}` |
| `/api/chat` | POST | `{course_id, query}` | `{answer, sources}` |
| `/api/get-graph` | GET | Query: `course_id` | `{nodes, edges, data}` |
| `/launch` | POST | Form: `context_id, roles` | HTML page |
