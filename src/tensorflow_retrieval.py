"""Optional TensorFlow retrieval extension.

The measured project pipeline is implemented with NumPy and pandas so it can run
in lightweight environments. This module documents the TensorFlow extension path
for environments where TensorFlow Recommenders is available.
"""

TENSORFLOW_RETRIEVAL_PLAN = {
    "user_tower": "embed user ids and optional user history/context features",
    "item_tower": "embed item ids and item metadata features",
    "retrieval_task": "train with sampled softmax or retrieval loss",
    "serving": "export item embeddings for approximate nearest-neighbor search",
    "evaluation": "compare Recall@K and NDCG@K against the lightweight models",
}
