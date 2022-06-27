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
Back-End - Django, TensorFlow, Rarify API, Heroku

## Problem and Solution
NFT prices are very volatile and unpredictable, and a large proportion of price movements are determined by sentiment shifts (online hype) rather than fundamental analysis such as in stocks. Unlike well-established online stock price platforms, current NFT price platforms do not provide users with useful insights into price trends other than basic price movements  (such as real-time social media sentiment analysis or celebrity tweets).

We aim to scrap data on discussions and mentions of NFT tokens/studios on social media channels (with the most prominent ones being Twitter and Discord), and assign each NFT studio with a sentiment score which will be displayed on the dashboard.

This way, investors will be better-equipped to make NFT investments since they can now view the top predicted NFTs for next week, top performing NFTs of the current week, as well as search their own NFTs of interest to view the sentiment score, making DogeTTM a very versatile platform for investors to research on NFTs.

## Features
![Orbital Video Presentation](https://user-images.githubusercontent.com/105634117/175895718-18ef378f-db6f-4ea1-97ad-bce9eee2f531.jpg)

Dashboard:
Using a Django backend, our app will scrap data on social media platforms Twitter and Reddit and categorise tweets based on NFT collections and assign a sentiment score. Top rated NFTs will be pushed to the top of the dashboard, allowing investors to catch opportunities as soon as they sizzle.

The front-end dashboard components will be created using Typescript and Preact.

Search Bar:
The webapp uses server-rendered HTML to communicate frontend(client webapp) to Django backend (dashboard).

Price Prediction Model:
We use simple linear regression algorithm under supervised learning to train our price prediction model, with sentiment scores over time and price over time as our parameters.

## Design Principles and Diagrams

Architectural Style: For this project, we use a mix of client-server architectural style and n-tier architectural style on the server-side.

Design Approach : We adopt the bottom-up agile design approach by focusing on creating a minimum viable product(MVP) with a basic home page first, then expanding our feature list, starting from individual NFT page, to searchbar, to dashboard, then lastly price prediction model.
![agile](https://user-images.githubusercontent.com/25603844/175925496-a9435b13-1cf4-4079-bead-4470f53e1530.png)

UML Diagram: 

User-flow Diagram:


## Testing and Evaluation 
For Milestone 2 we have performed developer testing as well as system testing. For subsequent milestone 3 we will integrate automated testing into our code, with the focus being on behaviour testing using Selenium and Behave in Python.

During milestone 2, we performed installation and set-up on 4 different OS machines (Windows, Linux, Mac, Ubuntu), and updated the dependencies and settings to suit all machines, as well as updating README to be OS-independent.

We also manually tested how the Typescript components interact with one another and with the system as a whole, whether the pages are routed correctly; as well as testing the input from the fetch API to the output graphs and JSON objects displayed at the end.

## To Run
1) Setup a directory `directory_name` on your local machine. In your terminal, change directory to `directory_name` as specified earlier, and `git clone` this package there.

2) Ensure that you have Python and `pip` installed on your machine.

3) Setup a virtual environment using the following terminal command:
```
python -m venv /path/to/new/virtual/environment
```
Proceed to `activate` the virtual environment using the specific system command for your Operating System. Mac users may wish to use the command `python3` instead to avoid conflicts with the Python version installed with Xcode Tools.

4) Change Directory to the `directory_name/backend`. Then install the Python packages via this command:
```
python -m pip install -r requirements.txt
```
Should any of the packages fail to install, the remaining packages may/may not be installed and the command may need to be re-run after fixing the issues highlighted.

5) Change Directory to the `directory_name/frontend`. Using your `npm` or Node Package Manager, run the terminal command:
```
npm install
```
to install any dependencies.

6) Get the necessary API keys from <a>rarify.tech</a> and <a>developer.twitter.com</a> and populate the `directory_name/frontend/.env` file with the necessary details. </br>
Alternatively, you may reach out for the keys if needed.

7) Change directory to `directory_name/backend` and run these commands:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Save the network endpoint under "endpoint" in `directory_name/frontend/URLCONFIG.json`

8) Change directory to `directory_name/frontend` and run the command:
```
npm run dev
```
Save the network endpoint and paste it in CORS_ALLOWED_ORIGINS under `directory_name/backend/backend/settings.py`

9) Navigate to the frontend network endpoint in your browser of choice.

## Evaluation and Subsequent Plans
So far we have accomplished: 
- Typescript preact frontend and Django backend development from scratch for a functional MVP.
- Backend sentiment analysis functions.
- Backend data processing functions for NFT prices, volume, trends against sentiment. 
- Frontend routing between pages
- API call functions for NFT data and routing from backend to frontend.
- Graphing functions

To-Do for Milestone 3:
- Finish training our price prediction model and integrate it into our code.
- Test different ML models (linear regression, CNN, RNN) and document their respective accuracy rates.
- Optimise our fetch requests for NFT data for faster loadtime.
- User authentication system and possibly a personal wallet 
- CSS styling
