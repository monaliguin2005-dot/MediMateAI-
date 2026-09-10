# 🌿 MediMateAI

### Personalized AI Wellness Companion for College Students

MediMateAI is an AI-powered wellness chatbot designed to help college students reflect on their everyday wellness, track daily habits, identify wellness patterns, and receive personalized general guidance.

## 🎯 Problem

College students often experience academic stress, irregular sleep, changes in diet, low mood, fatigue, and other wellness concerns. However, they may not have a simple way to discuss these concerns, track them consistently, or understand when they should seek professional support.

MediMateAI provides a conversational wellness companion that helps users describe how they are feeling and receive personalized, supportive guidance.

## 👥 Target Users

The primary target users are:

- College students
- Young adults
- Students experiencing academic stress
- Users who want to track everyday wellness habits

## 🤖 Why Gemini?

Wellness concerns are highly personal and users describe them in different ways.

A traditional rule-based chatbot would require manually creating responses for many possible combinations of user inputs.

Gemini allows MediMateAI to:

- Understand natural-language user messages
- Generate personalized responses
- Ask relevant follow-up questions
- Use user context when generating responses
- Provide conversational wellness guidance

Gemini is used as the conversational intelligence layer while application logic handles deterministic tasks such as wellness scoring and data storage.

## ✨ Features

### 💬 AI Wellness Chat

Users can describe their feelings, habits, concerns, or wellness experiences in natural language.

Gemini generates a personalized response.

### 📋 Daily Check-in

Users can provide daily wellness information.

The backend processes the information and calculates a wellness score.

### 📊 Wellness Score

A score is calculated from daily check-in information to provide users with a simple overview of their current wellness.

### 🧠 Wellness Pattern

The application can use stored wellness information to help identify patterns over time.

### 🌱 One Small Change

The application provides a practical small wellness action that the user can try.

### 🔐 Environment-based API Key

The Gemini API key is stored using environment variables and is not included in the source code.

## 🏗️ Architecture

```text
User
  ↓
Frontend
(HTML + CSS + JavaScript)
  ↓
Python Backend
  ↓
Prompt + User Context
  ↓
Gemini API
  ↓
AI Response
  ↓
Frontend
