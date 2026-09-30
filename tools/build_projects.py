'''
build_projects.py

Carves the showcase projects out of coursework/ into projects/<ProjectName>/
using git mv, so history follows each file. Primary notebooks and papers get
clean, subject-based names; figures and data keep their original names because
the notebooks reference them by name.

Run from the repo root (C:\\Users\\slimt\\DataSciencePortfolio):
    python build_projects.py            dry run: prints every move, changes nothing
    python build_projects.py --apply    performs the git mv commands
'''

import fnmatch
import subprocess
import sys
from pathlib import Path

REPO = Path.cwd()
COURSEWORK = REPO / 'coursework'
PROJECTS = REPO / 'projects'

CW = {
    'DSC530': 'DataExplorationAndAnalysis',
    'DSC540': 'DataPreparation',
    'DSC550': 'DataMining',
    'DSC630': 'PredictiveAnalytics',
    'DSC640': 'DataPresentationAndVisualization',
}

# Each project: source course folder, then (pattern, new name or None to keep the name).
PROJECT_MOVES = {
    'JobPostingFraudClassifier': ('DSC630', [
        ('TimHollis_FinalProjectEx11.2_DSC630.ipynb', 'fraud_classifier_final.ipynb'),
        ('TimHollis_FinalProjectEx11.2_DSC630.docx', 'fraud_classifier_paper.docx'),
        ('TimHollis_FinalProjectEx11.2_DSC630.pptx', 'fraud_classifier_presentation.pptx'),
        ('TimHollis_MS3Viz_DSC630.ipynb', 'milestone3_eda_visuals.ipynb'),
        ('TimHollis_MS4_DSC630.ipynb', 'milestone4_modeling.ipynb'),
        ('TimHollis_DSC630_Milestone1.docx', 'milestone1_proposal.docx'),
        ('TimHollis_DSC630_Milestone2.docx', 'milestone2_data_selection.docx'),
        ('TimHollis_DSC630_Milestone2-3.docx', 'milestone2-3_eda_report.docx'),
        ('TimHollis_DSC630_Milestone4.docx', 'milestone4_report.docx'),
        ('TimHollis_DSC630_Milestone4_NewContent.docx', 'milestone4_report_addendum.docx'),
        ('graph1_class_balance.png', None), ('graph1_desc_length.png', None),
        ('graph2_desc_*.png', None), ('graph2_fraud_by_experience.png', None),
        ('graph2_logo.png', None), ('graph2_missing_values.png', None),
        ('graph3_*.png', None), ('graph4_*.png', None),
        ('lr_*.png', None), ('rf_*.png', None),
    ]),
    'BillboardHitPrediction': ('DSC550', [
        ('TimHollis_TermProjectFinalEx11.3_DSC550.ipynb', 'billboard_hit_prediction_final.ipynb'),
        ('TimHollis_TermProjectFinalEx11.3_DSC550.docx', 'billboard_hit_prediction_paper.docx'),
        ('TimHollis_TermProjectFinal_Writeup_DSC550_Polished.docx', 'final_writeup.docx'),
        ('TimHollis_TermProjectFinal_Writeup_DSC550.docx', 'final_writeup_draft.docx'),
        ('TimHollis_TermProjectEx10.2_DSC550.ipynb', 'milestone_modeling.ipynb'),
        ('Term project.docx', 'project_proposal.docx'),
        ('BBHot100.csv', None),
        ('graph*.png', None), ('confusion_matrix.png', None),
        ('correlation_heatmap.png', None), ('feature_importance.png', None),
        ('roc_curve.png', None),
    ]),
    'CityLivabilityDataPipeline': ('DSC540', [
        ('HollisT_Milestone5_DSC540.ipynb', 'city_livability_pipeline.ipynb'),
        ('HollisT_Milestone5_DSC540.db', 'city_livability.db'),
        ('DSC540_HollisT_TermProject.ipynb', 'term_project_notebook.ipynb'),
        ('DSC540_HollisT_Milestone1.docx', 'milestone1_proposal.docx'),
        ('Vizuals.pbix', 'city_livability_dashboard.pbix'),
        ('Viz*.png', None), ('hud_*.csv', None), ('merged_*.csv', None),
        ('bedroom_summary.csv', None), ('qol_ranked.csv', None),
        ('background.webp', None), ('globe.webp', None),
    ]),
    'ChildcareAffordabilityTexas': ('DSC640', [
        ('TimHollis_TermProject_DSC640.ipynb', 'childcare_affordability_story.ipynb'),
        ('TimHollis_Milestone1_DSC640.ipynb', 'milestone1_findings.ipynb'),
        ('TimHollis_Milestone2_DSC640.ipynb', 'milestone2_visuals.ipynb'),
        ('TimHollis_Milestone3_DSC640.ipynb', 'milestone3_mockups.ipynb'),
        ('TimHollis_Milestone4_DSC640.ipynb', 'milestone4_review.ipynb'),
        ('viz_parcoords_childcare_tx.png', None),
    ]),
    'RetailSalesForecasting': ('DSC630', [
        ('TimHollis_Ex8.2_DSC630.ipynb', 'retail_sales_forecasting.ipynb'),
        ('us_retail_sales.csv', None), ('retail_sales_*.png', None),
        ('residual_plot.png', None), ('sarima_comparison.png', None),
    ]),
    'AirlineComplaintsAnalysis': ('DSC640', [
        ('TimHollis_Wk9&10_DSC640.ipynb', 'airline_complaints_analysis.ipynb'),
        ('complaints-by-airport.csv', None), ('iata-icao.csv', None),
        ('figures', None),
    ]),
    'HybridMovieRecommender': ('DSC630', [
        ('TimHollis_Ex10.2_DSC630.ipynb', 'hybrid_movie_recommender.ipynb'),
        ('ml-latest-small', None),
    ]),
}


def git_mv(src, dest, apply):
    '''Run git mv, or just print it in dry-run mode.'''
    rel_src = src.relative_to(REPO)
    rel_dest = dest.relative_to(REPO)
    print(f'   {rel_src}  ->  {rel_dest}')
    if apply:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'mv', str(rel_src), str(rel_dest)], check=True)


def resolve(course_dir, pattern):
    '''Return the paths in course_dir matching a filename or glob pattern.'''
    return sorted(p for p in course_dir.iterdir() if fnmatch.fnmatch(p.name, pattern))


def main():
    apply = '--apply' in sys.argv
    mode = 'APPLY' if apply else 'DRY RUN'
    print(f'🚀 Building projects tier in {mode} mode from {REPO}')
    if not COURSEWORK.exists() or not (REPO / '.git').exists():
        print('❌ Run this from the repo root (the folder that contains coursework/ and .git).')
        return

    moved = missing = 0
    for project, (code, patterns) in PROJECT_MOVES.items():
        course_dir = COURSEWORK / CW[code]
        target_dir = PROJECTS / project
        print(f'\n📁 projects/{project}  (from coursework/{CW[code]})')
        for pattern, new_name in patterns:
            matches = resolve(course_dir, pattern)
            if not matches:
                print(f'   ⚠️  no match for {pattern}')
                missing += 1
                continue
            for src in matches:
                dest = target_dir / (new_name or src.name)
                git_mv(src, dest, apply)
                moved += 1

    print(f'\n📊 {moved:,} moves planned, {missing:,} patterns unmatched')
    if apply:
        print('🎉 Done. Run git status to review, then commit.')
    else:
        print('👀 Dry run only. Rerun with --apply to perform the moves.')


if __name__ == '__main__':
    main()
