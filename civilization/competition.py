# civilization/competition.py

class Competition:

    def evaluate(self, results):

        best_score = -1
        winner = None

        for agent_name, result in results.items():

            score = 1 if result.get("success") else 0

            if score > best_score:
                best_score = score
                winner = agent_name

        return winner, best_score
