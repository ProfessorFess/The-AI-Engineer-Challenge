def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status": "minimal_python_working", "message": "Basic Python function works"}'
    }
