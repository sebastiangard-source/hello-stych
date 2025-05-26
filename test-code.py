from dotenv import load_dotenv
import os, sys
load_dotenv()
print("ID  :", os.getenv("STYTCH_PROJECT_ID"))
print("SECRET present?:", bool(os.getenv("STYTCH_SECRET")))
sys.exit()   # run this once to confirm the values show up

stytch = Client(
    project_id = os.getenv("STYTCH_PROJECT_ID"),  # should start with  project-test-
    secret     = os.getenv("STYTCH_SECRET"),      # secret-test-…=
    environment="test",                           # ← keep this “test” while you use test keys
)