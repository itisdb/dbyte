# # this was used when we were using the vercel hosting but now since the size of the files are very huge are are not doing so so this file is rendered useless.
# # Not Removing this as this might come handy in the future

# from dotenv import load_dotenv
# import os
# import uvicorn

# load_dotenv()

# PORT = int(os.getenv("PORT", 8000))
# HOST = "0.0.0.0"

# if __name__ == "__main__":
#     uvicorn.run("app.api:app", host=HOST, port=PORT, reload=True)