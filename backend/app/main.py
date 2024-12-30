from app import create_app

# entrypoint for uvicorn (see Dockerfile)
app = create_app()

if __name__ == "__main__":
    # for local development
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
