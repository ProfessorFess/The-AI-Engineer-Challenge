"""Ultra-minimal Python function to test Vercel deployment"""

def handler(event, context):
    """Minimal serverless handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': '{"status": "minimal_python_working", "message": "Basic Python works on Vercel"}'
    }
