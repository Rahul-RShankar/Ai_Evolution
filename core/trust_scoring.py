# core/trust_scoring.py

class TrustScoring:

    def __init__(self):
        # Default trust scores for users
        self.user_trust = {
            "root_admin": 1.0,
            "guest": 0.5
        }

    def get_weight(self, user_id):
        """
        Return the training weight for a given user.
        """
        return self.user_trust.get(user_id, 0.5)

    def record_accuracy(self, user_id, was_correct):
        """
        Dynamically adjust trust based on comparison with agent consensus or future cycles.
        """
        current = self.user_trust.get(user_id, 0.5)
        if was_correct:
            self.user_trust[user_id] = min(current + 0.05, 1.0)
        else:
            self.user_trust[user_id] = max(current - 0.1, 0.1)
