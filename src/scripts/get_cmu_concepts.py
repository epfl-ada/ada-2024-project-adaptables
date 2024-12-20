from ..models.keybert_model import KeyBERT
import pickle as pkl
from src.utils.data_utils import *
from src.utils.general_utils import *

RAW_DATA_FOLDER = "data/raw/"
CMU_PLOTS_DS = ProjectDataset(RAW_DATA_FOLDER+"plot_summaries.txt",
                              "CMU plots",
                              "Base dataset for ADA. Contains a plot summary for each of the movie in the CMU Movies dataset",
                              {
                                  "wikipedia_id":"The UID corresponding to the movie",
                                  "plot": "The (summarized) plot of the movie"
                              })


if __name__ == '__main__':
    with open("nlped_tot.pkl","rb") as f:
        scapy_parsed_plots = pkl.load(f)

    all_docs = CMU_PLOTS_DS.df["plot"].values
    np_words = [[noun for noun,pos in doc_tpl if pos == "VERB" or pos == "NOUN" or pos == "ADJ"] for doc_tpl in scapy_parsed_plots]
    model = KeyBERT(model="all-MiniLM-L12-v2")
    kw = model.extract_keywords(all_docs,seed_keywords=np_words,top_n=50,use_tqdm=True,model_encode_kwargs={"batch_size":512,"device":"cuda"})