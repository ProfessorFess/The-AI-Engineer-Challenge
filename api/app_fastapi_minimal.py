# Minimal FastAPI without any complex dependencies
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="Minimal Test")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/api/test")
    async def test():
        return {"status": "fastapi_minimal_working"}
    
    # Try Mangum
    try:
        from mangum import Mangum
        handler = Mangum(app)
    except ImportError:
        # Fallback handler
        def handler(event, context):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': '{"status": "fallback_handler", "error": "mangum_not_available"}'
            }
            
except ImportError as e:
    # If FastAPI fails, use basic handler
    def handler(event, context):
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"status": "import_failed", "error": "{str(e)}"}}'
        }
