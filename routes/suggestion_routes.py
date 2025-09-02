from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Suggestion, User
from utils.email_utils import send_bulk_confirmation_emails

suggestion_bp = Blueprint('suggestion', __name__)

@suggestion_bp.route('/')
@login_required
def suggestions():
    user_suggestions = Suggestion.query.filter_by(user_id=current_user.id).order_by(Suggestion.created_at.desc()).all()
    return render_template('suggestions.html', suggestions=user_suggestions)

@suggestion_bp.route('/submit', methods=['POST'])
@login_required
def submit():
    try:
        if request.is_json:
            data = request.get_json()
            content = data.get('content', '').strip()
        else:
            content = request.form.get('content', '').strip()
        
        if len(content) < 10:
            error_msg = 'Please provide a meaningful suggestion (at least 10 characters)'
            if request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 400
            flash(error_msg, 'error')
            return redirect(url_for('suggestion.suggestions'))
        
        # Create new suggestion
        suggestion = Suggestion(
            user_id=current_user.id,
            content=content
        )
        
        db.session.add(suggestion)
        db.session.commit()
        
        success_msg = 'Thank you! Your suggestion has been submitted successfully.'
        if request.is_json:
            return jsonify({'success': True, 'message': success_msg})
        
        flash(success_msg, 'success')
        return redirect(url_for('suggestion.suggestions'))
        
    except Exception as e:
        db.session.rollback()
        error_msg = 'Failed to submit suggestion. Please try again.'
        if request.is_json:
            return jsonify({'success': False, 'error': error_msg}), 500
        flash(error_msg, 'error')
        return redirect(url_for('suggestion.suggestions'))

@suggestion_bp.route('/send_confirmations', methods=['POST'])
@login_required
def send_confirmations():
    try:
        # Get all users who submitted suggestions but haven't received confirmation
        users_with_suggestions = db.session.query(User).join(Suggestion).filter(
            Suggestion.email_sent == False
        ).distinct().all()
        
        if not users_with_suggestions:
            message = 'No pending confirmations to send'
            if request.is_json:
                return jsonify({'success': True, 'message': message})
            flash(message, 'info')
            return redirect(url_for('suggestion.suggestions'))
        
        # Send bulk emails
        success_count = send_bulk_confirmation_emails(users_with_suggestions)
        
        if success_count > 0:
            # Mark suggestions as email sent
            Suggestion.query.filter_by(email_sent=False).update({'email_sent': True})
            db.session.commit()
            
            message = f'Confirmation emails sent to {success_count} users successfully!'
            if request.is_json:
                return jsonify({'success': True, 'message': message})
            flash(message, 'success')
        else:
            error_msg = 'Failed to send confirmation emails'
            if request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 500
            flash(error_msg, 'error')
        
        return redirect(url_for('suggestion.suggestions'))
        
    except Exception as e:
        error_msg = f'Error sending confirmations: {str(e)}'
        if request.is_json:
            return jsonify({'success': False, 'error': error_msg}), 500
        flash(error_msg, 'error')
        return redirect(url_for('suggestion.suggestions'))