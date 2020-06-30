import numpy as np
import tensorflow_hub as hub

# TODO: download the model in the dockerfile so embed.py doesn't have to do it
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

embeddings = embed([
    "How old are you?", 
    "What is you age?",
    "My phone is good.",
    "Your cellphone looks great",
    "I am a sentence for which I would like to get its embedding"
])

print(np.corrcoef(np.array(embeddings)))
