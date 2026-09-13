# Hybrid Movie Recommender

A recommender that blends what a movie *is* with what people *watch together*, because each approach fails in a way the other covers.

## The problem

Content-based recommenders match on attributes, so they are reliable but narrow: ask for something like a given comedy and you get more comedies, forever. Collaborative filtering matches on behavior, so it surfaces genuinely surprising connections but collapses on anything without enough ratings, the cold start problem.

Neither is satisfying alone. This project builds both and scores them together.

## Data

MovieLens (ml-latest-small): 9,742 movies, 100,836 ratings from 610 users, and 3,683 user-applied tags. Small enough to run on a laptop and large enough for the sparsity problem to be real, since only 1,572 of 9,742 movies carry any tags at all.

## Approach

The content side builds a text representation of each movie from its genres plus its user tags, vectorizes with TF-IDF into a 1,677 term vocabulary, and computes cosine similarity across the full 9,742 by 9,742 matrix.

The collaborative side pivots ratings into a user-by-movie matrix of 610 by 9,724, factorizes it with truncated SVD at 50 latent components capturing 53.9 percent of variance, and computes movie-to-movie similarity in that latent space. A minimum of 10 ratings is required for a movie to be recommendable, which leaves 2,269 eligible titles.

The hybrid score is a weighted blend, 40 percent content and 60 percent collaborative. Collaborative gets the larger weight because behavioral signal tends to produce the more interesting recommendations when it is available, while content keeps the result sane when it is not.

## What it produces

Asked for recommendations based on *The Devil Wears Prada*, the top result is *Marley & Me* with a hybrid score of 0.665, drawn from a perfect content match at 1.0 and a moderate collaborative signal at 0.442. Further down, *The Great Gatsby* appears at 0.631 on the opposite profile, a weaker content match at 0.679 but the strongest collaborative signal in the list at 0.599.

That contrast is the point of the blend. A pure content recommender would never have surfaced *Gatsby*, and a pure collaborative one would have ranked it above better-matched titles. Each recommendation is returned with its component scores visible alongside the blend, so the reason for a suggestion is inspectable rather than hidden.

## Limitations

53.9 percent explained variance at 50 components means roughly half the signal in the ratings matrix is left on the floor. More components would capture more and would also overfit a 610-user matrix.

Tag coverage is the bigger constraint. With 16 percent of movies carrying tags, most content vectors are genre strings alone, which makes the content side coarser than the vocabulary size suggests.

There is also no offline evaluation here, no held-out ratings and no precision at k. The recommendations are assessed qualitatively, which is enough to demonstrate the mechanism and not enough to claim the blend weights are optimal. Tuning that 40/60 split against a held-out set is the obvious next step.

## Files

| File | Contents |
|---|---|
| `hybrid_movie_recommender.ipynb` | Full build: content similarity, SVD collaborative filtering, hybrid scoring, example recommendations |
| `ml-latest-small/` | MovieLens data: movies, ratings, tags, links |

## Running it

```bash
pip install pandas numpy scikit-learn matplotlib
jupyter lab hybrid_movie_recommender.ipynb
```

All data is included in this folder.

## Reference

Harper, F. M., & Konstan, J. A. (2015). The MovieLens datasets: History and context. *ACM Transactions on Interactive Intelligent Systems, 5*(4), 1-19. https://doi.org/10.1145/2827872
