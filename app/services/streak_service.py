from datetime import datetime, date
from sqlalchemy import func, extract

from app import db
from app.models import User, Timeline


class StreakService:
    @staticmethod
    def check_missed_days(user_id: int) -> bool:
        """
        Check if user has missed days and reset streak if needed.
        Returns True if streak was reset, False otherwise.
        """
        # Get user's latest timeline
        latest_timeline = (
            Timeline.query.filter_by(user_id=user_id)
            .order_by(Timeline.date.desc())
            .first()
        )
        
        if not latest_timeline:
            return False
        
        # Calculate days difference
        today = date.today()
        latest_date = latest_timeline.date.date()
        days_diff = (today - latest_date).days
        
        # If gap > 1 day, reset streak to 1
        if days_diff > 1:
            user = User.query.get(user_id)
            if user:
                user.streak = 1
                db.session.commit()
                return True
        
        return False
    
    @staticmethod
    def get_streak_info(user_id: int) -> dict:
        """
        Get comprehensive streak information for a user.
        """
        user = User.query.get(user_id)
        latest_timeline = (
            Timeline.query.filter_by(user_id=user_id)
            .order_by(Timeline.date.desc())
            .first()
        )
        
        info = {
            "current_streak": user.streak if user and user.streak is not None else 0,
            "latest_timeline_date": latest_timeline.date.date() if latest_timeline else None,
            "days_since_last_timeline": None,
            "has_missed_days": False
        }
        
        if latest_timeline:
            today = date.today()
            days_diff = (today - latest_timeline.date.date()).days
            info["days_since_last_timeline"] = days_diff
            info["has_missed_days"] = days_diff > 1
        
        return info