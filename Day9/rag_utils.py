import pandas as pd
import chromadb
from chromadb.config import Settings
from typing import Dict, List, Any, Optional
import json
import logging
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from agent import MultiAgentSystem
from config import CHROMA_DB_PATH, COLLECTION_NAME


class RAGSystem:
    """RAG System for Student Placement Readiness Analysis"""

    def __init__(self, persist_directory: str = CHROMA_DB_PATH):
        self.persist_directory = persist_directory
        self.collection_name = COLLECTION_NAME

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        # Initialize multi-agent system
        self.agent_system = MultiAgentSystem()

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize or get collection
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize or get the ChromaDB collection"""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.logger.info(
                f"Loaded existing collection: {self.collection_name}")
        except Exception as e:
            # Create new collection if it doesn't exist
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.logger.info(f"Created new collection: {self.collection_name}")

    def load_dataframe_data(self, df: pd.DataFrame) -> bool:
        """Load student data from DataFrame into ChromaDB"""
        try:
            # Clear existing data
            self.clear_database()

            documents = []
            metadatas = []
            ids = []

            for idx, row in df.iterrows():
                # Create document text
                student_text = self._create_student_document(row)

                # Create metadata
                metadata = {
                    'student_id': str(idx),
                    'name': str(row.get('name', f'Student_{idx}')),
                    'attendance': float(row.get('attendance', 0)),
                    'test_score': float(row.get('test_score', 0)),
                    'assignment_percentage': float(row.get('assignment_percentage', 0)),
                    'event_participation': str(row.get('event_participation', 'No')),
                    'softskill_score': float(row.get('softskill_score', 50)),
                    'linkedin_bio': str(row.get('linkedin_bio', 'Not provided')),
                    'resume_text': str(row.get('resume_text', 'Not provided'))
                }

                documents.append(student_text)
                metadatas.append(metadata)
                ids.append(f"student_{idx}")

            # Add to ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            self.logger.info(
                f"Successfully loaded {len(documents)} students to ChromaDB")
            return True

        except Exception as e:
            self.logger.error(f"Error loading data to ChromaDB: {e}")
            return False

    def _create_student_document(self, row: pd.Series) -> str:
        """Create a text document for a student"""
        name = row.get('name', 'Unknown')
        attendance = row.get('attendance', 0)
        test_score = row.get('test_score', 0)
        assignment_percentage = row.get('assignment_percentage', 0)
        event_participation = row.get('event_participation', 'No')
        softskill_score = row.get('softskill_score', 50)
        linkedin_bio = row.get('linkedin_bio', 'Not provided')
        resume_text = row.get('resume_text', 'Not provided')

        document = f"""
        Student Name: {name}
        Academic Performance:
        - Attendance: {attendance}%
        - Test Score: {test_score}%
        - Assignment Completion: {assignment_percentage}%
        - Event Participation: {event_participation}
        
        Soft Skills Assessment:
        - Initial Soft Skills Score: {softskill_score}%
        
        Professional Profile:
        - LinkedIn Bio: {linkedin_bio}
        - Resume Summary: {resume_text}
        
        Academic Status: {'Strong' if attendance > 80 and test_score > 75 else 'Needs Improvement'}
        Communication Skills: {'Good' if softskill_score > 70 else 'Needs Development'}
        Overall Readiness: {'High' if attendance > 80 and test_score > 75 and softskill_score > 70 else 'Moderate'}
        """

        return document.strip()

    def search_and_process_students(self, query: str, n_results: int = 10) -> List[Dict]:
        """Search for students using semantic search and process them through agents"""
        try:
            # Perform semantic search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # Process students through multi-agent system
            students = []
            if results['metadatas'] and results['metadatas'][0]:
                for metadata in results['metadatas'][0]:
                    student_data = self._metadata_to_student_data(metadata)
                    processed_student = self.agent_system.process_student(
                        student_data)
                    students.append(processed_student)

            return students

        except Exception as e:
            self.logger.error(f"Error in semantic search: {e}")
            return []

    def filter_students_by_query(self, user_query: str) -> List[Dict]:
        """Filter students based on user query using AI agent"""
        try:
            # Get all students from database
            all_results = self.collection.get()

            if not all_results['metadatas']:
                return []

            # Convert to student data format
            all_student_data = []
            for metadata in all_results['metadatas']:
                student_data = self._metadata_to_student_data(metadata)
                processed_student = self.agent_system.process_student(
                    student_data)
                all_student_data.append(processed_student)

            # Use query analysis agent to filter
            filtered_names = self.agent_system.filter_students_by_query(
                user_query, all_student_data
            )

            # Return filtered students
            filtered_students = [
                student for student in all_student_data
                if student['name'] in filtered_names
            ]

            return filtered_students

        except Exception as e:
            self.logger.error(f"Error filtering students: {e}")
            return []

    def process_all_students(self) -> List[Dict]:
        """Process all students in the database through the multi-agent system"""
        try:
            # Get all students from database
            all_results = self.collection.get()

            if not all_results['metadatas']:
                return []

            # Process each student through multi-agent system
            students = []
            for metadata in all_results['metadatas']:
                student_data = self._metadata_to_student_data(metadata)
                processed_student = self.agent_system.process_student(
                    student_data)
                students.append(processed_student)

            # Sort by overall score (descending)
            students.sort(key=lambda x: x['overall_score'], reverse=True)

            return students

        except Exception as e:
            self.logger.error(f"Error processing all students: {e}")
            return []

    def _metadata_to_student_data(self, metadata: Dict) -> Dict:
        """Convert ChromaDB metadata to student data format"""
        return {
            'name': metadata.get('name', 'Unknown'),
            'attendance': metadata.get('attendance', 0),
            'test_score': metadata.get('test_score', 0),
            'assignment_percentage': metadata.get('assignment_percentage', 0),
            'event_participation': metadata.get('event_participation', 'No'),
            'softskill_score': metadata.get('softskill_score', 50),
            'linkedin_bio': metadata.get('linkedin_bio', 'Not provided'),
            'resume_text': metadata.get('resume_text', 'Not provided')
        }

    def generate_response(self, students: List[Dict], user_query: str) -> str:
        """Generate AI response based on student data and user query"""
        try:
            # Create context from student data
            context_parts = []
            for student in students:
                context_part = f"""
                Student: {student['name']}
                - Overall Score: {student['overall_score']}%
                - Academic Score: {student['academic_score']:.1f}%
                - Communication Score: {student['communication_score']}%
                - Technical Readiness: {student['tech_readiness']}%
                - Communication Readiness: {student['comm_readiness']}%
                - Analysis: {student['analysis']}
                - Recommendations: {'; '.join(student['recommendations'])}
                """
                context_parts.append(context_part.strip())

            context = "\n\n".join(context_parts)

            # Generate response using RAG agent
            response = self.agent_system.generate_rag_response(
                context, user_query)

            return response

        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error while generating the response. Please try again."

    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the database"""
        try:
            count = self.collection.count()
            return {
                'total_students': count,
                'collection_name': self.collection_name,
                'persist_directory': self.persist_directory
            }
        except Exception as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {
                'total_students': 0,
                'collection_name': self.collection_name,
                'persist_directory': self.persist_directory
            }

    def clear_database(self):
        """Clear all data from the database"""
        try:
            # Delete the collection
            self.client.delete_collection(name=self.collection_name)

            # Recreate the collection
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )

            self.logger.info("Database cleared successfully")

        except Exception as e:
            self.logger.error(f"Error clearing database: {e}")

    def get_student_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific student by name"""
        try:
            results = self.collection.query(
                query_texts=[f"Student Name: {name}"],
                n_results=1,
                where={"name": name}
            )

            if results['metadatas'] and results['metadatas'][0]:
                metadata = results['metadatas'][0][0]
                student_data = self._metadata_to_student_data(metadata)
                return self.agent_system.process_student(student_data)

            return None

        except Exception as e:
            self.logger.error(f"Error getting student by name: {e}")
            return None

    def get_students_by_criteria(self, criteria: Dict) -> List[Dict]:
        """Get students based on specific criteria"""
        try:
            # Build where clause for ChromaDB
            where_clause = {}
            for key, value in criteria.items():
                if key in ['attendance', 'test_score', 'assignment_percentage', 'softskill_score']:
                    # For numeric fields, you might want to implement range queries
                    # ChromaDB has limited query capabilities, so we'll filter after retrieval
                    continue
                else:
                    where_clause[key] = value

            # Get all students and filter manually
            all_results = self.collection.get()

            if not all_results['metadatas']:
                return []

            filtered_students = []
            for metadata in all_results['metadatas']:
                # Check if student meets criteria
                meets_criteria = True
                for key, value in criteria.items():
                    if key in metadata:
                        if isinstance(value, dict):
                            # Handle range queries like {'$gte': 70}
                            if '$gte' in value and metadata[key] < value['$gte']:
                                meets_criteria = False
                                break
                            if '$lte' in value and metadata[key] > value['$lte']:
                                meets_criteria = False
                                break
                        else:
                            if metadata[key] != value:
                                meets_criteria = False
                                break

                if meets_criteria:
                    student_data = self._metadata_to_student_data(metadata)
                    processed_student = self.agent_system.process_student(
                        student_data)
                    filtered_students.append(processed_student)

            return filtered_students

        except Exception as e:
            self.logger.error(f"Error getting students by criteria: {e}")
            return []


class StudentDatabase:
    """Wrapper class for database operations (for backward compatibility)"""

    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system

    def get_all_students(self) -> List[Dict]:
        """Get all students from database"""
        return self.rag_system.process_all_students()

    def add_student(self, student_data: Dict) -> bool:
        """Add a single student to database"""
        try:
            df = pd.DataFrame([student_data])
            return self.rag_system.load_dataframe_data(df)
        except Exception as e:
            logging.error(f"Error adding student: {e}")
            return False

    def update_student(self, student_name: str, updated_data: Dict) -> bool:
        """Update student data (simplified implementation)"""
        # Note: ChromaDB doesn't support easy updates, so this would require
        # more complex implementation in a production system
        logging.warning("Update operation not fully implemented for ChromaDB")
        return False

    def delete_student(self, student_name: str) -> bool:
        """Delete a student (simplified implementation)"""
        # Note: ChromaDB doesn't support easy deletes by condition
        logging.warning("Delete operation not fully implemented for ChromaDB")
        return False
