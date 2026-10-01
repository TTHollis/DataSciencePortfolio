# tools

Two scripts I used to build this repository. Both print what they would do and
change nothing until you add `--apply`, so you can run them safely to look.

If you want to borrow these, read the honest assessment below first. One of
them you can use almost as is. The other is a pattern, not a tool.

## build_coursework.py

Copies a filtered subset of a local coursework folder into `coursework/<CourseName>/`.
It never modifies or deletes anything in the source. It skips junk, secrets,
oversized data and exact duplicates, and writes a manifest listing every file
it kept and every file it skipped with the reason.

**This one you can reuse.** Three edits:

1. Set the two paths near the top. `SRC` is wherever your coursework lives,
   `REPO` is your local clone of the repo you are building.

   ```python
   SRC = Path.home() / 'Coursework'
   REPO = Path.home() / 'YourRepoName'
   ```

2. Replace the `COURSES` dictionary with your own. The key is the folder name
   as it exists on your machine, the value is the readable name you want in the
   repo.

   ```python
   COURSES = {
       'DSC530': 'DataExplorationAndAnalysis',
       'DSC540': 'DataPreparation',
   }
   ```

3. Delete the `migrate_old_repo_folders` function and the call to it in `main`,
   along with `OLD_REPO_FOLDERS` and `OLD_PARTIAL_UPLOADS`. That part renames
   two folders that existed only in my repo. You also do not need the textbook
   repository names in `EXCLUDED_DIRS`; swap in whatever clutter you have.

Then run it twice:

```bash
python build_coursework.py            # dry run, writes the manifest only
python build_coursework.py --apply    # actually copies
```

Read the manifest before the second run. Mine caught an `.env` file and an
`APIkeys.json` that would otherwise have gone public, which is the single best
reason to look at the list rather than trusting the filters.

The size limits are worth tuning to your own work. Data files over 10 MB and
anything over 25 MB are skipped by default, and PDFs are excluded entirely
because GitHub renders notebooks natively.

## build_projects.py

Moves showcase projects out of `coursework/` into `projects/<ProjectName>/`
using `git mv`, so each file's history follows it, and renames the main
notebooks and papers to subject-based names.

**This one is a pattern rather than something you can edit into place.** All of
its value sits in the `PROJECT_MOVES` dictionary, which is a hand-written list
of my filenames mapped to new ones. You would be writing that list from
scratch for your own files, and at that point you have written your own script.

What is worth stealing is the shape of it:

- Dry run by default, so you see every planned move before anything happens.
- `git mv` rather than moving files in Explorer, so history follows the file
  instead of showing a delete and an unrelated add.
- Glob patterns, so a dozen figures are one line rather than twelve.
- A count of unmatched patterns at the end, which is how you catch a typo in a
  filename before it quietly does nothing.

If you only take one idea from these, take the dry run. Every destructive step
in both scripts is gated behind a flag, and that is the reason I was willing to
run them against years of coursework at all.
