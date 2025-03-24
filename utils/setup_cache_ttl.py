from google.cloud import firestore
from google.cloud import firestore_admin_v1
from google.cloud.firestore_admin_v1.types import index

def setup_cache_ttl():
    """
    Set up TTL policy for document cache collection.
    This needs to be run once to configure the TTL policy.
    """
    db = firestore.Client()
    admin_client = firestore_admin_v1.FirestoreAdminClient()
    
    # Create TTL index on the expiration field
    idx = index.Index()
    idx.query_scope = index.Index.QueryScope.COLLECTION
    field = index.Index.IndexField()
    field.field_path = "expiration"
    field.order = index.Index.IndexField.Order.ASCENDING
    idx.fields.append(field)
    
    # Create the index
    parent = f"projects/{db.project}/databases/(default)/collectionGroups/document_cache"
    
    try:
        operation = admin_client.create_index(
            request={
                "parent": parent,
                "index": idx
            }
        )
        print(f"Created TTL index: {operation.name}")
        
        # Wait for the operation to complete
        result = operation.result()
        print("TTL index creation completed successfully")
        print(f"Index details: {result}")
        
    except Exception as e:
        print(f"Error creating TTL index: {e}")

if __name__ == "__main__":
    setup_cache_ttl() 