
import os
import sys
import io
import logging
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from PIL import Image
import uvicorn

# Setup path - add parent directory to path so imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Handle both module and direct imports
try:
    from backend.config import Config
    config = Config
except ImportError:
    from config import Config
    config = Config

# Now import services with absolute imports
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService

# Load .env after path setup
load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

feature_extractor = None
cloudinary_service = None
pinecone_service = None
quantum_algorithm = None


def get_feature_extractor():
    """Initialize ResNet-50 feature extractor"""
    global feature_extractor
    if feature_extractor is None:
        from ml.unified_feature_extractor import UnifiedFeatureExtractor
        feature_extractor = UnifiedFeatureExtractor(
            feature_dim=config.FEATURE_DIMENSION,
            use_amp=True
        )
        logger.info("✅ ResNet-50 feature extractor initialized")
    return feature_extractor


def get_cloudinary_service():
    global cloudinary_service
    if cloudinary_service is None:
        cloudinary_service = CloudinaryImageService()
    return cloudinary_service


def get_pinecone_service():
    global pinecone_service
    if pinecone_service is None:
        pinecone_service = PineconeVectorService()
    return pinecone_service


def get_quantum_algorithm():
    """Initialize quantum algorithm for enhanced similarity"""
    global quantum_algorithm
    if quantum_algorithm is None and config.USE_QUANTUM_SIMILARITY:
        try:
            from ml.quantum.ae_qip_v3 import AEQIPAlgorithm
            logger.info("🔮 Initializing Quantum Algorithm (AE-QIP v3.0)...")
            quantum_algorithm = AEQIPAlgorithm(
                use_quantum_inspired=(config.QUANTUM_MODE == 'inspired'),
                n_precision_qubits=config.QUANTUM_PRECISION_QUBITS,
                enable_entanglement=config.ENABLE_QUANTUM_ENTANGLEMENT
            )
            circuit_info = quantum_algorithm.get_circuit_info()
            logger.info(f"✅ Quantum algorithm ready! {circuit_info['total_qubits']} qubits")
        except Exception as e:
            logger.warning(f"⚠️ Quantum algorithm not available: {e}")
            quantum_algorithm = None
    return quantum_algorithm


