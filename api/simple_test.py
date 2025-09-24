# Ultra-minimal test function for Vercel
def handler(event, context):
    """Ultra-minimal handler to test if basic Python functions work."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"status": "ultra_minimal_working", "message": "Basic Python function works"}'
    }
