"""
Main entry point for CV reformatter
"""
import os
import time
from pathlib import Path
from docx import Document

def process_documents():
    print("CV Reformatter Service Starting")
    print("-" * 40)
    print("Environment:")
    print(f"- PYTHONPATH: {os.getenv('PYTHONPATH')}")
    print(f"- Azure OpenAI Endpoint configured: {'AZURE_OPENAI_ENDPOINT' in os.environ}")
    print(f"- Azure OpenAI API Key configured: {'AZURE_OPENAI_API_KEY' in os.environ}")
    print("-" * 40)
    
    # Watch for documents in the input directory
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create directories if they don't exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    print(f"\nWatching for documents in: {input_dir}")
    print(f"Processed documents will be saved to: {output_dir}")
    print("\nService is running. Place .docx files in the input directory to process them.")
    
    try:
        while True:
            # Check for new documents
            for doc_path in input_dir.glob("*.docx"):
                try:
                    print(f"\nProcessing document: {doc_path.name}")
                    doc = Document(doc_path)
                    
                    # TODO: Add your document processing logic here
                    
                    # Save to output directory
                    output_path = output_dir / f"processed_{doc_path.name}"
                    doc.save(output_path)
                    print(f"Saved processed document to: {output_path}")
                    
                    # Move or delete original
                    doc_path.unlink()
                    
                except Exception as e:
                    print(f"Error processing {doc_path.name}: {str(e)}")
            
            # Wait before next check
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    process_documents()
