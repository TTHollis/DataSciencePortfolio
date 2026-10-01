'''
build_coursework.py

Copies a curated subset of C:\\Users\\slimt\\Coursework into the DataSciencePortfolio repo
under coursework/<CourseName>/, applying keep and exclude rules, skipping
exact-duplicate files, and writing a manifest of everything kept and skipped.

Nothing in Coursework is ever modified or deleted.

Usage (Anaconda Prompt, any env):
    python build_coursework.py            dry run: prints the manifest, copies nothing
    python build_coursework.py --apply    actually copies the files
'''

import hashlib
import shutil
import sys
from pathlib import Path

SRC = Path.home() / 'Coursework'
REPO = Path.home() / 'DataSciencePortfolio'
DEST = REPO / 'coursework'
MANIFEST = Path.home() / 'coursework_manifest.txt'
OLD_UPLOADS = Path.home() / '_old_partial_uploads'

COURSES = {
    'DSC530': 'DataExplorationAndAnalysis',
    'DSC540': 'DataPreparation',
    'DSC550': 'DataMining',
    'DSC630': 'PredictiveAnalytics',
    'DSC640': 'DataPresentationAndVisualization',
    'DSC670': 'AdvancedGenerativeAI',
    'DSC680': 'AppliedDataScience',
}

OLD_REPO_FOLDERS = {
    'Py': 'IntroductionToProgramming',
    'R': 'StatisticsForDataScience',
}

OLD_PARTIAL_UPLOADS = ['Data Exploration and Analysis', 'Data Preparation']

EXCLUDED_DIRS = {
    '.ipynb_checkpoints', '.idea', '__pycache__', '.git', '.vscode',
    'miniconda', 'mlartifacts', 'MNIST',
    'Hands-On-Data-Analysis-with-Pandas-2nd-edition-master',
    'practical-statistics-for-data-scientists',
    'pydata-book', 'The-Data-Wrangling-Workshop', 'openaccess-master',
}

EXCLUDED_SUFFIXES = {'.pdf', '.mp4', '.zip', '.odt', '.pyc', '.log'}

EXCLUDED_NAMES = {
    '.env', 'APIkeys.json', 'census_config.json', 'mlflow.db',
    '___All_Errors.txt', 'New Text Document.txt', 'Thumbs.db', '.DS_Store',
}

EXCLUDED_PREFIXES = ('.~lock', 'sandbox', 'Untitled')
EXCLUDED_CONTAINS = ('WAVES-ACCESS-RECORDS',)

DATA_SUFFIXES = {'.csv', '.tsv', '.xlsx', '.xlsm', '.xls', '.json', '.db',
                 '.sqlite', '.parquet', '.txt', ''}
DATA_MAX_MB = 10
OTHER_MAX_MB = 25

MB = 1_048_576


def exclusion_reason(path):
    '''Return why a file is excluded, or None if it should be kept.'''
    name = path.name
    suffix = path.suffix.lower()
    size_mb = path.stat().st_size / MB
    course_code = path.relative_to(SRC).parts[0]

    if any(part in EXCLUDED_DIRS for part in path.relative_to(SRC).parts[:-1]):
        return 'excluded folder'
    other_codes = [c for c in COURSES if c != course_code and c in name]
    if other_codes:
        return f'misfiled: belongs to {other_codes[0]}'
    if name in EXCLUDED_NAMES:
        return 'secret or junk file'
    if name.startswith(EXCLUDED_PREFIXES):
        return 'lock, sandbox, or untitled file'
    if any(token in name for token in EXCLUDED_CONTAINS):
        return 'bulk raw data (excluded by name)'
    if suffix in EXCLUDED_SUFFIXES:
        return f'{suffix} files are not kept'
    if suffix in DATA_SUFFIXES and size_mb > DATA_MAX_MB:
        return f'data file over {DATA_MAX_MB} MB ({size_mb:,.1f} MB)'
    if size_mb > OTHER_MAX_MB:
        return f'file over {OTHER_MAX_MB} MB ({size_mb:,.1f} MB)'
    return None


