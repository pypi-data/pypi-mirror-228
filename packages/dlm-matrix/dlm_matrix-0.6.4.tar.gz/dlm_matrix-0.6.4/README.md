# Divergent Language Matrix

## Description
The Divergent Language Matrix is a novel approach designed to analyze and understand the intricate structures and dynamics within digital conversations. This repository contains the code and documentation necessary to implement the Divergent Language Matrix framework, allowing you to explore conversations in a new and comprehensive way.

## Introduction
In the realm of digital communication, understanding conversations goes beyond the surface-level exchange of messages. The Divergent Language Matrix framework recognizes conversations as dynamic systems, governed by evolving production rules that shape their evolution. This approach provides a deeper insight into the complexities of conversations by considering various factors such as semantic content, contextual embeddings, and hierarchical relationships.

## Formulation
Divergent Language Matrix (DLM) is designed to generate a lower-dimensional representation of complex, hierarchical text data, such as conversations. The algorithm preserves both semantic and structural relationships within the data, allowing for more efficient analysis and visualization.

In the Divergent Language Matrix (DLM) framework, a conversation tree `T` is formulated as a directed, acyclic graph where each node corresponds to a message in the conversation. Each message `t_i` is mathematically defined by a triplet `(d_i, s_i, c_i)`, such that:

* x_coord (Depth): Represents the hierarchical level of a message. If a message is a direct reply to another message, it will be one level deeper (e.g., the original message is at depth 0, a reply to it is at depth 1, a reply to that reply is at depth 2, and so on).

* y_coord (Order among siblings): Represents the order in which a message appears among its siblings. This is relevant when there are multiple replies (siblings) to a single message. It provides a sense of the sequence of the conversation.

* z_coord (Homogeneity based on sibling count): This is the most direct measure of homogeneity in the provided method. Messages that have no siblings (i.e., are the only reply to their parent message) are given a z-coordinate of 0. Conversely, if there are multiple sibling messages, they're assigned a z-value based on the formula −0.5 × ( total number of siblings − 1) −0.5 × (total number of siblings−1). 
In this scheme:
    * Isolated Messages (Zero Siblings): Messages that are the only replies to their parent have a natural Z-Coordinate of 0 in the sibling_spacing calculation. This assignment implies that these messages are unique in their context and, therefore, do not require differentiation based on sibling relationships.
    * Messages that are part of a set of siblings will have the same z value, marking them as part of the same homogeneous group at that depth level.

## Processing Stages

1. **Text Preprocessing and Segmentation**:  
   - Each message `M_{i,j}` is tokenized and segmented into `k` distinct parts: `P_{i,j} = {P_{i,j,1}, P_{i,j,2}, ..., P_{i,j,k}}`.
   - Syntactic and semantic relations are maintained among these segmented parts, laying the groundwork for in-depth analysis.

2. **Creating Contextual Embeddings with Sentence Transformers**:  
   - We employ Sentence Transformers to generate high-quality, contextual embeddings for each text to create high-dimensional contextual embeddings `E(P_{i,j,k})` for each part.

### 3. Hierarchical Spatial-Temporal Coordinate Assignment

The assignment of hierarchical spatial-temporal coordinates is a cornerstone in the DLM framework, bridging the gap between high-dimensional textual embeddings and the structured representation of a conversation. It assigns each segment a four-dimensional coordinate `(x, y, z, t)`, encoding both its place in the conversational hierarchy and its chronological order.

#### 3.1. The Framework for Coordinate Assignment

- **The Coordinate Tuple**: Every segment `P_{i,j,k}` within a given conversation `C_i` is mapped to a unique coordinate tuple `(x_{i,j,k}, y_{i,j,k}, z_{i,j,k}, t_{i,j,k})`.
- **Rooted in Message Metadata**: The values of `x, y, z` are computed as functions `f(d_i, s_i, c_i)`, where `d_i, s_i, c_i` are as previously defined. 
- **Chronological Timestamp**: `t_{i,j,k}` is defined by the temporal metadata associated with the message, normalized to a suitable scale for analysis.

#### 3.2. Spatial Coordinate Calculations

- **X-Axis (Thread Depth)**: `x_{i,j,k}` is directly proportional to `d_i`, representing the depth of the message in the conversation tree. It captures the level of nesting for each message.
  
  `x_{i,j,k} = f_x(d_i)`
  
- **Y-Axis (Sibling Order)**: `y_{i,j,k}` is a function of `s_i`, signifying the message's ordinal position among siblings.
  
  `y_{i,j,k} = f_y(s_i)`
  
- **Z-Axis (Sibling Density)**: `z_{i,j,k}` encapsulates the density of sibling messages at a given depth, calculated as a function of `c_i`.
  
  `z_{i,j,k} = f_z(c_i)`
  
These functions `f_x, f_y, f_z` can be linear or nonlinear mappings based on the specific requirements of the analysis.

#### 3.3. Temporal Coordinate Calculations

- **Timestamp Normalization**: The timestamp `t` for each message is normalized into a unit scale ranging from 0 to 1 across the entire conversation.
  
  `t_{i,j,k} = (Timestamp of P_{i,j,k} - Min Timestamp) / (Max Timestamp - Min Timestamp)`
  
#### 3.4. Final Coordinate Assignment

After calculating these coordinates, each segment `P_{i,j,k}` in conversation `C_i` will have a unique 4D coordinate `(x_{i,j,k}, y_{i,j,k}, z_{i,j,k}, t_{i,j,k})`. These coordinates serve as a comprehensive representation of each segment's position in both the conversational hierarchy and the temporal sequence.

