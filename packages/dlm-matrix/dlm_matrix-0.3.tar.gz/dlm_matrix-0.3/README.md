# Divergent Language Matrix

## Description
The Divergent Language Matrix is a novel approach designed to analyze and understand the intricate structures and dynamics within digital conversations. This repository contains the code and documentation necessary to implement the Divergent Language Matrix framework, allowing you to explore conversations in a new and comprehensive way.

## Introduction
In the realm of digital communication, understanding conversations goes beyond the surface-level exchange of messages. The Divergent Language Matrix framework recognizes conversations as dynamic systems, governed by evolving production rules that shape their evolution. This approach provides a deeper insight into the complexities of conversations by considering various factors such as semantic content, contextual embeddings, and hierarchical relationships.

## Formulation
Divergent Language Matrix (DLM) is designed to generate a lower-dimensional representation of complex, hierarchical text data, such as conversations. The algorithm preserves both semantic and structural relationships within the data, allowing for more efficient analysis and visualization. 

1. Text Preprocessing and Conversion to Parts:
    * Split each message 𝑀ᵢⱼ into smaller parts: 𝑃ᵢⱼ = {𝑃ᵢⱼ₁, 𝑃ᵢⱼ₂, ..., 𝑃ᵢⱼₖ}.
    * Maintain the order and relationships between the parts.

2. Creating Contextual Embeddings with Transformers:
    * For each part 𝑃ᵢⱼₖ, compute its contextual embedding using a transformer model: 𝐸(𝑃ᵢⱼₖ).

3. Construct Multi-level Hierarchical Representation:
    * Assign coordinates (𝑥, 𝑦, 𝑧, 𝑡) to each part 𝑃ᵢⱼₖ within its conversation 𝐶ᵢ.
    * Derive 𝑥, 𝑦, and 𝑧 coordinates, capturing part's position among parent and sibling parts.
    * Update the 𝑡 coordinate based on the temporal order of parts.

4. Dynamic Message Ordering:
    * Order the parts within each conversation 𝐶ᵢ based on contextual similarity or attention weights: 𝑂(𝑃ᵢⱼ).

5. Dimensionality Reduction with UMAP:
    * Create a joint representation by combining the contextual embeddings and hierarchical coordinates of the parts within each conversation 𝐶ᵢ.
    * Apply UMAP to reduce the dimensionality of the joint representation while preserving semantic and structural relationships.

6. Clustering and Final Representation:
    * Utilize advanced clustering techniques, such as HDBSCAN, on the reduced-dimensional representation.
    * Form clusters based on contextual embeddings and hierarchical representation to organize parts into coherent conversations.
    * Group similar parts together to capture thematic similarities and facilitate analysis.