app = FastAPI(title='Quantum Image API', version='3.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]


@app.get('/')
async def root():
    """Serve frontend or API info based on environment"""
    # In production with frontend, serve index.html
    frontend_index = project_root / 'frontend' / 'dist' / 'index.html'
    if frontend_index.exists():
        return FileResponse(frontend_index)
    
    # Fallback: return API info (for dev/testing)
    quantum_info = {'enabled': False}
    if config.USE_QUANTUM_SIMILARITY:
        quantum_algo = get_quantum_algorithm()
        if quantum_algo:
            quantum_info = {
                'enabled': True,
                'mode': config.QUANTUM_MODE,
                'circuit': quantum_algo.get_circuit_info()
            }
    
    return {
        'message': 'Quantum Image API v3.0',
        'storage': 'Cloudinary',
        'vectors': 'Pinecone',
        'quantum': quantum_info,
        'features': ['rate-limiting', 'quantum-enhanced', 'batch-upload'],
        'database_size': get_pinecone_service().get_statistics()['total_vector_count']
    }


@app.get('/api/info')
async def api_info():
    """API information endpoint"""
    quantum_info = {'enabled': False}
    if config.USE_QUANTUM_SIMILARITY:
        quantum_algo = get_quantum_algorithm()
        if quantum_algo:
            quantum_info = {
                'enabled': True,
                'mode': config.QUANTUM_MODE,
                'circuit': quantum_algo.get_circuit_info()
            }
    
    return {
        'message': 'Quantum Image API v3.0',
        'storage': 'Cloudinary',
        'vectors': 'Pinecone',
        'quantum': quantum_info,
        'features': ['rate-limiting', 'quantum-enhanced', 'batch-upload'],
        'database_size': get_pinecone_service().get_statistics()['total_vector_count']
    }


@app.post('/api/upload')
@limiter.limit("20/minute")
async def upload_image(request: Request, file: UploadFile = File(...)):
    try:
        start_time = time.time()
        contents = await file.read()

        # Extract features
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        features = get_feature_extractor().extract_features(image)

        # Search similar images
        matches = get_pinecone_service().search(
            features,
            top_k=10,
            min_score=config.GOOD_CONFIDENCE_THRESHOLD
        )

        results = [{
            'id': m['id'],
            'filename': m['metadata'].get('filename'),
            'category': m['metadata'].get('category'),
            'similarity': m['score'],
            'image_url': m['metadata'].get('cloudinary_url')
        } for m in matches]

        elapsed = time.time() - start_time

        return {
            'success': True,
            'similar_images': results,
            'processing_time': f"{elapsed:.3f}s"
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(500, str(e))


@app.post('/api/upload-and-store')
@limiter.limit("10/minute")
async def upload_and_store(
    request: Request,
    file: UploadFile = File(...),
    category: str = 'healthcare'
):
    try:
        start_time = time.time()
        contents = await file.read()

        # Extract features
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        features = get_feature_extractor().extract_features(image)

        # Upload to Cloudinary
        filename = file.filename or 'untitled.jpg'
        result = get_cloudinary_service().upload_image(
            contents,
            filename,
            category
        )

        # Store in Pinecone
        vector_id = result['public_id'].replace('/', '_')
        metadata = {
            'filename': file.filename,
            'category': category,
            'cloudinary_url': result['secure_url'],
            'uploaded_at': datetime.utcnow().isoformat()
        }
        get_pinecone_service().upsert_vector(vector_id, features, metadata)

        # Search similar
        matches = get_pinecone_service().search(
            features,
            top_k=10,
            category_filter=category,
            min_score=config.GOOD_CONFIDENCE_THRESHOLD
        )

        results = [{
            'id': m['id'],
            'filename': m['metadata'].get('filename'),
            'similarity': m['score'],
            'image_url': m['metadata'].get('cloudinary_url')
        } for m in matches if m['id'] != vector_id]

        elapsed = time.time() - start_time

        return {
            'success': True,
            'uploaded_image': {
                'filename': file.filename,
                'cloudinary_url': result['secure_url']
            },
            'similar_images': results,
            'processing_time': f"{elapsed:.3f}s"
        }
    except Exception as e:
        logger.error(f"Upload and store error: {e}")
        raise HTTPException(500, str(e))


@app.get('/api/stats')
async def get_stats():
    stats = get_pinecone_service().get_statistics()
    return {
        'success': True,
        'statistics': stats
    }


@app.post('/api/search-quantum')
@limiter.limit("30/minute")
async def search_images_quantum(request: Request, file: UploadFile = File(...)):
    """Quantum-enhanced image search with re-ranking"""
    try:
        start_time = time.time()
        contents = await file.read()
        
        # Extract features
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        features = get_feature_extractor().extract_features(image)
        
        # Get candidates from Pinecone (classical search)
        candidates = get_pinecone_service().search(
            features,
            top_k=50,  # Get more candidates for quantum re-ranking
            min_score=0.70  # Lower threshold for candidates
        )
        
        # Apply quantum re-ranking if enabled
        quantum_algo = get_quantum_algorithm()
        if quantum_algo and len(candidates) > 0:
            logger.info(f"⚛️ Applying quantum re-ranking to {len(candidates)} candidates")
            
            for candidate in candidates:
                # Get candidate features (vector values from Pinecone)
                candidate_features = candidate.get('values')
                
                if candidate_features and len(candidate_features) > 0:
                    # Calculate quantum-enhanced similarity
                    quantum_sim = quantum_algo.calculate_similarity(
                        features,
                        candidate_features
                    )
                    candidate['quantum_score'] = float(quantum_sim)
                    candidate['classical_score'] = float(candidate['score'])
                    candidate['similarity_boost'] = float(quantum_sim - candidate['score'])
                else:
                    # Fallback to classical score if no vector values
                    logger.warning(f"⚠️ No vector values for {candidate['id']}, using classical score")
                    candidate['quantum_score'] = candidate['score']
                    candidate['classical_score'] = candidate['score']
                    candidate['similarity_boost'] = 0.0
            
            # Sort by quantum score
            candidates.sort(key=lambda x: x['quantum_score'], reverse=True)
            search_method = 'quantum-enhanced'
        else:
            # Fallback to classical
            for candidate in candidates:
                candidate['quantum_score'] = candidate['score']
                candidate['classical_score'] = candidate['score']
                candidate['similarity_boost'] = 0.0
            search_method = 'classical'
        
        # Format results
        results = [{
            'id': m['id'],
            'filename': m['metadata'].get('filename'),
            'category': m['metadata'].get('category'),
            'similarity': m['quantum_score'],
            'classical_similarity': m['classical_score'],
            'quantum_boost': m['similarity_boost'],
            'image_url': m['metadata'].get('cloudinary_url')
        } for m in candidates[:10]]
        
        elapsed = time.time() - start_time
        
        return {
            'success': True,
            'method': search_method,
            'similar_images': results,
            'processing_time': f"{elapsed:.3f}s",
            'quantum_enabled': quantum_algo is not None,
            'candidates_evaluated': len(candidates)
        }
    except Exception as e:
        logger.error(f"Quantum search error: {e}")
        raise HTTPException(500, str(e))


@app.post('/api/search-quantum-detailed')
@limiter.limit("10/minute")
async def search_quantum_detailed(request: Request, file: UploadFile = File(...)):
    """Quantum search with full breakdown for demos and analysis"""
    try:
        start_time = time.time()
        contents = await file.read()
        
        # Extract features
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        features = get_feature_extractor().extract_features(image)
        
        # Get candidates
        candidates = get_pinecone_service().search(
            features,
            top_k=20,
            min_score=0.70
        )
        
        quantum_algo = get_quantum_algorithm()
        if not quantum_algo:
            raise HTTPException(400, "Quantum algorithm not enabled")
        
        detailed_results = []
        for candidate in candidates:
            # Get full quantum breakdown
            breakdown = quantum_algo.calculate_similarity_with_breakdown(
                features,
                candidate.get('values', candidate.get('metadata', {}).get('features', features))
            )
            
            detailed_results.append({
                'image_url': candidate['metadata'].get('cloudinary_url'),
                'filename': candidate['metadata'].get('filename'),
                'category': candidate['metadata'].get('category'),
                'metrics': {
                    'overall_similarity': float(breakdown['similarity']),
                    'classical_cosine': float(breakdown['classical']),
                    'quantum_fidelity': float(breakdown['quantum_fidelity']),
                    'phase_coherence': float(breakdown['phase_coherence']),
                    'amplitude_estimated': float(breakdown['amplitude_estimated']),
                    'combined': float(breakdown['combined'])
                },
                'quantum_advantage': float(breakdown['similarity'] - breakdown['classical'])
            })
        
        # Sort by overall similarity
        detailed_results.sort(key=lambda x: x['metrics']['overall_similarity'], reverse=True)
        
        elapsed = time.time() - start_time
        
        return {
            'success': True,
            'method': 'quantum-detailed',
            'results': detailed_results[:10],
            'circuit_info': quantum_algo.get_circuit_info(),
            'processing_time': f"{elapsed:.3f}s",
            'total_candidates': len(candidates)
        }
    except Exception as e:
        logger.error(f"Quantum detailed search error: {e}")
        raise HTTPException(500, str(e))


@app.get('/health')
async def health():
    return {'status': 'healthy'}


@app.get('/api/health')
async def api_health():
    """Health check endpoint for frontend"""
    return {
        'status': 'healthy',
        'feature_extractor': 'ResNet-50',
        'retrieval_system': 'Pinecone',
        'storage': 'Cloudinary',
        'vectors': 'Quantum-Enhanced'
    }


@app.get('/api/categories')
async def get_categories():
    """Get available image categories"""
    return {
        'success': True,
        'categories': config.CATEGORIES
    }


@app.post('/api/search')
@limiter.limit("30/minute")
async def search_by_features(request: Request, features: list):
    """Search images by feature vector"""
    try:
        matches = get_pinecone_service().search(
            features,
            top_k=10,
            min_score=config.GOOD_CONFIDENCE_THRESHOLD
        )
        
        results = [{
            'id': m['id'],
            'filename': m['metadata'].get('filename'),
            'category': m['metadata'].get('category'),
            'similarity': m['score'],
            'image_url': m['metadata'].get('cloudinary_url')
        } for m in matches]
        
        return {
            'success': True,
            'similar_images': results
        }
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(500, str(e))


@app.get('/api/image/{image_id}')
async def get_image(image_id: str):
    """Get image by ID (returns Cloudinary URL)"""
    try:
        # Query Pinecone for image metadata
        result = get_pinecone_service().index.fetch([image_id])
        
        if image_id in result['vectors']:
            metadata = result['vectors'][image_id]['metadata']
            return {
                'success': True,
                'image_url': metadata.get('cloudinary_url'),
                'filename': metadata.get('filename'),
                'category': metadata.get('category')
            }
        else:
            raise HTTPException(404, "Image not found")
    except Exception as e:
        logger.error(f"Get image error: {e}")
        raise HTTPException(500, str(e))


# Serve frontend static files in production
frontend_dist = project_root / 'frontend' / 'dist'
if frontend_dist.exists():
    # Serve static assets (JS, CSS, images)
    app.mount('/assets', StaticFiles(directory=frontend_dist / 'assets'), name='assets')
    
    # Serve index.html for all non-API routes (SPA fallback)
    @app.get('/{full_path:path}')
    async def serve_spa(full_path: str):
        # Don't serve index.html for API routes
        if full_path.startswith('api/'):
            raise HTTPException(404, 'Not found')
        index_file = frontend_dist / 'index.html'
        if index_file.exists():
            return FileResponse(index_file)
        raise HTTPException(404, 'Frontend not found')
    
    logger.info(f'✅ Frontend served from {frontend_dist}')
else:
    logger.warning(f'⚠️ Frontend dist not found at {frontend_dist}')


if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT)
