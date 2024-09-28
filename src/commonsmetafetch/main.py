from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import tempfile
import json


from .utils import (
    parse_filename,
    fetch_metadata,
    filter_image_metadata,
    write_dict_list_to_tsv
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


@app.post("/process/")
async def process_file(
        file: UploadFile = File(...),
        options: str = Form(...)
):

    try:
        options_dict = json.loads(options)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid options format")


    if not file.filename.endswith(('.csv', '.tsv')):
        raise HTTPException(status_code=400, detail="Only CSV and TSV files are allowed")


    content = await file.read()


    delimiter = '\t' if file.filename.endswith('.tsv') else ','

    data = []
    reader = csv.reader(io.StringIO(content.decode('utf-8')), delimiter=delimiter)
    for row in reader:
        for entry in row:
            parsed_entry = parse_filename(entry.strip())
            metadata = fetch_metadata(parsed_entry)
            filtered_metadata = filter_image_metadata(metadata)
            data.append(filtered_metadata)

    filtered_data = []
    for item in data:
        filtered_item = {}
        if options_dict.get('description'):
            filtered_item['Description'] = item['Description']
        if options_dict.get('creation_date'):
            filtered_item['Creation Date'] = item['Creation Date']
        if options_dict.get('author'):
            filtered_item['Author'] = item['Author']
        if options_dict.get('license') or options_dict.get('license_url') or options_dict.get('usage_terms'):
            filtered_item['License Information'] = {}
            if options_dict.get('license'):
                filtered_item['License Information']['License'] = item['License Information']['License']
            if options_dict.get('license_url'):
                filtered_item['License Information']['License URL'] = item['License Information']['License URL']
            if options_dict.get('usage_terms'):
                filtered_item['License Information']['Usage Terms'] = item['License Information']['Usage Terms']
        filtered_data.append(filtered_item)


    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.tsv') as temp_file:
        write_dict_list_to_tsv(filtered_data, temp_file.name)

    return FileResponse(
        temp_file.name,
        media_type='text/tab-separated-values',
        filename='processed_metadata.tsv'
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)