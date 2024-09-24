from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from zipfile import ZipFile
from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image
import logging
from typing import List

class dbyteException(Exception):
    pass

app = FastAPI()

from app.logthis import APILogger

@app.get("/")
async def root():
    logger = APILogger()
    logger.log(logging.DEBUG, "Root endpoint accessed")

    del logger
    return {"message": "This is the root of the dbyteAPI"}

@app.get("/error")
async def get_error_example():
    logger = APILogger()
    logger.log(logging.WARNING, "Error endpoint accessed")
    raise HTTPException(status_code=404, detail="This is a 404 error example")

@app.get("/health_check")
async def health_check():
    logger = APILogger()
    logger.log(logging.INFO, "Health check endpoint accessed")
    try:
        logger.log(logging.DEBUG, "Health check running...")
        logger.log(logging.INFO, "Health check passed successfully")
        del logger
        return {"message": "dbyteAPI is up and running!"}
    except Exception as e:
        logger.log(logging.ERROR, f"Health check failed: {e}")
        del logger
        raise HTTPException(status_code=500, detail=f"dbyte is unHealthy: {str(e)}")
    
@app.post("/pdf2image")
async def pdf2image(pdffile: UploadFile = File(...)):
    logger = APILogger()
    logger.log(logging.INFO, "PDF2Image endpoint accessed")
    try:
        # Check for a specific condition to raise custom exception
        if pdffile.filename.split('.')[-1] != 'pdf':
            logger.log(logging.ERROR, "Invalid file format provided")
            raise dbyteException("Invalid file format. Only PDFs are allowed.")
        
        logger.log(logging.DEBUG, f"Processing file: {pdffile.filename}")
        
        # Convert SpooledTemporaryFile to BytesIO
        pdf_bytes = await pdffile.read()
        pdf_stream = BytesIO(pdf_bytes)
        
        # Open the PDF from the BytesIO stream
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        logger.log(logging.DEBUG, f"PDF file opened. Number of pages: {len(pdf_document)}")
        
        # Create an in-memory ZIP file
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            # Convert each page to an image (JPEG)
            for page_num in range(len(pdf_document)):
                logger.log(logging.DEBUG, f"Processing page {page_num + 1}")
                page = pdf_document[page_num]
                pix = page.get_pixmap()
                
                # Convert the page pixmap to a PIL Image
                img_byte_arr = BytesIO(pix.tobytes("jpg"))
                pil_image = Image.open(img_byte_arr)
                
                # Add metadata to the image
                metadata = {
                    "Description": "Processed by dbyteAPI"
                }
                pil_image.info.update(metadata)
                
                # Save the image to a byte stream
                img_byte_arr = BytesIO()
                pil_image.save(img_byte_arr, format="JPEG", exif=pil_image.info.get("exif", b""))
                
                # Write each image as a JPEG file inside the ZIP
                zip_file.writestr(f"page_{page_num + 1}.jpg", img_byte_arr.getvalue())

                logger.log(logging.DEBUG, f"Page {page_num + 1} converted and added to ZIP")
        
        # Seek to the beginning of the ZIP buffer
        zip_buffer.seek(0)
        
        logger.log(logging.INFO, "ZIP file created successfully. Returning response.")
        # Return the ZIP file as a streaming response
        return StreamingResponse(zip_buffer, media_type="application/zip", 
                                 headers={"Content-Disposition": "attachment; filename=pdf_images.zip"})
    except Exception as e:
        logger.log(logging.ERROR, f"PDF2Image Failed ! : {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        logger.log(logging.INFO, "PDF2Image process completed")
        del logger

@app.post("/image2pdf")
async def image2pdf(imagefiles: List[UploadFile] = File(...)):
    logger = APILogger()
    logger.log(logging.INFO, f"Image2PDF endpoint accessed with {len(imagefiles)} files")

    if len(imagefiles) == 0:
        raise HTTPException(status_code=400, detail="No files uploaded")

    try:
        images = []
        logger.log(logging.INFO, "Processing uploaded images...")

        # Open each uploaded image file
        for imagefile in imagefiles:
            logger.log(logging.INFO, f"Reading image file: {imagefile.filename}")
            image = await imagefile.read()
            img = Image.open(BytesIO(image))
            logger.log(logging.INFO, f"Image {imagefile.filename} opened successfully")

            # Convert to RGB mode if the image has an alpha channel (e.g., PNG)
            if img.mode in ("RGBA", "LA"):
                logger.log(logging.INFO, f"Converting {imagefile.filename} to RGB mode")
                img = img.convert("RGB")

            images.append(img)

        # Create an in-memory buffer for the PDF
        pdf_buffer = BytesIO()
        logger.log(logging.INFO, "Creating PDF from images...")

        # Save the images as a PDF
        if images:
            images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])

        # Move the buffer's pointer to the beginning
        pdf_buffer.seek(0)
        logger.log(logging.INFO, "PDF created successfully")

        # Return the PDF as a StreamingResponse
        logger.log(logging.INFO, "Returning PDF as a response")
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=dbyteimage2pdf.pdf"})

    except Exception as e:
        logger.log(logging.ERROR, f"Image2PDF Failed: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        logger.log(logging.INFO, "Image2PDF process completed")
        del logger

