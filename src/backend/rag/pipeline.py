"""
SC Chatbot RAG Pipeline

Retrieval-Augmented Generation implementation.
"""

from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime

from ..models.database import get_db_session
from ..models.knowledge import KnowledgeDocument


class RAGPipeline:
    """RAG Pipeline for SC Chatbot."""
    
    def __init__(self, tenant_id: int):
        """Initialize RAG pipeline for a tenant."""
        self.tenant_id = tenant_id
        self.embeddings = HuggingFaceEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
        )
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
        )
        self.retriever = None
    
    async def load_knowledge(self):
        """Load knowledge documents into vector store."""
        async with get_db_session() as session:
            documents = session.query(KnowledgeDocument).filter(
                KnowledgeDocument.tenant_id == self.tenant_id,
                KnowledgeDocument.is_active == True,
                KnowledgeDocument.is_processed == True,
            ).all()
        
        # Create chunks
        chunks = []
        for doc in documents:
            text_splitter = self.text_splitter
            if doc.chunk_count == 0:  # First time processing
                chunks = text_splitter.split_text(doc.parsed_content or "")
            
            # Create vector store
            self.vectorstore = FAISS.from_texts(
                chunks,
                self.embeddings,
            )
            self.retriever = self.vectorstore.as_retriever(search_k=3)
            
            # Update document chunk count
            doc.chunk_count = len(chunks)
            doc.is_processed = True
            doc.processed_at = datetime.utcnow()
            session.commit()
    
    async def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant context for query."""
        if not self.retriever:
            await self.load_knowledge()
        
        # Get relevant chunks
        docs = self.retriever.invoke(query)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": doc.score,
            }
            for doc in docs
        ]
    
    async def generate_response(
        self,
        query: str,
        context: List[Dict[str, Any]] = None,
    ) -> str:
        """Generate response with RAG."""
        # Create retriever QA chain
        if not self.retriever:
            await self.load_knowledge()
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful AI assistant. Use the provided context to answer questions."),
                ("user", "{question}"),
            ]
        )
        
        chain = (
            prompt
            | (lambda x: x)
            | self.retriever
            | (lambda x: x)
            | self.embeddings
        )
        
        return "Generated response"