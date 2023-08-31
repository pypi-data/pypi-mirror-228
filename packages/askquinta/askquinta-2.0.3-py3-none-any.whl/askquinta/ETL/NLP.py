import uuid
import hashlib
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.metrics import jaccard_distance, edit_distance
from jellyfish import jaro_winkler_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
import base64
from nltk.stem import PorterStemmer, WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from textblob import TextBlob

class About_NLP:
    """
      A class for various Natural Language Processing tasks 
    """
    def generate_uuid(self, text):
        """
        Generate a UUID based on the input text.

        Parameters:
            text (str): The input text used to generate the UUID.

        Returns:
            str: The generated UUID.
        """
        unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
        return unique_id

    def summarize_text(self, text, ratio=0.2):
        from gensim.summarization import summarize #using version==3.6.0
        """
        Summarize news text using the TextRank algorithm.
        
        Args:
            text (str): The input news text to be summarized.
            ratio (float): The ratio of sentences to be included in the summary.
            
        Returns:
            str: The summarized news text.
        """
        summarized_text = summarize(text, ratio=ratio)
        return summarized_text
    


    def clean_text(self, text, remove_punctuation=False,remove_number=False, 
                   remove_stopwords=False, apply_stemming=False, 
                   apply_lemmatization=False, language='english'):
        """
        Clean and preprocess text.

        Parameters:
            text (str): The input text to be cleaned.
            remove_punctuation (bool): Whether to remove punctuation from the text.
            remove_stopwords (bool): Whether to remove stopwords from the text.
            apply_stemming (bool): Whether to apply stemming to the words.
            apply_lemmatization (bool): Whether to apply lemmatization to the words.
            language (str): The language of the text ('english' or 'indonesia').

        Returns:
            str: The cleaned and preprocessed text.
        """
        cleaned_text = text.strip().lower()

        if remove_number:
            cleaned_text = re.sub(r'[\d]', '', cleaned_text)  # Remove punctuation
            
        if remove_punctuation:
            cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuation

        if remove_stopwords:
            if language == 'english':
                stop_words = set(stopwords.words('english'))
            elif language == 'indonesia':
                stop_words = set(stopwords.words('indonesia'))
            words = word_tokenize(cleaned_text)
            words = [word for word in words if word not in stop_words]
            cleaned_text = ' '.join(words)
        
        if apply_stemming:
            if language == 'english':
                stemmer = PorterStemmer()
                words = word_tokenize(cleaned_text)
                stemmed_words = [stemmer.stem(word) for word in words]
                cleaned_text = ' '.join(stemmed_words)
            elif language == 'indonesia':
                stemmer_factory = StemmerFactory()
                stemmer = stemmer_factory.create_stemmer()
                cleaned_text = stemmer.stem(cleaned_text)

        if apply_lemmatization:
            lemmatizer = WordNetLemmatizer()
            words = word_tokenize(cleaned_text)
            lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
            cleaned_text = ' '.join(lemmatized_words)

        #fix multiple space
        cleaned_text = ' '.join(cleaned_text.split())
        
        return cleaned_text
    
    def hash_value(self, text, algorithm='sha256'):
        """
        Hash a value using the specified algorithm.

        Parameters:
            text (str): The input value to be hashed.
            algorithm (str): The hashing algorithm to use (default is 'sha256').

        Returns:
            str: The hashed value.
        
        Raises:
            ValueError: If the specified algorithm is not supported.
        """
        if algorithm not in hashlib.algorithms_available:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode('utf-8'))
        return hasher.hexdigest()

    def verify_hash(self, text, hashed_value, algorithm='sha256'):
        """
        Verify if a value matches a hashed value using the specified algorithm.

        Parameters:
            value (str): The input value to be verified.
            hashed_value (str): The hashed value to compare against.
            algorithm (str): The hashing algorithm used (default is 'sha256').

        Returns:
            bool: True if the value matches the hashed value, False otherwise.
        """
        return self.hash_value(text, algorithm) == hashed_value

    def encode_base64(self, value):
        """
        Encode a value using Base64 encoding.

        Parameters:
            value (str): The input value to be encoded.

        Returns:
            str: The encoded value.
        """
        encoded_bytes = base64.b64encode(value.encode('utf-8'))
        encoded_value = encoded_bytes.decode('utf-8')
        return encoded_value

    def decode_base64(self, encoded_value):
        """
        Decode a value from Base64 encoding.

        Parameters:
            encoded_value (str): The input encoded value to be decoded.

        Returns:
            str: The decoded value.
        """
        decoded_bytes = base64.b64decode(encoded_value.encode('utf-8'))
        decoded_value = decoded_bytes.decode('utf-8')
        return decoded_value

    def similarity_text_scoring(self, text1, text2, similarity_metric='jaccard'):
        """
        Calculate similarity between two texts using the specified similarity metric.

        Parameters:
            text1 (str): The first text for comparison.
            text2 (str): The second text for comparison.
            similarity_metric (str): The similarity metric to use:
                - 'jaccard': Jaccard similarity coefficient.
                - 'edit': Edit distance similarity (1.0 minus normalized edit distance).
                - 'cosine': Cosine similarity using TF-IDF vectors.
                - 'levenshtein': Levenshtein similarity (1.0 minus normalized Levenshtein distance).
                - 'jarowinkler': Jaro-Winkler similarity.
                - 'tfidf_cosine': Cosine similarity using TF-IDF vectors (sklearn's implementation).

        Returns:
            float: The similarity score.
        
        Raises:
            ValueError: If the specified similarity metric is not supported.
        """
        text1 = self.clean_text(text1, remove_punctuation=True)
        text2 = self.clean_text(text2, remove_punctuation=True)

        if similarity_metric == 'jaccard':
            words1 = set(word_tokenize(text1))
            words2 = set(word_tokenize(text2))
            similarity_score = 1.0 - jaccard_distance(words1, words2)
        elif similarity_metric == 'edit':
            words1 = word_tokenize(text1)
            words2 = word_tokenize(text2)
            max_length = max(len(words1), len(words2))
            similarity_score = 1.0 - edit_distance(words1, words2) / max_length
        elif similarity_metric == 'cosine':
            vectorizer = CountVectorizer().fit_transform([text1, text2])
            vectors = vectorizer.toarray()
            cosine_sim = cosine_similarity(vectors)[0][1]
            similarity_score = cosine_sim
        elif similarity_metric == 'levenshtein':
            distance = self.calculate_levenshtein_distance(text1, text2)
            max_length = max(len(text1), len(text2))
            similarity_score = 1.0 - distance / max_length
        elif similarity_metric == 'tfidf_cosine':
            similarity_score = self.calculate_tfidf_cosine_similarity(text1, text2)
        elif similarity_metric == 'jarowinkler':
            similarity_score = self.calculate_jaro_winkler_similarity(text1, text2)
        else:
            raise ValueError(f"Unsupported similarity metric: {similarity_metric}")

        return similarity_score

    def calculate_levenshtein_distance(self, s1, s2):
        """
        Calculate the Levenshtein Distance between two strings.

        Parameters:
            s1 (str): The first string.
            s2 (str): The second string.

        Returns:
            int: The Levenshtein Distance.
        """
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for index2, char2 in enumerate(s2):
            new_distances = [index2 + 1]
            for index1, char1 in enumerate(s1):
                if char1 == char2:
                    new_distances.append(distances[index1])
                else:
                    new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
            distances = new_distances

        return distances[-1]

    def calculate_tfidf_cosine_similarity(self, text1, text2):
        """
        Calculate TF-IDF Cosine Similarity between two texts.

        Parameters:
            text1 (str): The first text.
            text2 (str): The second text.

        Returns:
            float: The TF-IDF Cosine Similarity score.
        """
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)[0][1]
        return cosine_sim
    
    def calculate_jaro_winkler_similarity(self, s1, s2):
        """
        Calculate Jaro-Winkler Similarity between two strings.

        Parameters:
            s1 (str): The first string.
            s2 (str): The second string.

        Returns:
            float: The Jaro-Winkler Similarity score.
        """
        jaro_winkler_sim = jaro_winkler_similarity(s1, s2)
        return jaro_winkler_sim

    def translate(self, text,source_language = 'en', target_language = 'id'):
        """
        Translate a text to the target language.
        
        Parameters:
            text (str): Text to be translated.
            source_language (str, default en as english) : The source language code to translate the text to. 
            target_language (str, default id as indonesia): The target language code to translate the text to. 
        
        Returns:
            Str: Translated text.
        """
        blob = TextBlob(text)
        translated_text = blob.translate(from_lang = source_language, to=target_language)
        return str(translated_text)
    
    def sentiment(self, text):
        """
        Predict the sentiment label of a given text.
        
        Parameters:
            text (str): The text for sentiment prediction.
        
        Returns:
            str: The predicted sentiment label ('positive', 'negative', or 'neutral').
        """
        blob = TextBlob(text)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        if polarity > 0:
            sentiment_label = 'positive'
        elif polarity < 0:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        return sentiment_label
