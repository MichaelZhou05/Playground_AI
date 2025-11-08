"""
Flask API Routes (ROLE 2: The "API Router")
Handles all HTTP endpoints and connects frontend to core services.
"""
from flask import request, render_template, jsonify, current_app as app
from .services import firestore_service, rag_service, kg_service, canvas_service
from collections import defaultdict

# Simple in-memory storage for testing (replace with Firestore later)
test_storage = defaultdict(dict)


@app.route('/launch', methods=['POST'])
def launch():
    """
    Main LTI entry point from Canvas.
    Determines app state and renders the appropriate UI.
    """
    # Extract LTI parameters
    context_id = request.form.get('context_id')
    roles = request.form.get('roles', '')
    
    # Determine application state
    state = firestore_service.get_course_state(context_id)
    
    # Render the single-page app with injected state
    return render_template(
        'index.html',
        course_id=context_id,
        user_roles=roles,
        app_state=state
    )


@app.route('/api/initialize-course', methods=['POST'])
def initialize_course():
    """
    Kicks off the knowledge graph pipeline (MOCK MODE for testing).
    This is a long-running request triggered by the professor.
    """
    data = request.json
    course_id = data.get('course_id', 'test-course')
    topics = data.get('topics', '')
    




    # Mock file data for testing
    mock_files = [
        {'id': '101', 'name': 'Chapter 3.pdf', 'display_name': 'Chapter 3.pdf'},
        {'id': '102', 'name': 'Lecture 5.pdf', 'display_name': 'Lecture 5.pdf'},
        {'id': '103', 'name': 'Lab Manual.pdf', 'display_name': 'Lab Manual.pdf'},
        {'id': '104', 'name': 'Assignment 1.pdf', 'display_name': 'Assignment 1.pdf'},
        {'id': '105', 'name': 'Study Guide.pdf', 'display_name': 'Study Guide.pdf'},
    ]
    
    # Use mock version (no API calls)
    nodes_json, edges_json, data_json = kg_service.build_knowledge_graph_mock(
        topics, mock_files
    )
    
    # Store in test storage
    test_storage[course_id] = {
        'status': 'ACTIVE',
        'nodes': nodes_json,
        'edges': edges_json,
        'data': data_json
    }
    
    return jsonify({"status": "complete"})


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handles student questions using the RAG-powered TA bot.
    """
    data = request.json
    course_id = data.get('course_id')
    query = data.get('query')
    
    # TODO: Implement chat logic
    # 1. Get corpus_id from Firestore
    # 2. Query RAG corpus
    # 3. Return answer with citations
    
    return jsonify({
        "answer": "This is a placeholder response.",
        "sources": []
    })


@app.route('/api/get-graph', methods=['GET'])
def get_graph():
    """
    Fetches the knowledge graph data for visualization (MOCK MODE).
    """
    course_id = request.args.get('course_id', 'test-course')
    
    # Get from test storage
    if course_id in test_storage:
        stored = test_storage[course_id]
        return jsonify({
            "nodes": stored['nodes'],
            "edges": stored['edges'],
            "data": stored['data']
        })
    
    # Return empty if not found
    return jsonify({
        "nodes": "[]",
        "edges": "[]",
        "data": "{}"
    })


@app.route('/test', methods=['GET'])
def test_page():
    """
    Test route that directly shows the ACTIVE state for UI testing.
    """
    return render_template(
        'index.html',
        course_id='test-course',
        user_roles='instructor',
        app_state='NEEDS_INIT'  # Change to 'ACTIVE' if you want to skip initialization
    )
