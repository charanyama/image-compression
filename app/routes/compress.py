from fastapi import APIRouter, File, Response, UploadFile
from app.services.compression import compress_kmeans, compute_compression_stats
from app.utils.image_utils import encode_image_base64, read_image

router = APIRouter()


@router.post("/api/compress")
async def compress(file: UploadFile = File(...), clusters: int = 5):
    file_content = await file.read()

    img = read_image(file_content)
    compressed_img, centroids, labels = compress_kmeans(img, clusters)
    stats = compute_compression_stats(img=img, centroids=centroids, labels=labels)

    return {"compressed_image": encode_image_base64(compressed_img), "stats": stats}