### 4. Dynamic Message Ordering (DMO)

The Dynamic Message Ordering (DMO) system utilizes a Hierarchical Spatial-Temporal Coordinate Assignment methodology to arrange messages in a conversation space. In essence, the DMO aims to spatially organize messages in such a way that:

- Similar messages are closer in this space.
- The spatial relationship of messages reflects the temporal relationship among them.
- The hierarchical structure is reflected in the spatial coordinates.

#### 4.1. Spacing Calculation (Method: `calculate_spacing`)

In this part, the spacing `S` between siblings based on similarity scores is of utmost importance. Let's redefine the mathematical formulation with more specificity:

- **Variable Definitions:**
  - `n = Number of children, n = | children_ids |`
  - `avg_similarity = Average of normalized similarity scores, (Sum(s_i) from i=1 to n) / n`
  - `s_i = Individual normalized similarity scores`

- **Mathematical Representation:**

`S(n, avg_similarity, method) = { 0 if n <= 1; -0.5 x (n - 1) if method = "spacing"; (-0.5 + avg_similarity) x (n - 1) if method = "both" }`

#### 4.2. Temporal Weights Calculation (Method: `calculate_temporal_weights`)

The matrix of temporal weights is calculated as follows:

- **Variable Definitions:**
- `t = Vector of timestamps, t = [t_1, t_2, ..., t_n]`
- `Delta T = Matrix of pairwise time differences, Delta T_{ij} = | t_i - t_j |`

- **Mathematical Representation:**

`W_{ij} = f(Delta T_{ij})`

where `f(x)` is a decay function, applied element-wise.

#### 4.3. Time Coordinate Calculation (Method: `calculate_time_coordinate`)

In this part, the focus is to determine a singular time coordinate `T` for a message. We base it on its relationship with its siblings:

- **Variable Definitions:**
- `t_message = Timestamp of the current message`
- `t_sibling_i = Timestamps of siblings`
- `Delta t_i = t_sibling_i - t_message`

- **Mathematical Representation:**

`T(t_message, Delta t) = g(time_diff)`

where `g(x)` is another decay function, and `time_diff` is the time difference between the message and a root message.

#### 4.4. Time Decay Factor (Method: `time_decay_factor`)

The time decay factor `D` will amalgamate the impacts of both individual message time and sibling relations:

- **Variable Definitions:**
- `avg(Delta t) = Average time differences between a message and its siblings`

- **Mathematical Representation:**

`D = g(time_diff) x avg(Delta t)`

### 5. Dimensionality Reduction via UMAP (Uniform Manifold Approximation and Projection)

UMAP plays a crucial role in reducing the dimensionality of the complex, high-dimensional message representations to a lower-dimensional space where relationships between messages are maintained.

- **Variable Definitions:**
  - `E(P_{i,j,k})` = Embedding for each message `i`, where `j` and `k` may denote specific features or layers in the embedding.
  - `R` = Joint representation vector, `R = [E(P_{i,j,k}), x, y, z, t]`

- **Mathematical Representation:**
  
  `R_reduced = UMAP(R)`

Where `R_reduced` is the lower-dimensional representation of the original feature vector `R`.

### 6. Clustering and Final Representation using HDBSCAN

HDBSCAN provides an elegant solution to clustering by identifying clusters of varying shapes and densities, making it apt for this application.

- **Variable Definitions:**
  - `C` = Set of clusters, `C = { C1, C2, ..., Cm }`
  - `R_reduced` = Lower-dimensional representations obtained from UMAP

- **Mathematical Representation:**

  `C = HDBSCAN(R_reduced)`

- **Multi-layered Interpretation:**
  
Messages are now characterized not just by their semantic content but also by their spatial-temporal coordinates. This multi-layered approach allows for a more comprehensive understanding of the conversation's topology and semantic themes.

## Getting Started Guide

This guide walks you through the process of setting up and running a sample code to visualize conversation data. The guide assumes you have a Python package named `dlm` and the conversation data is in a JSON format which can be downloaded from `chat.openai.com`.

### Prerequisites

1. **Download Conversation Data**: Log in to `chat.openai.com`, navigate to the relevant section and download your conversation data, usually available in JSON format.

### Step-by-Step Guide

#### Step 1: Import Required Packages
```python
import dlm_matrix as dlm
```

#### Step 2: Set Up Directory Paths
Replace the placeholders with your actual local directory paths.

```python
# Path to the downloaded JSON file containing conversations
CONVERSATION_JSON_PATH = "<path_to_downloaded_conversation_json>"

# Directory where you'd like to save the processed data
BASE_PERSIST_DIR = "<path_to_save_directory>"

# Name for the output file
OUTPUT_NAME = "<output_file_name>"
```

#### Step 3: Combine Conversations & Generate Chain Tree
Combine the conversations and create a chain tree data structure for further analysis.

```python
combiner = dlm.ChainCombiner(
    path=CONVERSATION_JSON_PATH,
    base_persist_dir=BASE_PERSIST_DIR,
    output_name=OUTPUT_NAME,
)

chain_tree = combiner.process_trees(tree_range=(<min_tree_size>, <max_tree_size>), animate=True)
```

Replace `<min_tree_size>` and `<max_tree_size>` with the minimum and maximum size of trees you wish to process.

#### Step 4: Visualize the Data
Finally, use the visualization utility to view the 3D scatter plot.

```python
dlm.plot_3d_scatter_psychedelic(file_path_or_dataframe=chain_tree).show()
```
