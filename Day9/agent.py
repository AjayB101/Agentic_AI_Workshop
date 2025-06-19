from typing import Dict, List, Tuple, Any
from langchain.schema import HumanMessage
from model_utils import (
    get_gemini_llm,
    ACADEMIC_SCORING_PROMPT,
    SOFT_SKILLS_PROMPT,
    READINESS_ANALYSIS_PROMPT,
    INTERVENTION_PROMPT,
    QUERY_ANALYSIS_PROMPT,
    RAG_RESPONSE_PROMPT
)
import re


class BaseAgent:
    """Base class for all agents"""

    def __init__(self, llm=None):
        self.llm = llm or get_gemini_llm()

    def invoke_llm(self, prompt: str) -> str:
        """Invoke LLM with error handling"""
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"Error invoking LLM: {e}")
            return ""


class AcademicPerformanceAgent(BaseAgent):
    """Agent for evaluating academic performance"""

    def evaluate(self, student_data: Dict) -> Tuple[float, str]:
        """Evaluate academic performance and return score with reasoning"""
        try:
            prompt = ACADEMIC_SCORING_PROMPT.format(
                attendance=student_data.get('attendance', 0),
                test_score=student_data.get('test_score', 0),
                assignment_percentage=student_data.get(
                    'assignment_percentage', 0),
                event_participation=student_data.get(
                    'event_participation', 'No')
            )

            response = self.invoke_llm(prompt)

            # Parse response
            score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', response)
            reasoning_match = re.search(
                r'REASONING:\s*(.+)', response, re.DOTALL)

            if score_match:
                score = float(score_match.group(1))
                reasoning = reasoning_match.group(1).strip(
                ) if reasoning_match else "Academic performance calculated based on multiple factors."
                return min(100, score), reasoning
            else:
                # Fallback calculation
                return self._fallback_calculation(student_data)

        except Exception as e:
            print(f"Error in academic evaluation: {e}")
            return self._fallback_calculation(student_data)

    def _fallback_calculation(self, student_data: Dict) -> Tuple[float, str]:
        """Fallback calculation if LLM fails"""
        score = (
            0.3 * student_data.get('attendance', 0) +
            0.3 * student_data.get('test_score', 0) +
            0.3 * student_data.get('assignment_percentage', 0) +
            (10 if str(student_data.get('event_participation', '')
                       ).strip().lower() == 'yes' else 0)
        )
        return min(100, score), "Calculated from attendance, tests, assignments, and events."


class SoftSkillsAgent(BaseAgent):
    """Agent for evaluating soft skills and communication"""

    def evaluate(self, student_data: Dict) -> Tuple[float, str]:
        """Evaluate soft skills and return score with reasoning"""
        try:
            linkedin_bio = student_data.get('linkedin_bio', 'Not provided')
            resume_text = student_data.get('resume_text', 'Not provided')

            # If no bio or resume provided, use existing score
            if linkedin_bio == 'Not provided' and resume_text == 'Not provided':
                existing_score = student_data.get('softskill_score', 50)
                return float(existing_score), "Score based on provided soft skills assessment."

            prompt = SOFT_SKILLS_PROMPT.format(
                linkedin_bio=linkedin_bio,
                resume_text=resume_text
            )

            response = self.invoke_llm(prompt)

            # Parse response
            score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', response)
            reasoning_match = re.search(
                r'REASONING:\s*(.+)', response, re.DOTALL)

            if score_match:
                score = float(score_match.group(1))
                reasoning = reasoning_match.group(1).strip(
                ) if reasoning_match else "Communication skills evaluated from professional profile."
                return min(100, score), reasoning
            else:
                # Use existing score as fallback
                existing_score = student_data.get('softskill_score', 50)
                return float(existing_score), "Score based on provided assessment."

        except Exception as e:
            print(f"Error in soft skills evaluation: {e}")
            existing_score = student_data.get('softskill_score', 50)
            return float(existing_score), "Score based on provided assessment."


class ReadinessAnalysisAgent(BaseAgent):
    """Agent for calculating overall placement readiness"""

    def analyze(self, student_name: str, academic_score: float, communication_score: float) -> Dict:
        """Analyze placement readiness and return comprehensive results"""
        try:
            prompt = READINESS_ANALYSIS_PROMPT.format(
                student_name=student_name,
                academic_score=academic_score,
                communication_score=communication_score
            )

            response = self.invoke_llm(prompt)

            # Parse response
            overall_match = re.search(
                r'OVERALL_SCORE:\s*(\d+(?:\.\d+)?)', response)
            tech_match = re.search(
                r'TECH_READINESS:\s*(\d+(?:\.\d+)?)', response)
            comm_match = re.search(
                r'COMM_READINESS:\s*(\d+(?:\.\d+)?)', response)
            analysis_match = re.search(
                r'ANALYSIS:\s*(.+)', response, re.DOTALL)

            if overall_match:
                return {
                    'overall_score': int(float(overall_match.group(1))),
                    'tech_readiness': int(float(tech_match.group(1))) if tech_match else int(academic_score),
                    'comm_readiness': int(float(comm_match.group(1))) if comm_match else int(communication_score),
                    'analysis': analysis_match.group(1).strip() if analysis_match else "Placement readiness calculated based on academic and communication scores."
                }
            else:
                return self._fallback_analysis(academic_score, communication_score)

        except Exception as e:
            print(f"Error in readiness analysis: {e}")
            return self._fallback_analysis(academic_score, communication_score)

    def _fallback_analysis(self, academic_score: float, communication_score: float) -> Dict:
        """Fallback analysis calculation"""
        tech = int(academic_score)
        comm = int(communication_score)
        overall = int(0.6 * tech + 0.4 * comm)

        return {
            'overall_score': overall,
            'tech_readiness': tech,
            'comm_readiness': comm,
            'analysis': f"Overall readiness: {overall}%. Technical: {tech}%, Communication: {comm}%"
        }


