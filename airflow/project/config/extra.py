import os


# --------------------- SERVICES URL ---------------------
NATIONAL_BANK_KZ_BASE_URL = os.environ.get('NATIONAL_BANK_KZ_BASE_URL', 'https://www.nationalbank.kz/')
PROVIDER_A_BASE_URL = os.environ.get('PROVIDER_A_BASE_URL', 'http://provider_a:8000/')
PROVIDER_B_BASE_URL = os.environ.get('PROVIDER_B_BASE_URL', 'http://provider_b:8000/')

# --------------------- PROVIDERS FLIGHTS URL -------------
# For the future, it will be possible to save providers in the database
PROVIDERS_FLIGHTS_URL = [
    PROVIDER_A_BASE_URL + 'search/',
    PROVIDER_B_BASE_URL + 'search/',
]

# --------------------- REDIS -----------------------------
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB = os.environ.get('REDIS_DB', '0')
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# --------------------- REDIS KEYS ------------------------
CURRENT_EXCHANGE_RATE_REDIS_KEY = 'CURRENT_EXCHANGE_RATE'
