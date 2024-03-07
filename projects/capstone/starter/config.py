import os
from dotenv import load_dotenv

load_dotenv()

class Testing:
    cast_assistant_token=os.getenv("cast_assistant_token")
    cast_director_token=os.getenv("cast_director_token")
    exec_producer_token=os.getenv("exec_producer_token")


class Auth0_data:
    auth0_domain=os.getenv("auth0_domain")
    algorithms=os.getenv("algorithms")
    api_audience=os.getenv("api_audience")