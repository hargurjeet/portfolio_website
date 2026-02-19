"""Unit test for document loader"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.core.document_loader import load_and_chunk_resume

def test_document_loader():
    print("Testing Document Loader Module")
    print("=" * 60)
    
    # Test file path
    resume_path = "chatbot/data/resume.pdf"
    
    # Check if file exists
    if not os.path.exists(resume_path):
        print(f"❌ Resume file not found at: {resume_path}")
        print(f"Please place your resume.pdf in the chatbot/data/ folder")
        return False
    
    try:
        # Load and chunk the document
        chunks = load_and_chunk_resume(resume_path)
        
        print(f"✓ PDF loaded successfully")
        print(f"✓ Total chunks created: {len(chunks)}")
        print(f"\nFirst chunk preview:")
        print("-" * 60)
        print(chunks[0].page_content[:300] + "...")
        print("-" * 60)
        print(f"\nChunk metadata: {chunks[0].metadata}")
        print("=" * 60)
        print("✓ Document loader test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_document_loader()
