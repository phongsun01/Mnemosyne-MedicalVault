from fastapi import FastAPI, BackgroundTasks
import os
import asyncio
import logging
from watcher import start_watcher
from parser import get_file_content
from ai_engine import extract_metadata
from notifier import send_telegram_review
from storage import save_to_markdown, index_in_chroma

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MedicalVault")

app = FastAPI(title="MedicalVault AI API")

@app.on_event("startup")
async def startup_event():
    raw_path = "/vault/raw/new"
    # Ensure folder exists
    os.makedirs(raw_path, exist_ok=True)
    # Start file watcher in a separate thread/loop
    start_watcher(raw_path, process_new_file_sync)

def process_new_file_sync(file_path):
    # Watchdog callback is sync, we bridge to async
    asyncio.run_coroutine_threadsafe(process_file(file_path), asyncio.get_event_loop())

async def process_file(file_path):
    logger.info(f"🔥 Processing file: {file_path}")
    try:
        # 1. Parse content
        content_text, images = get_file_content(file_path)
        
        # 2. AI Extraction
        metadata = await extract_metadata(file_path, content_text, images)
        if not metadata:
            logger.error(f"Failed to extract metadata for {file_path}")
            return

        # 3. Human-in-the-loop Notification
        approved = await send_telegram_review(metadata, os.path.basename(file_path))
        
        if approved:
            # 4. Save to Wiki (MD)
            md_path = save_to_markdown(metadata, file_path)
            
            # 5. Index for Search
            index_in_chroma(metadata, md_path)
            
            # 6. Archive raw file
            archive_path = file_path.replace("/raw/new/", "/raw/classified/")
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            os.rename(file_path, archive_path)
            logger.info(f"✅ Successfully processed and archived: {file_path}")

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")

@app.get("/")
def read_root():
    return {"status": "AI Brain Pipeline is Active", "version": "2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
