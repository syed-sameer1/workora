from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import Job

def recommend_jobs_from_db(user, db):
    jobs = db.query(Job).all()

    job_skills = [job.skills.replace(",", " ") for job in jobs]
    user_skills = user.skills.replace(",", " ")

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([user_skills] + job_skills)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])[0]

    results = []
    for i, score in enumerate(similarity_scores):
        if (
            score > 0.4
            and jobs[i].experience <= user.experience
            and jobs[i].education.lower() in user.education.lower()
        ):
            results.append({
                "title": jobs[i].title,
                "skills": jobs[i].skills,
                "experience": jobs[i].experience,
                "education": jobs[i].education,
                "score": round(score, 2)
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
