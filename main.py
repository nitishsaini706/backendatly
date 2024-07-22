from fastapi import FastAPI, Depends, HTTPException, Header, Request
from typing import Optional
from scraper import Scraper
from database import Database
from notifier import Notifier
import os
import logging
from dotenv import load_dotenv
import redis

load_dotenv()
app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

logging.basicConfig(level=logging.INFO)

@app.get("/")
def hello():
    return "Server working fine"

def get_token(api_token: str = Header(..., alias="api_token")):
    expected_token = os.getenv("API_TOKEN")
    if api_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_token

@app.post("/scrape/")
async def scrape(limit: Optional[int] = None, proxy: Optional[str] = None, token: str = Depends(get_token)):
    scraper = Scraper(limit, proxy)
    products = await scraper.scrape()
    logging.info(f"Scraped {len(products)} products.")
    
    db = Database()
    updated_count = db.save_products(products)
    
    notifier = Notifier()
    notifier.notify(updated_count)
    
    return {"status": "success", "updated_count": updated_count}

@app.get("/product/{product_id}")
async def get_product(product_id: str, token: str = Depends(get_token)):
    # Check Redis cache first
    product = redis_client.get(product_id)
    if product:
        logging.info(f"Product {product_id} found in cache")
        return {"status": "success", "product": json.loads(product)}  # Deserialize JSON string

    logging.info(f"Product {product_id} not found in cache. Checking database.")
    db = Database()
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Store product in Redis cache
    redis_client.set(product_id, json.dumps(product))  # Serialize Python object to JSON string
    return {"status": "success", "product": product}
