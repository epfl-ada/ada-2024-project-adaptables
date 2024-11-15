
# A comedy handbook

## Team

ADAptables :

Arthur Removille, Caroline Verchère, Quentin Gallien, Théo Le Blan, Victor Garvalov

## Project presentation - Abstract
Laughter. This great human sentiment that surrounds us from a very early age is a crucial aspect in cinematography and even has its own genre associated – comedies. Do you remember chuckling at the latest Hangover ? Do you also remember being bored out of your mind when watching The Emoji Movie ? Both movies are comedies, yet one was much “better” than the other. In this project, we aim to determine what factors make for a great comedy in order to better understand this phenomenon. We will explore four main aspects, namely what makes a movie popular, what makes it qualitative, whether there are cultural aspects influencing this, and to what extent are each of these factors unique to our genre of interest.


## Repository presentation

In this repository, you will find all the code and data for our project.

## Quickstart

```bash
# clone project
git clone git@github.com:epfl-ada/ada-2024-project-adaptables.git
cd ada-2024-project-adaptables

# [OPTIONAL] create conda environment
# conda create -n <env_name> python=3.11 or ...
# conda activate <env_name>

# [OR, OPTIONAL] create venv
python3 -m venv venv
source venv/bin/activate        # POSIX (Linux, MAC ; bash)
# venv/Scripts/activate.bat     # Windows (cmd)
# venv/Scripts/Activate.ps1     # Windows (PS)

# install requirements
pip install -r pip_requirements.txt
```

## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Datasets
│   ├── raw                             <- raw files (for subset of smaller datasets)
│   ├── cleaned                         <- cleaned/pre-processed datasets
│
├── src                         <- Source code
│   ├── data                            <- Dataloaders/datamodules code 
│   ├── models                          <- Model directory (unused for now)
│   ├── utils                           <- Utility directory (unused for now)
│   ├── scripts                         <- Shell scripts (unused for now)
│
├── tests                       <- Various tests (unused for now)
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

**Important note!**

One of the additional datasets we are using is too large to be hosted on Git, and we cannot use Git LFS as the repository is tied to one owner - the organization. As such, please download it manually from here, and place the `rotten_tomatoes_movie_reviews.csv` under `data/raw/` 