## To run program locally

```
git clone https://github.com/nitishsaini706/backendatly
cd backendatly

pip install -r requirements.txt
uvicorn main:app --reload
```

open http://127.0.0.1:8000
server working fine tells server is up and run 

1. /scrape as post api with ?limit, proxy for setting 
this will get products and store in product.json file locally and will store it in cache

2. /products/{id}
   to get specific product and this will return data from cache if present else get from db
