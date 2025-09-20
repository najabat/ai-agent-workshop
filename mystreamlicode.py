import streamlit as st
import re
import random
from typing import List, Dict, Tuple

class AssignmentQuizGenerator:
    def __init__(self):
        self.key_phrases = [
            "definition", "concept", "principle", "theory", "method", "process",
            "example", "characteristic", "feature", "advantage", "disadvantage",
            "cause", "effect", "result", "consequence", "factor", "element"
        ]
        
        self.question_starters = [
            "What is", "How does", "Why is", "When did", "Where does",
            "Which of the following", "What are the main", "How can you explain"
        ]
    
    def extract_key_sentences(self, text: str, min_length: int = 50) -> List[str]:
        """Extract meaningful sentences from text that could form good questions."""
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Filter sentences based on length and content
        key_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) >= min_length:
                # Check if sentence contains key educational phrases
                if any(phrase in sentence.lower() for phrase in self.key_phrases):
                    key_sentences.append(sentence)
                # Also include sentences with numbers or specific terms
                elif re.search(r'\d+|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', sentence):
                    key_sentences.append(sentence)
        
        return key_sentences[:10]  # Limit to top 10 sentences
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract important terms and concepts from the text."""
        # Find capitalized words (likely proper nouns or important terms)
        terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Find technical terms (words that appear frequently)
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        word_freq = {}
        for word in words:
            if word not in ['this', 'that', 'with', 'from', 'they', 'have', 'been', 'said', 'each', 'which']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent words
        frequent_terms = [word for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]]
        
        return list(set(terms + [term.capitalize() for term in frequent_terms]))[:10]
    
    def generate_assignments(self, text: str) -> List[str]:
        """Generate 2 essay-style assignment questions."""
        key_sentences = self.extract_key_sentences(text)
        key_terms = self.extract_key_terms(text)
        
        assignments = []
        
        # Assignment 1: Analysis-based
        if key_sentences:
            main_concept = key_terms[0] if key_terms else "the main topic"
            assignments.append(
                f"Analyze the key concepts presented in the text regarding {main_concept}. "
                f"Discuss how these concepts relate to each other and provide specific examples "
                f"from the material to support your analysis. (500-750 words)"
            )
        
        # Assignment 2: Application-based
        if len(key_terms) > 1:
            concept1, concept2 = key_terms[0], key_terms[1]
            assignments.append(
                f"Compare and contrast {concept1} and {concept2} as discussed in the material. "
                f"Evaluate their significance and explain how understanding these concepts "
                f"could be applied in real-world scenarios. Include critical reflection on the "
                f"strengths and limitations of each approach. (600-800 words)"
            )
        else:
            assignments.append(
                f"Critically evaluate the information presented in the text. "
                f"What are the main arguments or points made? Do you agree or disagree "
                f"with these points? Support your position with evidence and reasoning. (500-700 words)"
            )
        
        return assignments
    
    def generate_quiz_questions(self, text: str) -> List[Dict]:
        """Generate 3 multiple-choice quiz questions."""
        key_sentences = self.extract_key_sentences(text)
        key_terms = self.extract_key_terms(text)
        
        quiz_questions = []
        
        # Question 1: Definition-based
        if key_terms and key_sentences:
            term = random.choice(key_terms[:3])
            # Find sentence containing this term
            context_sentence = None
            for sentence in key_sentences:
                if term.lower() in sentence.lower():
                    context_sentence = sentence
                    break
            
            if context_sentence:
                question = f"Based on the text, what is {term}?"
                correct_answer = f"As described in the context: {context_sentence[:100]}..."
                wrong_answers = [
                    f"A completely different concept not mentioned in the text",
                    f"An alternative definition that contradicts the source material",
                    f"A related but incorrect interpretation of {term}"
                ]
                
                options = [correct_answer] + wrong_answers
                random.shuffle(options)
                correct_index = options.index(correct_answer)
                
                quiz_questions.append({
                    "question": question,
                    "options": options,
                    "correct_answer": correct_index,
                    "explanation": f"The correct answer is based on the definition provided in the source text."
                })
        
        # Question 2: Comprehension-based
        if len(key_sentences) >= 2:
            sentence = random.choice(key_sentences[:3])
            # Create a question about the main idea of this sentence
            question = f"According to the text, which statement best represents the main idea?"
            correct_answer = sentence[:80] + "..." if len(sentence) > 80 else sentence
            wrong_answers = [
                "A statement that contradicts the source material",
                "An idea not mentioned in the provided text",
                "A partially correct but incomplete interpretation"
            ]
            
            options = [correct_answer] + wrong_answers
            random.shuffle(options)
            correct_index = options.index(correct_answer)
            
            quiz_questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_index,
                "explanation": f"This statement directly reflects information from the source text."
            })
        
        # Question 3: Application-based
        if key_terms:
            main_term = key_terms[0]
            question = f"How might {main_term} be applied or relevant in practical situations?"
            correct_answer = f"It can be applied by understanding its principles and implementing them contextually"
            wrong_answers = [
                f"{main_term} has no practical applications",
                f"It should be ignored in real-world scenarios",
                f"It only applies to theoretical situations with no practical value"
            ]
            
            options = [correct_answer] + wrong_answers
            random.shuffle(options)
            correct_index = options.index(correct_answer)
            
            quiz_questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_index,
                "explanation": f"Understanding {main_term} allows for practical application of its underlying principles."
            })
        
        # Fill remaining slots if we don't have enough questions
        while len(quiz_questions) < 3:
            question = f"Based on the provided text, which of the following is most accurate?"
            correct_answer = "The information supports evidence-based conclusions"
            wrong_answers = [
                "The text provides no useful information",
                "All statements in the text are opinion-based",
                "The content contradicts established knowledge"
            ]
            
            options = [correct_answer] + wrong_answers
            random.shuffle(options)
            correct_index = options.index(correct_answer)
            
            quiz_questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_index,
                "explanation": "This answer reflects critical analysis of the source material."
            })
        
        return quiz_questions[:3]


def main():
    st.set_page_config(
        page_title="Assignment & Quiz Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Assignment & Quiz Generator")
    st.markdown("""
    This tool helps educators create assignments and quizzes based on any document or topic.
    Simply paste your content below and get instant educational materials!
    """)
    
    # Initialize the generator
    generator = AssignmentQuizGenerator()
    
    # Input section
    st.header("📝 Input Your Content")
    input_text = st.text_area(
        "Enter your document text or topic description:",
        height=200,
        placeholder="Paste your document content here... The more detailed the content, the better the generated questions will be."
    )
    
    # Generate button
    if st.button("🎯 Generate Assignments & Quiz", type="primary"):
        if input_text.strip():
            with st.spinner("Analyzing content and generating questions..."):
                # Generate assignments and quiz
                assignments = generator.generate_assignments(input_text)
                quiz_questions = generator.generate_quiz_questions(input_text)
                
                # Display results
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.header("📋 Assignment Questions")
                    for i, assignment in enumerate(assignments, 1):
                        st.subheader(f"Assignment {i}")
                        st.write(assignment)
                        st.markdown("---")
                
                with col2:
                    st.header("🧠 Quiz Questions")
                    for i, quiz in enumerate(quiz_questions, 1):
                        st.subheader(f"Question {i}")
                        st.write(quiz["question"])
                        
                        # Display options
                        for j, option in enumerate(quiz["options"]):
                            prefix = "✅" if j == quiz["correct_answer"] else "❌"
                            st.write(f"{prefix} {chr(65+j)}) {option}")
                        
                        st.info(f"**Explanation:** {quiz['explanation']}")
                        st.markdown("---")
                
                # Export functionality
                st.header("💾 Export Options")
                
                # Create downloadable content
                export_content = "# Generated Assignments and Quiz\n\n"
                export_content += "## Assignment Questions\n\n"
                for i, assignment in enumerate(assignments, 1):
                    export_content += f"### Assignment {i}\n{assignment}\n\n"
                
                export_content += "## Quiz Questions\n\n"
                for i, quiz in enumerate(quiz_questions, 1):
                    export_content += f"### Question {i}\n"
                    export_content += f"{quiz['question']}\n\n"
                    for j, option in enumerate(quiz["options"]):
                        marker = "**[CORRECT]**" if j == quiz["correct_answer"] else ""
                        export_content += f"{chr(65+j)}) {option} {marker}\n"
                    export_content += f"\n**Explanation:** {quiz['explanation']}\n\n"
                
                st.download_button(
                    label="📄 Download as Markdown",
                    data=export_content,
                    file_name="assignments_and_quiz.md",
                    mime="text/markdown"
                )
        else:
            st.warning("⚠️ Please enter some content to generate assignments and quiz questions.")
    
    # Help section
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        **Tips for best results:**
        
        1. **Content Length**: Provide at least 200-300 words for better question generation
        2. **Content Quality**: Include clear concepts, definitions, and explanations
        3. **Structure**: Well-organized content with clear sentences works best
        4. **Topics**: Works with any subject - science, history, literature, business, etc.
        
        **What you get:**
        - 2 essay-style assignment questions (analysis and application focused)
        - 3 multiple-choice quiz questions with explanations
        - Downloadable markdown file with all generated content
        
        **Question Types:**
        - **Assignments**: Critical thinking, analysis, comparison, and application questions
        - **Quiz**: Definition-based, comprehension, and application multiple-choice questions
        """)


if __name__ == "__main__":
    main()