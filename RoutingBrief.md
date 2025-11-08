Backend Task Briefing: The API Router (Flask)

Welcome to the team. Your role is the central "plumber" or "glue" for the entire application. You are responsible for building the Flask web server that handles all incoming HTTP requests, from the initial Canvas LTI launch to the AJAX calls from the frontend.
You will work almost exclusively in app/routes.py.
Your job is not to write the core business logic (not to talk to Vertex AI, not to build graphs). Your job is to:
Define all API routes.
Receive and validate data from request objects (forms, JSON, query params).
Orchestrate calls to the Core Services (the Python functions built by Role 3).
Format the responses from the Core Services and send them back to the frontend as JSON or rendered HTML.
You will work in parallel with the Core Services team. You must build your routes by assuming the functions listed in the "Contract" section exist and will return the data specified.

1. Core Tasks (Your To-Do List)

Set up the Flask App (app/__init__.py, app/routes.py)
Initialize the Flask app.
Initialize the Firestore client (db = firestore.client()) and make it available to your routes.
Implement the LTI Launch Handler (POST /launch)
This is the main entry point from Canvas.
Logic:
Receive the POST request from Canvas. Do not worry about LTI OAuth signature validation for the hackathon.
Extract context_id (the course ID) and roles from request.form.
Call state = firestore_service.get_course_state(db, context_id).
Call return render_template('index.html', ...) and pass all the necessary data to the frontend: course_id, user_roles, and app_state=state.
Implement the Initialization Endpoint (POST /api/initialize-course)
This is the long-running "Go" button for professors.
Logic:
Get course_id from request.json.
Call firestore_service.create_course_doc(course_id).
Call files = canvas_service.get_course_files(course_id). (Assume you have a dev token for now).
Upload files to google cloud service
Call corpus_id = rag_service.create_and_provision_corpus(files, token=...).
Call (nodes, edges, data) = kg_service.build_knowledge_graph(topics, corpus_id, files).
Bundle all returned data (corpus_id, indexed_files_map, nodes, edges, data) into a final update_payload dictionary.
Clean up (Delete canvas files locally and in google cloud)
Call firestore_service.finalize_course_doc(db, course_id, update_payload).
Return jsonify({"status": "complete"}).
Implement the Chat Endpoint (POST /api/chat)
This is the core TA-Bot MVP.
Logic:
Get course_id and query from request.json.
Call course_doc = firestore_service.get_course_data(db, course_id).
Extract corpus_id from course_doc.
Call (answer, sources) = rag_service.query_rag_corpus(corpus_id, query).
Return jsonify({"answer": answer, "sources": sources}).
Implement the Graph Data Endpoint (GET /api/get-graph)
This feeds the Vis.js visualization.
Logic:
Get course_id from request.args.
Call course_doc = firestore_service.get_course_data(db, course_id).
Extract the (already-serialized) JSON strings from the doc:
nodes_json = course_doc.get('kg_nodes')
edges_json = course_doc.get('kg_edges')
data_json = course_doc.get('kg_data')
Return jsonify({"nodes": nodes_json, "edges": edges_json, "data": data_json}).

2. Tools & Technologies

Flask: You will live in this library. Use request, render_template, and jsonify.
Google Cloud Firestore: You will only use the db client to call functions from firestore_service.

3. Your Assumptions (The "Contract" with Core Services)

You must import the following functions from the app.services package. You can assume they exist, they work exactly as described, and they will be built by the Core Services developer. Your job is to call them.

Python


# --- From app.services.firestore_service ---
# Returns one of: 'NEEDS_INIT', 'NOT_READY', 'GENERATING', 'ACTIVE'
def get_course_state(db, course_id: str) -> str: ...

# Fetches the entire course document
def get_course_data(db, course_id: str) -> dict: ... 

# Creates the initial doc, sets status to 'GENERATING'
def create_course_doc(db, course_id: str): ...

# Updates the final doc with all data and sets status to 'ACTIVE'
def finalize_course_doc(db, course_id: str, data: dict): ...

# --- From app.services.canvas_service ---
# Returns a list of file objects and a map of their hashes/URLs
def get_course_files(course_id: str, token: str) -> (list, dict): ... 

# (For AI topic gen) Returns syllabus text
def get_syllabus(course_id: str, token: str) -> str: ... 

# --- From app.services.rag_service ---
# Creates corpus, uploads all files, returns the new corpus ID
def create_and_provision_corpus(files: list, token: str) -> str: ... 

# The chat function. Returns the final answer and a list of source names
def query_rag_corpus(corpus_id: str, query: str) -> (str, list): ... 

# --- From app.services.kg_service ---
# The big one. Builds the graph and returns the three JSON strings for the DB
def build_knowledge_graph(topic_list: list, corpus_id: str, files: list) -> (str, str, str): ...



4. Stretch Goals (Your Task)

If you complete the MVP, your job is to add the routes for the stretch goals:
Conversational Memory:
Modify POST /api/chat:
It will now receive {"history": [...]} instead of {"query": "..."}.
You will call a new Core Service function: (answer, sources) = rag_service.query_rag_with_history(corpus_id, history_list).
The response format {"answer": ..., "sources": ...} remains the same.
File Node Summaries:
Create POST /api/summarize-file:
Get course_id and file_id from request.json.
Call course_doc = firestore_service.get_course_data(db, course_id). Get corpus_id.
Call a new Core Service function: summary = rag_service.summarize_file(corpus_id, file_id).
Return jsonify({"summary": summary}).
AI-Generated Questions:
Create POST /api/get-suggested-questions:
Get topic from request.json.
Call a new Core Service function: questions = kg_service.get_suggested_questions(topic).
Return jsonify({"questions": questions}).
