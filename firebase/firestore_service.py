import uuid
from firebase.firebase_config import get_db
from datetime import datetime

class FirestoreService:
    def __init__(self):
        self.db = get_db()
        
    def save_document_metadata(self, user_uid, doc_id, metadata):
        """Saves metadata of an uploaded and processed document."""
        if not self.db: return False
        
        doc_ref = self.db.collection('users').document(user_uid).collection('documents').document(doc_id)
        metadata['updated_at'] = datetime.now().isoformat()
        if 'created_at' not in metadata:
            metadata['created_at'] = datetime.now().isoformat()
            
        doc_ref.set(metadata, merge=True)
        return True
        
    def get_user_documents(self, user_uid):
        """Retrieves all documents for a user."""
        if not self.db: return []
        
        docs_ref = self.db.collection('users').document(user_uid).collection('documents').order_by('created_at', direction='DESCENDING')
        docs = docs_ref.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
        
    def get_document(self, user_uid, doc_id):
        """Retrieves a specific document."""
        if not self.db: return None
        
        doc_ref = self.db.collection('users').document(user_uid).collection('documents').document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None

    def save_chat_message(self, user_uid, doc_id, message_data):
        """Saves chat history for a document."""
        if not self.db: return False
        
        chat_ref = self.db.collection('users').document(user_uid).collection('documents').document(doc_id).collection('chat_history').document()
        message_data['timestamp'] = datetime.now().isoformat()
        chat_ref.set(message_data)
        return True

    def get_chat_history(self, user_uid, doc_id):
        """Gets chat history for a document."""
        if not self.db: return []
        
        chats_ref = self.db.collection('users').document(user_uid).collection('documents').document(doc_id).collection('chat_history').order_by('timestamp')
        chats = chats_ref.stream()
        return [chat.to_dict() for chat in chats]
        
    def update_analytics(self, user_uid, metrics):
        """Updates user analytics (e.g., total docs processed)."""
        if not self.db: return False
        
        analytics_ref = self.db.collection('users').document(user_uid).collection('analytics').document('summary')
        
        # Merge metrics
        doc = analytics_ref.get()
        if doc.exists:
            current = doc.to_dict()
            for k, v in metrics.items():
                if isinstance(v, (int, float)):
                    current[k] = current.get(k, 0) + v
            analytics_ref.set(current, merge=True)
        else:
            analytics_ref.set(metrics)
        return True
        
    def get_analytics(self, user_uid):
        if not self.db: return {}
        doc = self.db.collection('users').document(user_uid).collection('analytics').document('summary').get()
        if doc.exists:
            return doc.to_dict()
        return {}
