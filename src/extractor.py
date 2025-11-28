import spacy

class ClaimExtractor:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("Please run: python -m spacy download en_core_web_sm")

    def extract_metadata(self, text):
        """
        Extracts Named Entities to display to the user or boost retrieval.
        """
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        
        return {
            "original_text": text,
            "entities": entities,
            "keywords": keywords
        }
