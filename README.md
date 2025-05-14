# Social Network Simulation with EdgeRank – University Project (Python)

This repository contains a Python-based simulation of a simplified **social network**, developed as part of a university project. The main goal was to process a large dataset of posts and rank them using a **graph-based EdgeRank algorithm**, similar to those used in modern social media feeds.

## 🌐 Project Overview

The project simulates the core behavior of a social media platform by analyzing and ranking posts based on various factors. Each post in the dataset includes:

- **Timestamp**
- **Reactions** (likes, dislikes, etc.)
- **Comments**

### Main Features:

- **Feed Ranking** using a custom implementation of the **EdgeRank algorithm**
- **Graph representation** of relationships between users and posts
- **Search functionality** to query posts
- **Autocomplete** suggestions for search terms based on indexed post content

## 📊 EdgeRank Algorithm

The EdgeRank algorithm was adapted to this simulation to determine which posts are most relevant to a user’s feed. Ranking is influenced by:
- **Affinity score** (user-post interaction)
- **Weight** (type and number of interactions: likes, comments, etc.)
- **Time decay** (older posts lose value over time)

The graph structure links users and posts, with edge weights representing interaction strength.

## 🔍 Search and Autocomplete

The project includes a simple **search engine** that:
- Supports full-text search through posts
- Suggests **autocomplete** options based on prefixes
- Ranks search results using post relevance and popularity

## 🛠️ Technologies Used

- Python 3

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/davidstakic/graph-edge-rank.git
