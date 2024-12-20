# Pre-processed data

This folder contains some of the pre-processed data.
Use the table hereunder to find, for each file in this directory, which of the python scripts under `src/scripts` was used to generate the data file, if you would want to recreate it yourself.
Most of these are loaded in the global `ExtraDatasetInfo` object (see `src/utils/data_utils.py`).


| File (name)               | Script (name)                                                                           | File (data) description                                                                               | Notes/Requirements   |
|---------------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|----------------------|
| reviews_with_compound.csv | TODO.py                                                                                 | The Massive Rotten Tomatoes dataset, extended by performing VADER sentiment analysis on the reviews.  | ~12GB RAM, 10minutes |
| ratings_expert.csv        | This comes from the pre-processing in Milestone 2, section II., `list_movie` variable.  | The movies from CMU, which also appear in the RT datasets and have (at least one) expert rating.      |  /                   |
|                           |                                                                                         |                                                                                                       |                      |
|                           |                                                                                         |                                                                                                       |                      |
|                           |                                                                                         |                                                                                                       |                      |
|                           |                                                                                         |                                                                                                       |                      |
|                           |                                                                                         |                                                                                                       |                      |