import requests
import json
from config import Config

def generate_flashcards_from_text(text):
    """
    Generate flashcards from text using Hugging Face Question-Answering API
    """
    try:
        # If Hugging Face API key is available, use the real API
        if Config.HUGGINGFACE_API_KEY:
            return generate_with_huggingface_api(text)
        else:
            # Fallback to mock generation for demo purposes
            return generate_mock_flashcards(text)
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return generate_mock_flashcards(text)

def generate_with_huggingface_api(text):
    """
    Use Hugging Face Question-Answering API to generate flashcards
    """
    headers = {
        "Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Split text into chunks for better processing
    chunks = split_text_into_chunks(text, max_length=500)
    flashcards = []
    
    for i, chunk in enumerate(chunks[:5]):  # Limit to 5 flashcards
        # Generate questions based on the text
        questions = generate_questions_for_chunk(chunk)
        
        for j, question in enumerate(questions[:2]):  # Max 2 questions per chunk
            payload = {
                "inputs": {
                    "question": question,
                    "context": chunk
                }
            }
            
            try:
                response = requests.post(
                    Config.HUGGINGFACE_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('answer', '').strip()
                    
                    if answer and len(answer) > 10:
                        flashcards.append({
                            'title': f'Concept {len(flashcards) + 1}',
                            'question': question,
                            'answer': answer,
                            'difficulty': determine_difficulty(question, answer)
                        })
                        
            except requests.RequestException as e:
                print(f"API request failed: {e}")
                continue
    
    return flashcards if flashcards else generate_mock_flashcards(text)

def generate_mock_flashcards(text):
    """
    Generate mock flashcards for demo purposes when API is not available
    """
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if len(s.strip()) > 20]
    flashcards = []
    
    for i, sentence in enumerate(sentences[:5]):
        words = sentence.split()
        if len(words) < 5:
            continue
            
        # Find key terms (longer words)
        key_terms = [word for word in words if len(word) > 4 and word.isalpha()]
        
        if key_terms:
            key_term = key_terms[0]
            question = f"What is the main concept related to '{key_term}' in this context?"
            
            flashcards.append({
                'title': f'Study Card {i + 1}',
                'question': question,
                'answer': sentence.strip(),
                'difficulty': 'medium'
            })
    
    # Ensure we have at least 3 flashcards
    if len(flashcards) < 3 and len(text) > 100:
        additional_cards = [
            {
                'title': 'Key Concept',
                'question': 'What is the main topic discussed in this material?',
                'answer': text[:200] + '...' if len(text) > 200 else text,
                'difficulty': 'easy'
            },
            {
                'title': 'Important Details',
                'question': 'What are the important details mentioned in this study material?',
                'answer': 'The material covers various important concepts that require careful study and understanding.',
                'difficulty': 'medium'
            }
        ]
        flashcards.extend(additional_cards)
    
    return flashcards[:5]  # Return max 5 flashcards

def split_text_into_chunks(text, max_length=500):
    """
    Split text into manageable chunks for API processing
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def generate_questions_for_chunk(text):
    """
    Generate relevant questions for a text chunk
    """
    questions = [
        "What is the main concept explained in this text?",
        "What are the key points mentioned here?",
        "How would you summarize this information?",
        "What is the most important detail in this passage?"
    ]
    
    # Try to generate more specific questions based on content
    words = text.lower().split()
    
    if any(word in words for word in ['definition', 'define', 'meaning']):
        questions.insert(0, "What is being defined in this text?")
    
    if any(word in words for word in ['process', 'steps', 'procedure']):
        questions.insert(0, "What process or steps are described here?")
    
    if any(word in words for word in ['cause', 'effect', 'result']):
        questions.insert(0, "What cause and effect relationship is explained?")
    
    return questions[:3]  # Return top 3 questions

def determine_difficulty(question, answer):
    """
    Determine difficulty level based on question and answer complexity
    """
    answer_length = len(answer.split())
    question_complexity = len([word for word in question.split() if len(word) > 6])
    
    if answer_length < 10 and question_complexity < 2:
        return 'easy'
    elif answer_length > 30 or question_complexity > 3:
        return 'hard'
    else:
        return 'medium'