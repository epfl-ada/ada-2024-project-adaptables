from tqdm import tqdm
import numpy as np
import gensim.downloader as api
import pickle as pkl
from itertools import chain

class TopicSummarizer:
    def __init__(self, embedding_model: str = 'glove-wiki-gigaword-100',lessen_words: set[str]|None = None,reduction_factor: float = 0.1):
        """
        Initialize the topic summarizer with a pre-trained word embedding model.
        
        Args:
            embedding_model (str): Name of the embedding model to use.
                Default is 'glove-wiki-gigaword-100'.
            lessen_words (set[str]|none): set of words whose weight should be reduced, by a `reduction_factor`
        """
        try:
            self.model = api.load(embedding_model)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            print("Falling back to a simpler model.")
            self.model = api.load('glove-wiki-gigaword-50')
        
        assert 0 <= reduction_factor and reduction_factor <= 1
        self.lessen_words = lessen_words
        self.reduction_factor = reduction_factor
        
    def _get_topic_vector(self, topics: list[tuple[str, float]]) -> np.ndarray:
        """
        Create a weighted average vector for the topics.
        
        Args:
            topics (list[tuple[str, float]]): list of topics with their weights.
        
        Returns:
            np.ndarray: Weighted average vector representing the topics.
        """
        vectors = []
        total_weight = 0
        
        for topic, weight in topics:
            try:
                # Ensure topic is in lowercase and in the model's vocabulary
                topic = topic.lower()
                w_to_use = weight
                if self.lessen_words is not None and topic in self.lessen_words:
                    w_to_use *= self.reduction_factor
                if topic in self.model.key_to_index:
                    vectors.append(self.model[topic] * w_to_use)
                    total_weight += w_to_use
            except KeyError:
                continue
        
        if not vectors:
            raise ValueError(f"No valid topic vectors found for topics, {topics}")
        
        return np.sum(vectors, axis=0) / total_weight
    
    def _find_most_similar_words(
        self, 
        topic_vector: np.ndarray | list[str], 
        k: int = 2, 
        exclude_words: list[str] = None,
        weighted = True
    ) -> list[str]:
        """
        Find K most similar words to the topic vector.
        
        Args:
            topic_vector (np.ndarray): Vector representing the topics.
                    or   (list[str]) iff weighted == false: a list of all topics to (equally) consider 
            k (int): Number of words to return.
            exclude_words (list[str]): Words to exclude from results.
        
        Returns:
            list[str]: K most similar words.
        """
        if len(topic_vector) == 0:
            return ["unknown"] * k
        assert (weighted and isinstance(topic_vector,np.ndarray)) or (not weighted and isinstance(topic_vector,list) and isinstance(topic_vector[0],str))

        exclude_words = exclude_words or []
        
        # Find most similar words, excluding specified words
        candidates = []
        for word, cos_sim in self.model.most_similar(positive=[topic_vector] if weighted else topic_vector, topn=k+len(exclude_words)):
            if word not in exclude_words:
                candidates.append((word,cos_sim))
                if len(candidates) == k:
                    break
        
        return candidates
    
    def summarize_topics(
        self, 
        corpus: list[list[tuple[str, float]]], 
        k: int = 2,
        weighted = True,
        use_tqdm = True
    ) -> list[list[str|float]]:
        """
        Summarize topics for an entire corpus.
        
        Args:
            corpus (list[list[tuple[str, float]]]): Corpus of topic lists.
            k (int): Number of summary words per topic list.
        
        Returns:
            list[list[str]]: Summary words for each topic list.
        """
        summaries = []
        for topics in (tqdm(corpus,desc="Finding topics",total=len(corpus)) if use_tqdm else corpus):
            topic_vector = self._get_topic_vector(topics) if weighted else [topic_tpl[0] for topic_tpl in topics]
            summary = self._find_most_similar_words(topic_vector, k,weighted=weighted)
            summaries.append(summary)
            
        return summaries
    

if __name__ == '__main__':
    with open("victor_rt_kw.pkl","rb") as f:
        kw = pkl.load(f)
    with open("rt_scapy_parsed.pkl","rb") as f:
        rt_scapy_parsed = pkl.load(f)

    np_words = [[noun for noun,pos in doc_tpl if pos == "VERB" or pos == "NOUN" or pos == "ADJ"] for doc_tpl in rt_scapy_parsed]

    srtnp = set(chain.from_iterable(np_words))
    bad_words = [[noun for noun,pos in doc_tpl if noun not in srtnp and pos != "PUNCT"] for doc_tpl in rt_scapy_parsed]
    sbw = set(chain.from_iterable(bad_words))
    lessen_summarizer = TopicSummarizer(lessen_words=sbw,reduction_factor=0.1)
    if srtnp:
        del srtnp
    if bad_words:
        del bad_words
    if np_words:
        del np_words

    rt_lessen_topicized = lessen_summarizer.summarize_topics(kw,k=5,weighted=True,use_tqdm=True)
    with open("rt_summarized.pkl","wb") as f:
        pkl.dump(rt_lessen_topicized,f,pkl.HIGHEST_PROTOCOL)