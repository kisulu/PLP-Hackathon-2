from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, Flashcard
from utils.ai_utils import generate_flashcards_from_text

flashcard_bp = Blueprint('flashcard', __name__)

@flashcard_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if len(text) < 50:
            return jsonify({'success': False, 'error': 'Please provide at least 50 characters of study material'}), 400
        
        # Generate flashcards using AI
        flashcards_data = generate_flashcards_from_text(text)
        
        if not flashcards_data:
            return jsonify({'success': False, 'error': 'Failed to generate flashcards. Please try again.'}), 500
        
        # Save flashcards to database
        saved_flashcards = []
        for card_data in flashcards_data:
            flashcard = Flashcard(
                user_id=current_user.id,
                title=card_data['title'],
                question=card_data['question'],
                answer=card_data['answer'],
                difficulty=card_data.get('difficulty', 'medium')
            )
            db.session.add(flashcard)
            saved_flashcards.append({
                'title': flashcard.title,
                'question': flashcard.question,
                'answer': flashcard.answer,
                'difficulty': flashcard.difficulty
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'flashcards': saved_flashcards,
            'count': len(saved_flashcards)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'An error occurred while generating flashcards'}), 500

@flashcard_bp.route('/library')
@login_required
def library():
    flashcards = Flashcard.query.filter_by(user_id=current_user.id).order_by(Flashcard.created_at.desc()).all()
    return render_template('flashcards.html', flashcards=flashcards)

@flashcard_bp.route('/study/<int:flashcard_id>')
@login_required
def study_single(flashcard_id):
    flashcard = Flashcard.query.filter_by(id=flashcard_id, user_id=current_user.id).first_or_404()
    return render_template('flashcards.html', flashcards=[flashcard], study_mode=True)

@flashcard_bp.route('/study/all')
@login_required
def study_all():
    flashcards = Flashcard.query.filter_by(user_id=current_user.id).all()
    return render_template('flashcards.html', flashcards=flashcards, study_mode=True)

@flashcard_bp.route('/update_stats', methods=['POST'])
@login_required
def update_stats():
    try:
        data = request.get_json()
        flashcard_id = data.get('flashcard_id')
        is_correct = data.get('is_correct', False)
        
        flashcard = Flashcard.query.filter_by(id=flashcard_id, user_id=current_user.id).first()
        if flashcard:
            flashcard.times_studied += 1
            if is_correct:
                flashcard.correct_answers += 1
            db.session.commit()
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@flashcard_bp.route('/delete/<int:flashcard_id>', methods=['DELETE'])
@login_required
def delete(flashcard_id):
    try:
        flashcard = Flashcard.query.filter_by(id=flashcard_id, user_id=current_user.id).first()
        if flashcard:
            db.session.delete(flashcard)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Flashcard not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500