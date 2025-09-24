# Alternative approach - basic WSGI handler
def application(environ, start_response):
    """Basic WSGI application for testing."""
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]
    start_response(status, headers)
    return [b'{"status": "wsgi_working", "message": "Basic WSGI handler works"}']

# Also expose as handler for serverless
def handler(event, context):
    """Serverless handler."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"status": "serverless_working", "message": "Basic serverless handler works"}'
    }
