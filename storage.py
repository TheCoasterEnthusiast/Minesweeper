SCORES_FILE_NAME = 'scores.csv'


def get_scores(n=0):
    with open(SCORES_FILE_NAME, 'r') as file:
        scores = file.readlines()
        scores = [score.strip() for score in scores]
        if n:
            scores = scores[:n]
        return scores


def write_new_score(new_score: float):
    scores = get_scores()
    scores = [float(score) for score in scores]
    scores.append(new_score)
    scores.sort()
    scores = [f'{score}\n' for score in scores]
    with open(SCORES_FILE_NAME, 'w') as file:
        file.writelines(scores)
