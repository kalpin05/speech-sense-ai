from sqlalchemy.orm import Session
from app.models.badge_model import UserBadge
from app.models.session_model import TherapySession
from datetime import date
import logging

log = logging.getLogger(__name__)

def calculate_streak(sessions) -> int:
    """Calculate the consecutive days active ending today or yesterday."""
    if not sessions:
        return 0
        
    # Extract unique session dates
    dates = sorted(list({s.created_at.date() for s in sessions}), reverse=True)
    if not dates:
        return 0
        
    today = date.today()
    
    # If the most recent session is older than yesterday, the streak is 0
    if (today - dates[0]).days > 1:
        return 0
        
    streak = 1
    for i in range(len(dates) - 1):
        diff = (dates[i] - dates[i+1]).days
        if diff == 1:
            streak += 1
        elif diff > 1:
            break
            
    return streak

def check_and_unlock_badges(user_id, db: Session, current_accuracy: float):
    """Evaluate badge logic and persist newly unlocked badges."""
    try:
        # Fetch all user sessions
        sessions = db.query(TherapySession).filter(TherapySession.user_id == user_id).all()
        total_attempts = len(sessions)
        
        # Get already unlocked badge IDs
        unlocked_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
        unlocked_ids = {b.badge_id for b in unlocked_badges}
        
        badges_to_unlock = []
        
        # b1: First Attempt
        if total_attempts >= 1 and 'b1' not in unlocked_ids:
            badges_to_unlock.append('b1')
            
        # b2: Score 80+
        if (current_accuracy >= 80 or any(s.accuracy_score >= 80 for s in sessions)) and 'b2' not in unlocked_ids:
            badges_to_unlock.append('b2')
            
        # b3: Score 90+
        if (current_accuracy >= 90 or any(s.accuracy_score >= 90 for s in sessions)) and 'b3' not in unlocked_ids:
            badges_to_unlock.append('b3')
            
        # b4: 5 Day Streak
        streak = calculate_streak(sessions)
        if streak >= 5 and 'b4' not in unlocked_ids:
            badges_to_unlock.append('b4')
            
        # b5: 10 Attempts
        if total_attempts >= 10 and 'b5' not in unlocked_ids:
            badges_to_unlock.append('b5')
            
        # b6: Pro Speaker (avg accuracy >= 85)
        if total_attempts > 0:
            avg_score = sum(s.accuracy_score for s in sessions) / total_attempts
            if avg_score >= 85 and 'b6' not in unlocked_ids:
                badges_to_unlock.append('b6')
                
        # Persist new badges
        for badge_id in badges_to_unlock:
            new_badge = UserBadge(user_id=user_id, badge_id=badge_id)
            db.add(new_badge)
            log.info(f"Badge {badge_id} unlocked for user {user_id}")
            
    except Exception as e:
        log.error(f"Failed to check/unlock badges: {e}")
