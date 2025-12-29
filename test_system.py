"""
Test script to verify the RAG system
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.document_loader import DocumentLoader
from utils.chunking import TextChunker


def test_document_loading():
    """Test document loading functionality"""
    print("=" * 60)
    print("Testing Document Loading")
    print("=" * 60)
    
    try:
        loader = DocumentLoader(settings.document_path)
        documents = loader.load_all_documents()
        
        print(f"✅ Loaded {len(documents)} documents")
        
        if documents:
            stats = loader.get_document_stats(documents)
            print(f"\nDocument Statistics:")
            print(f"  Total Documents: {stats['total_documents']}")
            print(f"  Total Characters: {stats['total_characters']:,}")
            print(f"  Average Chars/Doc: {stats['average_chars_per_doc']:,}")
            print(f"  File Types: {stats['file_types']}")
            
            print(f"\nSample Document:")
            sample = documents[0]
            print(f"  Source: {sample['source']}")
            print(f"  Type: {sample['file_type']}")
            print(f"  Size: {sample['file_size']} bytes")
            print(f"  Content preview: {sample['content'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_chunking():
    """Test document chunking functionality"""
    print("\n" + "=" * 60)
    print("Testing Document Chunking")
    print("=" * 60)
    
    try:
        loader = DocumentLoader(settings.document_path)
        documents = loader.load_all_documents()
        
        if not documents:
            print("⚠️ No documents to chunk")
            return False
        
        chunker = TextChunker(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        chunks = chunker.chunk_documents(documents)
        
        print(f"✅ Created {len(chunks)} chunks from {len(documents)} documents")
        
        if chunks:
            print(f"\nChunk Statistics:")
            print(f"  Average chunks per document: {len(chunks) // len(documents)}")
            print(f"  Chunk size: {settings.chunk_size} chars")
            print(f"  Chunk overlap: {settings.chunk_overlap} chars")
            
            print(f"\nSample Chunk:")
            sample_chunk = chunks[0]
            print(f"  Source: {sample_chunk['source']}")
            print(f"  Chunk ID: {sample_chunk['chunk_id']}")
            print(f"  Index: {sample_chunk['chunk_index']} / {sample_chunk['total_chunks']}")
            print(f"  Content preview: {sample_chunk['content'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n" + "=" * 60)
    print("Testing Configuration")
    print("=" * 60)
    
    print(f"Document Path: {settings.document_path}")
    print(f"Chunk Size: {settings.chunk_size}")
    print(f"Chunk Overlap: {settings.chunk_overlap}")
    print(f"Top K Results: {settings.top_k_results}")
    print(f"Azure Configured: {settings.validate_azure_config()}")
    
    if not settings.validate_azure_config():
        print("\n⚠️ Warning: Azure configuration is incomplete")
        print("   Please update the .env file with your Azure credentials")
    else:
        print("\n✅ Azure configuration looks good")
    
    return True


def main():
    """Run all tests"""
    print("\n🧪 RAG System Test Suite\n")
    
    results = {
        "Configuration": test_configuration(),
        "Document Loading": test_document_loading(),
        "Document Chunking": test_chunking()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
