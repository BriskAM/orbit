import os
from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the server on port 5000 by default (in debug mode for local development)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
