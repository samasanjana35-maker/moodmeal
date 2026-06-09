# Problem Statement: AI-Powered Restaurant Recommendation System

## Overview

Build an AI-powered restaurant recommendation service inspired by Zomato. The system should suggest restaurants that match a user's preferences by combining structured restaurant data with a Large Language Model (LLM) to produce personalized, human-readable recommendations.

## Objective

Design and implement an application that:

- Accepts user preferences (location, budget, cuisine, ratings, and other constraints)
- Uses a real-world restaurant dataset as the source of truth
- Leverages an LLM to rank options and explain why each recommendation fits
- Presents results in a clear, useful format for end users

## Dataset

Use the Zomato restaurant dataset hosted on Hugging Face:

**[ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)**

Relevant fields to extract and use include:

- Restaurant name
- Location
- Cuisine type
- Cost / price range
- Rating
- Other attributes useful for filtering and ranking

## System Workflow

### 1. Data Ingestion

- Load and preprocess the dataset from Hugging Face
- Clean and normalize fields needed for filtering and display
- Prepare a structured representation suitable for downstream filtering and LLM prompting

### 2. User Input

Collect preferences through a **basic web UI** (form-based). The user submits:


| Preference | Examples |
|---|---|
| Location | Delhi, Bangalore |
| Budget | Low, medium, high |
| Cuisine | Italian, Chinese |
| Minimum rating | e.g. 4.0+ |
| Additional constraints | Family-friendly, quick service, outdoor seating |

### 3. Integration Layer

- Filter restaurant data based on user input
- Select a candidate set of relevant restaurants
- Format structured results into an LLM prompt
- Design a prompt that enables the model to reason over options and produce ranked recommendations

### 4. Recommendation Engine

Use the LLM to:

- Rank restaurants from the filtered candidate set
- Explain why each recommendation matches the user's preferences
- Optionally summarize trade-offs between top choices

### 5. Output Display

Present the top recommendations in a user-friendly format. Each result should include:

- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation of why it was recommended

## Success Criteria

The solution is successful when it:

1. Correctly filters restaurants based on structured user preferences
2. Uses the LLM to add value beyond simple filtering (ranking and explanation)
3. Returns consistent, readable output that helps users make a decision
4. Handles edge cases gracefully (e.g. no matches, ambiguous preferences)

## Out of Scope (Optional Clarifications)

- User accounts and persistent preference history
- Real-time restaurant availability or booking
- Production-grade deployment and scaling

These may be considered extensions but are not required for the core milestone.
