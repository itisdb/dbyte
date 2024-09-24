## How to Run

1. Run the preinstaller.py using the command : `pip3 install -r requirements.txt` (Use pip3 for Unix systems and pip for Windows)
2. For Unix based systems run the command : `./run.sh` and for Windows run the command: `uvicorn app.api:app --reload`
3. Open the host on the browser and then add `/docs` to the suffix and enjoy the APIs.
4. Requirements for the code to run:
   * Tesseract
     * Mac : `brew install tesseract`
     * Windows : just Google man, you are a dev.
