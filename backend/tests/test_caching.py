import json
from backend.app import create_app
from backend.app.extensions import db
from backend.app import extensions
from backend.app.models.profile import CachedProfile

def test_double_caching():
    app = create_app()
    client = app.test_client()
    
    with app.app_context():
        # 1. Clear database cache to force miss
        try:
            db.session.query(CachedProfile).delete()
            db.session.commit()
            print("Successfully cleared database cache.")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to clear database cache: {e}")
            
        # 2. Clear Redis cache
        # Access extensions.redis_client to ensure we get the initialized reference
        if extensions.redis_client:
            try:
                extensions.redis_client.delete("profile:response:octocat")
                print("Successfully cleared Redis cache for octocat.")
            except Exception as e:
                print(f"Failed to clear Redis cache: {e}")
        else:
            print("Redis client is not initialized.")
            
        # 3. Call 1: Cache Miss (Must fetch from GitHub)
        print("\n=== Request 1: Cache Miss ===")
        resp1 = client.get('/api/profile/octocat')
        assert resp1.status_code == 200, f"Request failed: {resp1.data}"
        data1 = json.loads(resp1.data.decode('utf-8'))
        print(f"Status: {data1.get('status')}")
        print(f"Source: {data1.get('source')}")
        print(f"Cached Label: {data1.get('cached')}")
        
        assert data1.get('source') == 'github_api'
        assert data1.get('cached') is False
        
        # 4. Call 2: Cache Hit
        print("\n=== Request 2: Cache Hit ===")
        resp2 = client.get('/api/profile/octocat')
        assert resp2.status_code == 200, f"Request failed: {resp2.data}"
        data2 = json.loads(resp2.data.decode('utf-8'))
        print(f"Status: {data2.get('status')}")
        print(f"Source: {data2.get('source')}")
        print(f"Cached Label: {data2.get('cached')}")
        
        if extensions.redis_client:
            # Should hit Redis
            assert data2.get('source') == 'redis_cache'
            assert data2.get('cached') is True
        else:
            # Should fallback to SQLite
            assert data2.get('source') == 'database_cache'
            assert data2.get('cached') is True
            
        print("\nDouble-caching verification successful!")

if __name__ == "__main__":
    test_double_caching()
