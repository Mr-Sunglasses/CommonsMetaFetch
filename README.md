# CommonsMetaFetch

This application is a FastAPI-based web service that allows users to upload CSV or TSV files containing file names or URLs, fetch metadata for these files from Wikimedia Commons, and download a processed TSV file with the selected metadata fields.

## Features

- Upload CSV or TSV files
- Select specific metadata fields to include in the output
- Process files and fetch metadata from Wikimedia Commons
- Download processed metadata as a TSV file
- Dockerized for easy deployment

## Prerequisites

- Docker

## Quick Start

1. Clone this repository:
   ```
   git clone https://github.com/Mr-Sunglasses/CommonsMetaFetch.git
   cd CommonsMetaFetch
   ```

2. Build and run the Docker container:
   ```
   docker build -t CommonsMetaFetch .
   docker run -p 8000:8000 CommonsMetaFetch.git
   ```

3. Open your web browser and navigate to `http://localhost:8000`

## Usage

1. On the web interface, click "Choose File" to select your CSV or TSV file.
2. Select the metadata fields you want to include in the output.
3. Click "Process File" to upload and process your file.
4. Once processing is complete, the processed TSV file will be automatically downloaded.

## Development

### Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- Requests
- pytest (for running tests)

### Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.