"""
Firestore Service
Handles all Cloud Firestore operations for course data persistence.
"""
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False
    firestore = None


# Initialize Firestore client (only if available)
if FIRESTORE_AVAILABLE:
    try:
        db = firestore.Client()
    except Exception:
        # If Firestore client initialization fails, set to None
        db = None
        FIRESTORE_AVAILABLE = False
else:
    db = None

COURSES_COLLECTION = 'courses'


def get_course_state(course_id: str) -> str:
    """
    Returns the current state of the course.
    
    Args:
        course_id: The Canvas course ID (context_id)
        
    Returns:
        One of: 'NEEDS_INIT', 'NOT_READY', 'GENERATING', 'ACTIVE'
    """
    if not FIRESTORE_AVAILABLE or db is None:
        # Fallback for testing without Firestore
        return 'NEEDS_INIT'
    
    try:
        doc = db.collection(COURSES_COLLECTION).document(course_id).get()
        
        if not doc.exists:
            # TODO: Determine if user is professor or student
            # For now, return NEEDS_INIT
            return 'NEEDS_INIT'
        
        status = doc.get('status')
        if status == 'GENERATING':
            return 'GENERATING'
        elif status == 'ACTIVE':
            return 'ACTIVE'
        else:
            return 'NOT_READY'
    except Exception:
        # If Firestore query fails, return NEEDS_INIT
        return 'NEEDS_INIT'


def create_course_doc(course_id: str):
    """
    Creates the initial course document with GENERATING status.
    
    Args:
        course_id: The Canvas course ID
    """
    if not FIRESTORE_AVAILABLE or db is None:
        # No-op for testing without Firestore
        return
    
    try:
        db.collection(COURSES_COLLECTION).document(course_id).set({
            'status': 'GENERATING'
        })
    except Exception:
        pass  # Silently fail in test mode


def get_course_data(course_id: str):
    """
    Fetches the complete course document.
    
    Args:
        course_id: The Canvas course ID
        
    Returns:
        DocumentSnapshot containing all course data
    """
    if not FIRESTORE_AVAILABLE or db is None:
        # Return None for testing without Firestore
        return None
    
    try:
        return db.collection(COURSES_COLLECTION).document(course_id).get()
    except Exception:
        return None


def finalize_course_doc(course_id: str, data: dict):
    """
    Updates the course document with all RAG/KG data and sets status to ACTIVE.
    
    Args:
        course_id: The Canvas course ID
        data: Dictionary containing corpus_id, indexed_files, kg_nodes, kg_edges, kg_data
    """
    if not FIRESTORE_AVAILABLE or db is None:
        # No-op for testing without Firestore
        return
    
    try:
        db.collection(COURSES_COLLECTION).document(course_id).update({
            'status': 'ACTIVE',
            'corpus_id': data.get('corpus_id'),
            'indexed_files': data.get('indexed_files'),
            'kg_nodes': data.get('kg_nodes'),
            'kg_edges': data.get('kg_edges'),
            'kg_data': data.get('kg_data')
        })
    except Exception:
        pass  # Silently fail in test mode
