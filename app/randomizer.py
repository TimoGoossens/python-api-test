from fastapi import FastAPI
from random import randint

app = FastAPI()

@app.get("/percentage")
async def get_random_percentage():
    return {'percentage': randint(0, 100)}

@app.get("/percentage/{lower_limit}/{upper_limit}")
async def get_random_percentage1(lower_limit: int, upper_limit: int):
    if(lower_limit >= upper_limit):
        return {'error': 'The upper limit must be greater than the lower limit!', 'lower limit': lower_limit, 'upper limit': upper_limit}
    return {'percentage': randint(lower_limit, upper_limit)}

@app.get("/percentage/{lower_limit}/{upper_limit}/{amount}")
async def get_random_percentage2(lower_limit: int, upper_limit: int, amount: int):
    if(lower_limit >= upper_limit):
        return {'error': 'The upper limit must be greater than the lower limit!', 'lower limit': lower_limit, 'upper limit': upper_limit}

    if (amount <= 0):
        return {'error': 'The amount must be greater than 0!', 'amount': amount}

    random_numbers = []
    for counter in range(amount):
        random_numbers.append(randint(lower_limit, upper_limit))

    return {'percentages': random_numbers}