def file_hash(path):
    '''MD5 of the file contents, used to catch exact duplicates.'''
    digest = hashlib.md5()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def plan_course(course_dir):
    '''Walk one course folder and decide keep or skip for every file.'''
    kept, skipped = [], []
    seen_hashes = {}
    files = sorted(course_dir.rglob('*'), key=lambda p: (len(p.name), str(p)))
    for path in files:
        if not path.is_file():
            continue
        reason = exclusion_reason(path)
        if reason is None:
            digest = file_hash(path)
            if digest in seen_hashes:
                reason = f'exact duplicate of {seen_hashes[digest].name}'
            else:
                seen_hashes[digest] = path
        if reason is None:
            kept.append(path)
        else:
            skipped.append((path, reason))
    return kept, skipped


def copy_kept(course_dir, kept, apply):
    '''Copy kept files into coursework/<CourseName>/, preserving subfolders.'''
    target_root = DEST / COURSES[course_dir.name]
    for path in kept:
        target = target_root / path.relative_to(course_dir)
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def migrate_old_repo_folders(apply):
    '''Rename the old Py and R folders into the coursework tier and park the
    two partial uploads outside the repo so nothing is lost.'''
    notes = []
    for old_name, new_name in OLD_REPO_FOLDERS.items():
        old_path = REPO / old_name
        new_path = DEST / new_name
        if old_path.exists():
            notes.append(f'  {old_name}/  ->  coursework/{new_name}/')
            if apply:
                DEST.mkdir(parents=True, exist_ok=True)
                old_path.rename(new_path)
    for old_name in OLD_PARTIAL_UPLOADS:
        old_path = REPO / old_name
        if old_path.exists():
            notes.append(f'  {old_name}/  ->  {OLD_UPLOADS / old_name}  (outside the repo)')
            if apply:
                OLD_UPLOADS.mkdir(parents=True, exist_ok=True)
                old_path.rename(OLD_UPLOADS / old_name)
    return notes


def main():
    apply = '--apply' in sys.argv
    mode = 'APPLY' if apply else 'DRY RUN'
    print(f'🚀 Building coursework tier in {mode} mode')
    print(f'📂 Source: {SRC}')
    print(f'📦 Repo:   {REPO}')

    if not SRC.exists() or not REPO.exists():
        print('❌ Source or repo folder not found. Check the paths at the top of the script.')
        return

    lines = [f'Coursework build manifest ({mode})', '']
    total_kept = total_skipped = 0
    total_bytes = 0

    for code, folder_name in COURSES.items():
        course_dir = SRC / code
        if not course_dir.exists():
            print(f'⚠️  {code} not found in Coursework, skipping')
            continue
        kept, skipped = plan_course(course_dir)
        copy_kept(course_dir, kept, apply)
        kept_bytes = sum(p.stat().st_size for p in kept)
        total_kept += len(kept)
        total_skipped += len(skipped)
        total_bytes += kept_bytes
        print(f'✅ {code} -> coursework/{folder_name}: '
              f'{len(kept):,} kept ({kept_bytes / MB:,.1f} MB), {len(skipped):,} skipped')

        lines.append(f'{code} -> coursework/{folder_name}')
        lines.append(f'  KEPT ({len(kept):,} files, {kept_bytes / MB:,.1f} MB)')
        for p in kept:
            lines.append(f'    {p.relative_to(course_dir)}  ({p.stat().st_size / MB:,.2f} MB)')
        lines.append(f'  SKIPPED ({len(skipped):,} files)')
        for p, reason in skipped:
            lines.append(f'    {p.relative_to(course_dir)}  [{reason}]')
        lines.append('')

    notes = migrate_old_repo_folders(apply)
    if notes:
        print('🔀 Old repo folders:')
        for note in notes:
            print(note)
        lines.append('Old repo folders')
        lines.extend(notes)
        lines.append('')

    lines.append(f'TOTAL kept: {total_kept:,} files, {total_bytes / MB:,.1f} MB; '
                 f'skipped: {total_skipped:,} files')
    MANIFEST.write_text('\n'.join(lines), encoding='utf-8')

    print(f'📊 Total kept: {total_kept:,} files ({total_bytes / MB:,.1f} MB), '
          f'skipped: {total_skipped:,} files')
    print(f'📝 Manifest written to {MANIFEST}')
    if not apply:
        print('👀 Dry run only. Review the manifest, then rerun with --apply to copy.')
    else:
        print('🎉 Copy complete. Run git status in the repo to review before committing.')


if __name__ == '__main__':
    main()