class InterventionAgent(BaseAgent):
    """Agent for recommending interventions and improvements"""

    def recommend(self, student_name: str, overall_score: int, tech_score: int, comm_score: int) -> List[str]:
        """Generate intervention recommendations"""
        try:
            prompt = INTERVENTION_PROMPT.format(
                student_name=student_name,
                overall_score=overall_score,
                tech_score=tech_score,
                comm_score=comm_score
            )

            response = self.invoke_llm(prompt)

            # Parse recommendations
            recommendations = []
            lines = response.split('\n')
            in_recommendations = False

            for line in lines:
                line = line.strip()
                if 'RECOMMENDATIONS:' in line:
                    in_recommendations = True
                    continue
                elif in_recommendations and line:
                    # Remove numbering and clean up
                    clean_line = re.sub(r'^\d+\.\s*', '', line)
                    if clean_line:
                        recommendations.append(clean_line)

            return recommendations if recommendations else self._fallback_recommendations(overall_score, tech_score, comm_score)

        except Exception as e:
            print(f"Error in intervention recommendations: {e}")
            return self._fallback_recommendations(overall_score, tech_score, comm_score)

    def _fallback_recommendations(self, overall_score: int, tech_score: int, comm_score: int) -> List[str]:
        """Fallback recommendations"""
        recs = []
        if overall_score < 70:
            recs.append(
                "Join a comprehensive placement bootcamp to improve overall readiness.")
        if comm_score < 65:
            recs.append("Attend resume writing and communication workshops.")
        if tech_score < 65:
            recs.append(
                "Practice coding problems on platforms like LeetCode and HackerRank.")
        if overall_score >= 70:
            recs.append(
                "You're on track! Focus on mock interviews and company-specific preparation.")

        return recs or ["Continue your current preparation and focus on consistent improvement."]


class QueryAnalysisAgent(BaseAgent):
    """Agent for analyzing user queries and filtering students"""

    def analyze_query(self, user_query: str, all_student_data: List[Dict]) -> List[str]:
        """Analyze user query and return list of student names to show"""
        try:
            # Create student summary
            student_summary = []
            for student in all_student_data:
                student_summary.append(
                    f"- {student['name']}: Overall {student['overall_score']}%, "
                    f"Academic {student['academic_score']:.1f}%, Communication {student['communication_score']}%"
                )

            prompt = QUERY_ANALYSIS_PROMPT.format(
                user_query=user_query,
                available_students='\n'.join(student_summary)
            )

            response = self.invoke_llm(prompt)

            # Parse response
            response = response.strip()
            if response.upper() == "ALL":
                return [student['name'] for student in all_student_data]
            else:
                # Parse comma-separated names
                student_names = [name.strip()
                                 for name in response.split(',') if name.strip()]
                # Validate names exist
                valid_names = [student['name'] for student in all_student_data]
                filtered_names = [
                    name for name in student_names if name in valid_names]
                return filtered_names if filtered_names else [student['name'] for student in all_student_data]

        except Exception as e:
            print(f"Error in query analysis: {e}")
            return [student['name'] for student in all_student_data]


class RAGResponseAgent(BaseAgent):
    """Agent for generating responses using RAG"""

    def generate_response(self, context: str, question: str) -> str:
        """Generate comprehensive response using context"""
        try:
            prompt = RAG_RESPONSE_PROMPT.format(
                context=context,
                question=question
            )

            response = self.invoke_llm(prompt)
            return response.strip()

        except Exception as e:
            print(f"Error in RAG response generation: {e}")
            return "I apologize, but I encountered an error while processing your request. Please try again."


class MultiAgentSystem:
    """Orchestrator for all agents"""

    def __init__(self, llm=None):
        self.llm = llm or get_gemini_llm()
        self.academic_agent = AcademicPerformanceAgent(self.llm)
        self.soft_skills_agent = SoftSkillsAgent(self.llm)
        self.readiness_agent = ReadinessAnalysisAgent(self.llm)
        self.intervention_agent = InterventionAgent(self.llm)
        self.query_agent = QueryAnalysisAgent(self.llm)
        self.rag_agent = RAGResponseAgent(self.llm)

    def process_student(self, student_data: Dict) -> Dict:
        """Process a single student through all agents"""
        # Get academic score
        academic_score, academic_reasoning = self.academic_agent.evaluate(
            student_data)

        # Get soft skills score
        comm_score, comm_reasoning = self.soft_skills_agent.evaluate(
            student_data)

        # Get readiness analysis
        readiness_results = self.readiness_agent.analyze(
            student_data['name'], academic_score, comm_score
        )

        # Get recommendations
        recommendations = self.intervention_agent.recommend(
            student_data['name'],
            readiness_results['overall_score'],
            readiness_results['tech_readiness'],
            readiness_results['comm_readiness']
        )

        return {
            'name': student_data['name'],
            'academic_score': academic_score,
            'academic_reasoning': academic_reasoning,
            'communication_score': comm_score,
            'communication_reasoning': comm_reasoning,
            'overall_score': readiness_results['overall_score'],
            'tech_readiness': readiness_results['tech_readiness'],
            'comm_readiness': readiness_results['comm_readiness'],
            'analysis': readiness_results['analysis'],
            'recommendations': recommendations,
            'raw_data': student_data
        }

    def filter_students_by_query(self, user_query: str, all_student_data: List[Dict]) -> List[str]:
        """Filter students based on user query"""
        return self.query_agent.analyze_query(user_query, all_student_data)

    def generate_rag_response(self, context: str, question: str) -> str:
        """Generate RAG response"""
        return self.rag_agent.generate_response(context, question)
