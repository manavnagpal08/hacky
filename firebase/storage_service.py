import uuid
import os
from firebase.firebase_config import get_storage_bucket

class StorageService:
    def __init__(self):
        self.bucket = get_storage_bucket()
        
    def upload_file(self, file_bytes, destination_blob_name, content_type=None):
        """Uploads a file to the bucket."""
        if not self.bucket: return None
        
        blob = self.bucket.blob(destination_blob_name)
        
        if content_type:
            blob.upload_from_string(file_bytes, content_type=content_type)
        else:
            blob.upload_from_string(file_bytes)
            
        # Make the blob publicly viewable for easy display in Streamlit
        blob.make_public()
        return blob.public_url
        
    def upload_local_file(self, local_path, destination_blob_name):
        if not self.bucket: return None
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)
        blob.make_public()
        return blob.public_url

    def download_file(self, blob_name, destination_file_name):
        """Downloads a file from the bucket."""
        if not self.bucket: return False
        
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(destination_file_name)
        return True
        
    def delete_file(self, blob_name):
        if not self.bucket: return False
        blob = self.bucket.blob(blob_name)
        blob.delete()
        return True
