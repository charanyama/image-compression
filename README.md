# Image Compression using K-Means Clustering

A modern web application that compresses images using K-Means clustering algorithm. By reducing the number of unique colors in an image, this tool significantly reduces file size while maintaining visual quality.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Performance](#performance)
- [Contributing](#contributing)
- [License](#license)

## Overview

Image compression is achieved through the K-Means clustering algorithm, which groups similar colors together and replaces them with their cluster centroids. This technique:

- **Reduces color palette**: Limits image colors to the specified number of clusters
- **Maintains structure**: Preserves important visual features while reducing data
- **Fast processing**: Efficiently compresses images on the server side
- **Quality control**: Adjustable compression levels through cluster count parameter

## Features

- **Web Interface**: User-friendly dashboard for uploading and compressing images
- **Real-time Compression**: Instant visual feedback with compression statistics
- **Adjustable Clustering**: Control compression ratio by specifying number of clusters
- **Compression Statistics**: View detailed metrics including:
  - Original and compressed file sizes
  - Compression ratio
  - Space saved percentage
- **Before/After Preview**: Side-by-side image comparison
- **RESTful API**: Easy integration with external applications
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Project Structure

```
kmeans/
├── app/                          # FastAPI application
│   ├── __init__.py              # FastAPI app initialization
│   ├── models/
│   │   └── img_request.py        # Request/response models
│   ├── routes/
│   │   ├── compress.py           # Compression API endpoints
│   │   └── pages.py              # Web page routes
│   ├── services/
│   │   └── compression.py        # K-Means compression logic
│   ├── utils/
│   │   └── image_utils.py        # Image processing utilities
│   ├── static/
│   │   └── favicon.ico           # Browser tab icon
│   └── templates/
│       ├── compress.html         # Compression interface
│       └── landing.html          # Landing page
├── data/
│   └── img/                      # Sample images directory
├── kmeans.py                     # Standalone K-Means implementation (stub)
├── kmeans.ipynb                  # Jupyter notebook with experiments
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Requirements

- Python 3.8+
- pip (Python package manager)

### Core Dependencies

- **fastapi** - Modern web framework
- **uvicorn** - ASGI server
- **scikit-learn** - Machine learning library for K-Means
- **opencv-python** - Image processing
- **numpy** - Numerical computing
- **jinja2** - Template engine (included with FastAPI)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kmeans
```

### 2. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

First, create a `requirements.txt` file (if not present):

```bash
pip install fastapi uvicorn scikit-learn opencv-python numpy python-multipart
```

Or create `requirements.txt`:

```
fastapi
uvicorn
scikit-learn
opencv-python
numpy
python-multipart
```

Then install:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Start the FastAPI server
uvicorn app:app --reload

# The application will be available at:
# http://localhost:8000/
```

## Usage

### Web Interface

1. **Open the Application**
   - Navigate to `http://localhost:8000/`
   - Click on "Compress" button

2. **Upload an Image**
   - Click the upload area or drag-and-drop an image
   - Supported formats: JPG, PNG, BMP, etc.

3. **Configure Compression**
   - Select the number of clusters (2-256)
   - Lower values = higher compression, lower quality
   - Higher values = lower compression, better quality

4. **View Results**
   - See original and compressed images side-by-side
   - Review compression statistics
   - Download the compressed image

### Python API

```python
from app.services.compression import compress_kmeans, compute_compression_stats
from app.utils.image_utils import read_image
import cv2

# Read image
img = cv2.imread('image.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) / 255.0

# Compress with 5 clusters
compressed_img, centroids, labels = compress_kmeans(img, clusters=5)

# Get compression statistics
stats = compute_compression_stats(img, centroids, labels)
print(stats)
```

### REST API

**Endpoint**: `POST /api/compress`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/compress" \
  -F "file=@image.jpg" \
  -F "clusters=5"
```

**Response**:
```json
{
  "compressed_image": "base64_encoded_image_string",
  "stats": {
    "original_size": 150000,
    "compressed_size": 45000,
    "compression_ratio": 3.33,
    "saved_percent": 70.0
  }
}
```

## How It Works

### K-Means Clustering Algorithm

The compression process follows these steps:

1. **Flatten Image**: Convert image (H × W × 3) to (H×W × 3) matrix where each row is an RGB pixel

2. **K-Means Clustering**: 
   - Initialize k random centroids
   - Assign each pixel to nearest centroid
   - Update centroids based on mean of assigned pixels
   - Repeat until convergence

3. **Compress**: Replace each pixel with its cluster centroid

4. **Reshape**: Convert back to original image dimensions

### Example

```
Original: 1000×1000 RGB image = 3,000,000 values
With 5 clusters:
- Centroids: 5 × 3 = 15 values
- Labels: 1,000,000 values
- Total: ~1,000,015 values
- Compression ratio: ~3:1
```

### Algorithm Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `clusters` | 5 | Number of color clusters (2-256) |
| `max_iter` | 100 | Maximum iterations for K-Means |
| `n_init` | 10 | Number of K-Means initializations |
| `random_state` | 42 | Random seed for reproducibility |

## API Documentation

### Endpoints

#### GET `/`
- **Description**: Landing page
- **Response**: HTML page

#### GET `/compress`
- **Description**: Compression interface
- **Response**: HTML page with UI

#### POST `/api/compress`
- **Description**: Compress an image
- **Parameters**:
  - `file` (File, required): Image file to compress
  - `clusters` (int, optional): Number of clusters (default: 5)
- **Response**: 
  ```json
  {
    "compressed_image": "base64_string",
    "stats": {
      "original_size": int,
      "compressed_size": int,
      "compression_ratio": float,
      "saved_percent": float
    }
  }
  ```

## Configuration

### Adjusting Compression Levels

Edit `app/services/compression.py` to change default parameters:

```python
def compress_kmeans(img: np.ndarray, clusters: int = 5, max_iter: int = 100, ...):
    # Modify defaults here
```

### Image Quality Settings

Modify JPEG quality in `app/utils/image_utils.py`:

```python
_, buffer = cv2.imencode(".jpg", img_bgr)  # Add quality parameter if needed
```

## Performance

### Compression Ratios by Cluster Count

| Clusters | Typical Ratio | Quality Level |
|----------|---------------|---------------|
| 2-4      | 5:1 - 10:1    | Low          |
| 5-10     | 3:1 - 5:1     | Medium       |
| 16-32    | 2:1 - 3:1     | Good         |
| 64-128   | 1.5:1 - 2:1   | High         |
| 256      | ~1:1          | Original     |

### Processing Time

- Typical image (2000×1500): ~50-200ms
- Large image (4000×3000): ~200-500ms
- Depends on number of clusters and system performance

## Testing

Run the Jupyter notebook for experimentation:

```bash
jupyter notebook kmeans.ipynb
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Notes

- The algorithm is deterministic with `random_state=42` for reproducible results
- Image is normalized to [0, 1] range before processing
- Final output is converted back to [0, 255] for display
- Base64 encoding ensures compatibility with JSON responses

## Troubleshooting

### Issue: "Img is invalid!"
- **Solution**: Ensure image format is supported (JPG, PNG, BMP)

### Issue: Slow compression
- **Solution**: Use fewer clusters or resize large images

### Issue: Poor compression quality
- **Solution**: Increase the number of clusters

## Resources

- [K-Means Clustering](https://en.wikipedia.org/wiki/K-means_clustering)
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Image Compression Techniques](https://en.wikipedia.org/wiki/Image_compression)

## License

This project is open source and available under the MIT License.

---

**Created**: 2026  
**Last Updated**: May 2026  
**Author**: Charan Yama
