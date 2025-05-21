Step 1: Build and run the Docker container:
docker build -t products-service
docker run -p 5000:5000 products-service

Step 2: Test with client script:(in cmd)
python3 client/client.py

Step 3: Test manually with curl/Postman:(Build in VSC Terminal and run this below command in cmd)
curl http://localhost:5000/products
curl -X POST http://localhost:5000/products -H "Content-Type: application/json" -d '{"name":"Camera","price":450}'
