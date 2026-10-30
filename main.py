import uvicorn
import logging

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        level=logging.INFO,
        datefmt='%H-%M'
    )
    uvicorn.run(
        "app.presentation.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )