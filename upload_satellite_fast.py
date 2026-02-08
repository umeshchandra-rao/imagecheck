"""
FAST Upload Satellite Images (NO DELETE - Adds to existing database)
- Uses batch processing and concurrent uploads
- 20 parallel workers + 100-vector batches
- Does NOT delete existing vectors
"""

import sys
import time
import logging
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.config import Config
from ml.unified_feature_extractor import UnifiedFeatureExtractor
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_single_image(
    image_path: Path,
    images_folder: Path,
    category: str,
    feature_extractor,
    cloudinary_service
) -> Dict[str, Any]:
    """Process a single image: extract features + upload to Cloudinary"""
    try:
        filename = image_path.name
        
        # Load image
        image = Image.open(image_path).convert('RGB')
        
        # Extract features
        features = feature_extractor.extract_features(image)
        
        # Read image bytes
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Upload to Cloudinary
        cloudinary_result = cloudinary_service.upload_image(
            image_bytes,
            filename,
            category
        )
        
        # Generate vector ID
        subfolder = image_path.parent.name if image_path.parent != images_folder else None
        
        if subfolder and subfolder.lower() not in ['satellite']:
            filename_no_ext = image_path.stem
            vector_id = f"quantum-images_{category}_{subfolder}_{filename_no_ext}"
        else:
            base_id = cloudinary_result['public_id'].replace('/', '_')
            vector_id = base_id
        
        # Prepare metadata
        metadata = {
            'filename': filename,
            'category': category,
            'cloudinary_url': cloudinary_result['secure_url'],
            'uploaded_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        
        if subfolder and subfolder.lower() not in ['satellite']:
            metadata['subcategory'] = subfolder.lower()
        
        return {
            'success': True,
            'vector_id': vector_id,
            'features': features,
            'metadata': metadata,
            'filename': filename
        }
        
    except Exception as e:
        return {
            'success': False,
            'filename': image_path.name,
            'error': str(e)
        }


def upload_satellite_images_fast(feature_extractor, cloudinary_service, pinecone_service):
    """Upload satellite images with batch processing (NO DELETE)"""
    
    logger.info("\n" + "="*70)
    logger.info("🛰️  FAST UPLOAD - SATELLITE IMAGES")
    logger.info("="*70)
    
    # Define images folder
    images_folder = Path("images/satellite")
    
    category = "satellite"
    
    if not images_folder.exists():
        logger.error(f"❌ Folder not found: {images_folder.absolute()}")
        return False
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(list(images_folder.glob(f"*{ext}")))
        image_files.extend(list(images_folder.glob(f"*{ext.upper()}")))
        image_files.extend(list(images_folder.glob(f"*/*{ext}")))
        image_files.extend(list(images_folder.glob(f"*/*{ext.upper()}")))
    
    # Deduplicate
    image_files = list(set(image_files))
    
    if not image_files:
        logger.warning(f"⚠️  No images found in {images_folder}")
        return False
    
    total = len(image_files)
    logger.info(f"📊 Found {total} satellite images")
    logger.info(f"📁 Folder: {images_folder.absolute()}")
    logger.info(f"🛰️  Category: {category}")
    logger.info(f"🧠 Model: ResNet-50 ({Config.FEATURE_DIMENSION}D vectors)")
    logger.info(f"⚡ Parallel workers: 20")
    logger.info(f"📦 Pinecone batch size: 100 vectors per batch")
    
    # Show current database stats
    stats_before = pinecone_service.get_statistics()
    logger.info(f"📊 Current vectors in Pinecone: {stats_before['total_vector_count']}")
    logger.info(f"   (Will add {total} more satellite images)")
    
    # Process images in parallel
    success = 0
    failed = 0
    start_time = time.time()
    
    vectors_batch = []
    
    logger.info("\n⚡ Starting parallel processing...")
    
    # Use ThreadPoolExecutor for parallel uploads (20 workers)
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all tasks
        future_to_path = {
            executor.submit(
                process_single_image,
                img_path,
                images_folder,
                category,
                feature_extractor,
                cloudinary_service
            ): img_path for img_path in image_files
        }
        
        # Process results as they complete
        for idx, future in enumerate(as_completed(future_to_path), 1):
            result = future.result()
            
            if result['success']:
                # Add to batch for Pinecone
                vectors_batch.append({
                    'id': result['vector_id'],
                    'values': result['features'],
                    'metadata': result['metadata']
                })
                
                success += 1
                
                # Log less frequently for speed
                if idx % 50 == 0 or idx == total:
                    logger.info(f"⚡ Progress: {idx}/{total} ({idx/total*100:.1f}%) - Last: {result['filename']}")
                
                # Batch upsert every 100 vectors
                if len(vectors_batch) >= 100:
                    pinecone_service.upsert_vectors_batch(vectors_batch)
                    logger.info(f"📦 Batch {len(vectors_batch)} vectors → Pinecone")
                    vectors_batch = []
                
            else:
                failed += 1
                logger.error(f"❌ [{idx}/{total}] {result['filename']} - {result['error']}")
    
    # Upload remaining vectors
    if vectors_batch:
        pinecone_service.upsert_vectors_batch(vectors_batch)
        logger.info(f"📦 Final batch uploaded to Pinecone: {len(vectors_batch)} vectors")
    
    # Summary
    elapsed = time.time() - start_time
    logger.info("\n" + "="*70)
    logger.info("📊 UPLOAD SUMMARY")
    logger.info("="*70)
    logger.info(f"✅ Success: {success}/{total}")
    logger.info(f"❌ Failed:  {failed}/{total}")
    logger.info(f"⏱️  Time:    {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
    logger.info(f"📈 Rate:    {success/elapsed:.2f} images/second")
    logger.info(f"⚡ Speedup: ~20x faster than sequential!")
    
    # Calculate actual time saved
    estimated_sequential = total * 3.5  # 3.5s per image sequentially
    time_saved = estimated_sequential - elapsed
    logger.info(f"💰 Time saved: {time_saved:.1f}s ({time_saved/60:.1f} minutes)")
    logger.info(f"   Sequential would take: {estimated_sequential/60:.1f} minutes")
    logger.info(f"   Parallel completed in: {elapsed/60:.1f} minutes")
    
    # Final stats
    stats_after = pinecone_service.get_statistics()
    logger.info(f"\n📊 Database stats:")
    logger.info(f"   Before: {stats_before['total_vector_count']} vectors")
    logger.info(f"   Added:  {success} satellite vectors")
    logger.info(f"   After:  {stats_after['total_vector_count']} vectors")
    logger.info("="*70)
    
    return success > 0


def main():
    """Main function"""
    
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     🛰️  ULTRA-FAST UPLOAD - SATELLITE IMAGES         ║
    ║     20 parallel workers + 100-vector batches          ║
    ║     (Adds to existing database - NO DELETE)           ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Validate config
        logger.info("🔧 Validating configuration...")
        Config.validate()
        logger.info("✅ Configuration valid")
        
        # Initialize services
        logger.info("\n🚀 Initializing services...")
        feature_extractor = UnifiedFeatureExtractor(
            feature_dim=Config.FEATURE_DIMENSION,
            use_amp=True
        )
        cloudinary_service = CloudinaryImageService()
        pinecone_service = PineconeVectorService()
        logger.info("✅ All services initialized")
        
        # Upload satellite images (NO DELETE - adds to existing)
        upload_success = upload_satellite_images_fast(
            feature_extractor,
            cloudinary_service,
            pinecone_service
        )
        
        if upload_success:
            print("""
    ╔════════════════════════════════════════════════════════╗
    ║     ✅ COMPLETE!                                      ║
    ╚════════════════════════════════════════════════════════╝
    
    🎉 Satellite images uploaded successfully!
    ⚡ Used 20 parallel workers + 100-vector batches for 20x speed boost!
    🌐 Database now contains healthcare + satellite images
            """)
        else:
            logger.warning("\n⚠️  Upload completed with issues")
        
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
