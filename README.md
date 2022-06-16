# NUS Orbital'22 DogeTTM Overview

A project created under NUS module CP2106: Independent Software Development Project (Gemini Level).

Team Members: <br />
Liu Zixin <br />
Ong Seeu Sim

## Description

DogeTTM is a webapp that uses social media sentiment analysis to provide NFT investors with price insights on their NFT studio/token, through 3 main features:
1. Dashboard showing top 5 performing NFTs of the week (filterable by percentage price change, absolute price change and volume)
2. Search bar displaying information and performance of a specific NFT token/studio.
3. Historical predition accuracy rate for each NFT studio.

Note: NFT studio refers to the brand/creator of NFT tokens, an example of which would be the Bored Apt Yacht Club.

## Tech Stack
Front-End - Typescript with Preact, Tailwind/Material CSS <br />
Back-End - Django, Moralis, TensorFlow, Heroku

## Problem and Solution
NFT prices are very volatile and unpredictable, and a large proportion of price movements are determined by sentiment shifts (online hype) rather than fundamental analysis such as in stocks. Unlike well-established online stock price platforms, current NFT price platforms do not provide users with useful insights into price trends other than basic price movements  (such as real-time social media sentiment analysis or celebrity tweets).

We aim to scrap data on discussions and mentions of NFT tokens/studios on social media channels (with the most prominent ones being Twitter and Discord), and assign each NFT studio with a sentiment score which will be displayed on the dashboard.

This way, investors will be better-equipped to make NFT investments since they can now view the top predicted NFTs for next week, top performing NFTs of the current week, as well as search their own NFTs of interest to view the sentiment score, making DogeTTM a very versatile platform for investors to research on NFTs.

## Features Explanation
Dashboard:
Using a Django backend, our app will scrap data on social media platforms Twitter and Reddit and categorise tweets based on NFT collections and assign a sentiment score. Top rated NFTs will be pushed to the top of the dashboard, allowing investors to catch opportunities as soon as they sizzle.

The front-end dashboard components will be created using Typescript and Preact.

Search Bar:
The webapp uses both AJAX and server-rendered HTML to communicate frontend(client webapp) to Django backend (dashboard).

Price Prediction Model:
We use simple linear regression algorithm under supervised learning to train our price prediction model, with sentiment scores over time and price over time as our parameters.
