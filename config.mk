ENV_NAME=bulkhours_py3.10
PROJECT_NAME=bulkhours
SCRIPT:bulkhours-correct=bulkhours.core.evaluation:dump_corrections
SCRIPT:bulkhours-boids=bulkhours.boids.simulation:main
SCRIPT:bulkhours-git-push=bulkhours.core:git_push
