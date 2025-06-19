import chromadb
from chromadb.config import Settings
import pandas as pd
import json
import os
from typing import List, Dict, Any
from datetime import datetime


class StudentDatabase:
    def __init__(self, persist_directory="./chroma_db"):
        """Initialize ChromaDB with persistent storage"""
        self.persist_directory = persist_directory

        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="student_placement_data",
            metadata={"description": "Student placement readiness data"}
        )

    def add_students_from_csv(self, csv_file_path: str) -> bool:
        """Load student data from CSV into ChromaDB"""
        try:
            df = pd.read_csv(csv_file_path)
            return self.add_students_from_dataframe(df)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False

    def add_students_from_dataframe(self, df: pd.DataFrame) -> bool:
        """Add students from pandas DataFrame to ChromaDB"""
        try:
            documents = []
            metadatas = []
            ids = []

            for idx, row in df.iterrows():
                # Create a text document for embedding
                document_text = self._create_student_document(row)
                documents.append(document_text)

                # Store metadata
                metadata = {
                    "name": str(row.get('name', f'Student_{idx}')),
                    "attendance": float(row.get('attendance', 0)),
                    "test_score": float(row.get('test_score', 0)),
                    "assignment_percentage": float(row.get('assignment_percentage', 0)),
                    "event_participation": str(row.get('event_participation', 'No')),
                    "softskill_score": float(row.get('softskill_score', 50)),
                    "linkedin_bio": str(row.get('linkedin_bio', '')),
                    "resume_text": str(row.get('resume_text', '')),
                    "timestamp": datetime.now().isoformat()
                }
                metadatas.append(metadata)

                # Create unique ID
                student_id = f"student_{idx}_{row.get('name', 'unknown').replace(' ', '_').lower()}"
                ids.append(student_id)

            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            print(f"Successfully added {len(documents)} students to database")
            return True

        except Exception as e:
            print(f"Error adding students to database: {e}")
            return False

    def _create_student_document(self, row) -> str:
        """Create a searchable document text for each student"""
        document = f"""
        Student Name: {row.get('name', 'Unknown')}
        Academic Performance:
        - Attendance: {row.get('attendance', 0)}%
        - Test Score: {row.get('test_score', 0)}%
        - Assignment Completion: {row.get('assignment_percentage', 0)}%
        - Event Participation: {row.get('event_participation', 'No')}
        
        Soft Skills:
        - Communication Score: {row.get('softskill_score', 50)}%
        
        Professional Profile:
        LinkedIn Bio: {row.get('linkedin_bio', 'Not provided')}
        
        Resume Summary: {row.get('resume_text', 'Not provided')}
        """
        return document.strip()

    def search_students(self, query: str, n_results: int = 10) -> List[Dict]:
        """Search for students based on query"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # Combine results with metadata
            student_data = []
            for i in range(len(results['ids'][0])):
                student_info = {
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                student_data.append(student_info)

            return student_data

        except Exception as e:
            print(f"Error searching students: {e}")
            return []

    def get_all_students(self) -> List[Dict]:
        """Get all students from database"""
        try:
            results = self.collection.get()

            student_data = []
            for i in range(len(results['ids'])):
                student_info = {
                    'id': results['ids'][i],
                    'document': results['documents'][i],
                    'metadata': results['metadatas'][i]
                }
                student_data.append(student_info)

            return student_data

        except Exception as e:
            print(f"Error getting all students: {e}")
            return []

    def get_student_by_name(self, name: str) -> Dict:
        """Get specific student by name"""
        try:
            results = self.collection.get(
                where={"name": name}
            )

            if results['ids']:
                return {
                    'id': results['ids'][0],
                    'document': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
            return None

        except Exception as e:
            print(f"Error getting student by name: {e}")
            return None

    def delete_all_students(self):
        """Clear all student data"""
        try:
            # Get all IDs and delete them
            all_students = self.collection.get()
            if all_students['ids']:
                self.collection.delete(ids=all_students['ids'])
            print("All student data cleared")
        except Exception as e:
            print(f"Error clearing database: {e}")

    def get_collection_stats(self) -> Dict:
        """Get database statistics"""
        try:
            count = self.collection.count()
            return {
                "total_students": count,
                "collection_name": self.collection.name,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"error": str(e)}
