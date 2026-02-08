# IFC Graph Viewer - Server Setup

## Local Testing

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
If you don't have python in your path, you can try one of the following: 
```bash
python -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```



### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Open in Browser

Navigate to `http://localhost:5000` in your web browser.

## Usage

1. Click "Choose File" and select your IFC 4x3 file
2. Click "Generate Graph" button
3. Wait for processing (may take a minute for large files)
4. The graph will automatically load and display

## Server Deployment

For production deployment, consider using:
- **Gunicorn** (recommended for production):
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 app:app
  ```

## Notes

- The server accepts IFC files up to 1GB
- Processing timeout is set to 5 minutes
- Generated GraphML files are saved to `data/facility.graphml`
- Temporary uploaded files are automatically cleaned up
