from fastapi import FastAPI
app = FastAPI()

@app.get("/api/users")
def get_users():
    return {"service": "user-service", "data": ["Alice", "Bob", "Charlie"]}

@app.get("/api/payments")
def get_payments():
    return {"service": "payment-service", "data": ["$10.00", "$25.50", "$100.00"]}
