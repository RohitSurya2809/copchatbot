import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from datetime import datetime

class PoliceAssistanceChatbot:
    def __init__(self):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cache_file = os.path.join(root_dir, 'chatbot_cache.json')
        self.load_and_preprocess_data()
        
    def load_and_preprocess_data(self):
        # Get the project root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(root_dir, 'Police_Assistance_Excel.csv')
        
        # Try to load from cache first
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    if self._is_cache_valid(cache_data):
                        self._load_from_cache(cache_data)
                        return
            except Exception as e:
                print(f"Error loading cache: {str(e)}")
        
        try:
            # Load from CSV if cache is invalid or doesn't exist
            self.df = pd.read_csv(csv_path)
            self.categories = self.df['Category'].unique()
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Question'].astype(str))
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise RuntimeError("Failed to load required data. Please ensure the data file exists and is accessible.")
        
        # Create and save cache
        self._create_cache()
    
    def _is_cache_valid(self, cache_data):
        # Check if cache is from today
        cache_date = datetime.strptime(cache_data['created_at'], '%Y-%m-%d').date()
        return cache_date == datetime.now().date()
    
    def _load_from_cache(self, cache_data):
        self.df = pd.DataFrame(cache_data['data'])
        self.categories = self.df['Category'].unique()
        self.vectorizer = TfidfVectorizer(vocabulary=cache_data['vocabulary'])
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Question'].astype(str))
    
    def _create_cache(self):
        cache_data = {
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'data': self.df.to_dict('records'),
            'vocabulary': self.vectorizer.vocabulary_
        }
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"Error creating cache: {str(e)}")
            # Continue without cache - not critical
    
    def get_response(self, user_input):
        if not hasattr(self, 'vectorizer') or not hasattr(self, 'tfidf_matrix'):
            return "I apologize, but I'm currently experiencing technical difficulties. Please try again later."
            
        try:
            # Transform user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate similarity scores
            similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
            
            # Get top 3 similar questions
            top_indices = similarities.argsort()[-3:][::-1]
            
            # Filter responses with similarity score above threshold
            threshold = 0.3
            valid_responses = [(i, similarities[i]) for i in top_indices if similarities[i] > threshold]
            
            if not valid_responses:
                return "I apologize, but I couldn't find a specific answer to your question. Please try rephrasing your question or contact your local police station for more detailed information."
            
            # Get the best matching response
            best_idx = valid_responses[0][0]
            response = self.df.iloc[best_idx]['Answer']
            category = self.df.iloc[best_idx]['Category']
            
            # Format response with category
            formatted_response = f"Category: {category}\n\n{response}"
            
            return formatted_response
            
        except Exception as e:
            return "I apologize, but I'm currently experiencing technical difficulties. Please try again later or visit your nearest police station for assistance."
