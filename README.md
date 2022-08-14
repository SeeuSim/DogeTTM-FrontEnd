# NUS Orbital'22 DogeTTM Overview

A project created under NUS module CP2106: Independent Software Development Project (Apollo 11).

Team Members: <br />
Liu Zixin <br />
Ong Seeu Sim

## Navigation
* [Description](#description)
* [Tech Stack](#tech-stack)
* [Motivation](#motivation)
* [Problem](#problem)
* [Solution and Benefits](#solution-and-benefits)
* [Market Validation](#market-validation)
* [Features](#features)
* [Price Prediction Model](#price-prediction-model)
* [Design Principles and Diagrams](#design-principles-and-diagrams)
* [Problems Encountered](#problems-encountered)
* [Testing and Evaluation](#testing-and-evaluation)
* [To Run](#to-run)
* [Evaluation and Subsequent Plans](#evaluation-and-subsequent-plans)

## Description

DogeTTM is a webapp that uses social media sentiment analysis to provide NFT investors with price insights on their NFT studio/token, through 3 main features:
1. Dashboard showing top 5 performing NFTs of the week (filterable by percentage price change, absolute price change and volume)
2. Search bar displaying information and performance of a specific NFT token/studio.
3. Historical prediction accuracy rate for each NFT studio.

Note: NFT studio refers to the brand/creator of NFT tokens, an example of which would be the Bored Apt Yacht Club.

## Tech Stack
Front-End - Typescript with Preact <br />
Back-End - Django, TensorFlow, Mnemonic API, Heroku, PostgreSQL

## Motivation
As a user who has heard about the NFT rise, who has heard about the USD$122 billion market size, who has witnessed a dozen friends making 6-figure profits from NFT trading, I am dying to find out what this is all about and how I can profit too.

However upon a basic Google search, sites like openSea provide only basic price trends for NFTs, but I know that to profit consistently, I need a way to jump onto the latest hype before other people discover it.

Hence, a site like DogeTTM, with its real-time social media (Twitter) sentiment analysis, will help me uncover the latest buzz in the NFT space, and I can invest before it reaches the mainstream.

Moreover, through its price prediction tools, I will be able to determine when a crash is coming, or how well my portfolio stacks up in the coming weeks, so I can prime my portfolio to cut loss, as well as double down on winning collections.

## Problem
As a user looking to invest and gain deeper insights into the NFT space,  current NFT price platforms do not provide users with useful insights into price trends other than basic price movements  (such as real-time social media sentiment analysis or celebrity tweets).

1st Problem:
Most users do not have access to exclusive discord release channels for NFT, and by the time they learn about a rising NFT through news or their social media, its too late to profit.

2nd Problem:
NFT space is very volatile, and as in the case of Luna in the crypto space, an investor's portfolio may be wiped out overnight, due to echoing fear among the community and a Domino effect from investors. There is a need on a real-time tracking of fear index (sentiment) in the market.

## Solution and Benefits
Since NFT prices are very volatile and unpredictable, and a large proportion of price movements are determined by sentiment shifts (online hype) rather than fundamental analysis. We can tap into the power of social media sentiment analysis to gain deeper insights into both price trends of big players, as well as identify up-and-coming collections so that we can invest before it reaches the mainstream.

This way, investors will be better-equipped to make NFT investments since they can now view the top predicted NFTs for next week, top performing NFTs of the current week, as well as search their own NFTs of interest to view the sentiment score, making DogeTTM a very versatile platform for investors to research on NFTs.

Secondly, they can also view when the fear index is rising beyond the threshold, and sell accordingly.


## Market Validation
Through thorough preliminary research, we have determined there is no existing free sentiment analysis platform for NFT collections, due in part to the novelty of the NFT space.
With the recent yearly double digit growth in NFT market cap, there has been more demand for more advanced analytics tool within the space.

Through polls on online forums (Reddit) and interviews with our peers, we have identified a strong interest in a product that can identify trending NFT collections before they reach the mainstream, and hence we have decided to embark on this project.

## Features
![Orbital Video Presentation](https://user-images.githubusercontent.com/105634117/175895718-18ef378f-db6f-4ea1-97ad-bce9eee2f531.jpg)

Dashboard:
Using a Django backend, our app will scrap data on social media platforms Twitter and Reddit and categorise tweets based on NFT collections and assign a sentiment score. Top rated NFTs will be pushed to the top of the dashboard, allowing investors to catch opportunities as soon as they sizzle.

The front-end dashboard components will be created using Typescript and Preact.

Search Bar:
The webapp uses server-rendered HTML to communicate frontend(client webapp) to Django backend (dashboard).

Price Prediction Model:
We use LSTM algorithm to train our price prediction model, with sentiment scores over time and price over time (one step up) as our parameters.

## Price Prediction Model:
Choosing of Learning Algorithm:
According to a 2018 ![report](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-017-0111-6#Sec21) titled "Big Data: Deep Learning for financial sentiment analysis", the Pearson Correlation Coefficient between a stock price and a general user’s sentiment is equal to 0.05, which means that only 53% of the time are users able to predict future stock prices correctly. With the use of deep learning models in sentiment analysis, the percentage can rise to up to 75%.
![comparison](https://user-images.githubusercontent.com/25603844/180782877-da9ec8b1-71b1-4adc-b901-959edf045c70.PNG)


In the analysis, Convolutional Neural Network (CNN) model had the best performance, followed by LSTM (based of RNN), Logistic Regression then lastly Doc2Vec.
As CNN is convolutional in nature and requires a very specifically transformed set of inputs, we opted for the second best performing model LSTM. The difference between LSTM and RNN is that LSTM effectively resolves the vanishing gradient problem of RNN, where recent inputs are weighted higher. Hence accounting for ease of data processing and performance, we opted for LSTM as our machine learning model.

Data Collecting and Processing:

For the top 500 NFT collections, we collect daily price data over the past 7 days (due to a 7-day limit by the twitter search API), and append it to a priceArray. At every day iterated for each token, we call a function to get the twitter sentiment for that day (value from -1 to 1), and append it to a sentimentArr.
We then clean arrays with insufficient data (as some collections do not have data for a field on that day), and transform it into a one-dimensional numpy array, and normalise the price to (-1 to 1).

Model training and prediction:

We have 2 separate files for model training and prediction, under backend/train.py and backend/prediction.py. Everyday we feed new data to train.py, and it trains the model using sentimentArr as X variable, and priceArr (one day ahead) as Y variable, then eventually it stores the trained model as "name.h5", with h5 being a model extension.
Then, in prediction.py, we load up the model and predict the next day price increase (in percentage), with the sentiment score as input. If an array of sentiment scores are provided, then the next day price increase will be more accurate.

## Design Principles and Diagrams

Architectural Style: For this project, we use a mix of client-server architectural style and n-tier architectural style on the server-side.

UML Diagram:
![src_diagram (2)](https://user-images.githubusercontent.com/25603844/175934696-46c957dd-5184-47b2-a60c-4465ba92494e.png)

Design Approach : We adopt the waterfall design approach by focusing on creating a basic home page first, then expanding our feature list, starting from individual NFT page, to searchbar, to dashboard, then lastly price prediction model.

![waterfall](https://user-images.githubusercontent.com/25603844/180778975-bd4f8a2e-39c1-404a-a48c-c8ac09f4d4bd.jpg)

UI/UX : We focused on ease of use for users, making it as easy as possible to understand and interact with the features as possible. For example:
- Home Page is accessible by a simple click of the header logo -> No need for unnecessary routing.
- Reduced number of pages to just 2 (Dashboard and Single Collection Page). -> Easy navigation and clear structure, minimises navigation and button clicks.
- Dashboard information is on a single-page and displayed on click for the default home page. -> No need to renavigate for different data.

Hence, with just 2 main pages and simple workflow, the user design is straightforward and easy to remember for users.


## Problems Encountered

1. Some functions and images are very computation-intensive/resource-intensive, so end data take a long time to load.
Solution : We implemented async functions wherever possible, changed rendering order/structure to optimise load time, and reduced total number of times the data is routed to the end function, through reviewing the UML class diagram.

2. Even though the API functions output the correct data format, some NFT tokens are very new, so they are missing in some data values. Fetching code returns incomplete data, and the API call will return an error when we use it for subsequent functions. For the ML models, we had to spend a lot of time debugging the data processing and cleaning, because the input were missing in a lot of fields and we had to clean, reshape and transform it by numpy standards.

Solution : We implemented functions such as clean(), and have data integrity check when inserting/updating the database to ensure that incoming data is complete.


## Testing and Evaluation
For Milestone 2 we have performed developer testing as well as system testing. For subsequent milestone 3 we have integrated unit testing for Django models into our code.

For milestone 3, we added unit test cases for the model classes, testing interactions with the database through methods like create(), delete(), and update() and asserting the results.
### Example Testcases:
1) When I update the collection object, querying that specific field should give me the updated value.
2) When I create a duplicate collection or datapoint object, the new entry should be unable to be added, and an error message will show up regarding the duplicate.
3) When I delete the object, it will no longer be queried.

We also manually tested how the Typescript components interact with one another and with the system as a whole, whether the pages are routed correctly; as well as testing the input from the fetch API to the output graphs and JSON objects displayed at the end.

### Example Testcases:
1) When on the `Home` page, the data should load when I click the `See My Data!` button.
2) When I select the different ranking metrics and re-click the `See My Data!` button, the data should re-render according to the metric chosen.
3) When I click on the collection name hyperlink, I should navigate to a page displaying the token metadata.
4) The token metadata page should have a graph showing the price data.
5) When I click on the Logo at the top left, I should navigate back to the main page.

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

python -m nltk.downloader vader_lexicon
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
python manage.py createcachetable 
python manage.py runjobs daily
python manage.py runserver
```
`cachetable` is to reate the cache in the database backend.
Provided the `backend/backend/.env` is setup according to `SETUP.md`, 
`runjobs daily` should populate the server with the API data to be served to the frontend.

8) Change directory to `directory_name/frontend` and run the command:
```
npm run dev
```

9) Navigate to the frontend network endpoint in your browser of choice.

## Evaluation and Subsequent Plans
What we have accomplished for Milestone 2:
- Typescript preact frontend and Django backend development from scratch for a functional MVP.
- Backend sentiment analysis functions.
- Backend data processing functions for NFT prices, volume, trends against sentiment.
- Frontend routing between pages
- API call functions for NFT data and routing from backend to frontend.
- Graphing functions

What we have accomplished for Milestone 3:
- Finish training our price prediction model and integrate it into our code.
- Test different ML models (linear regression, CNN, RNN) and pick an optimal one
- Optimise our fetch requests for NFT data for faster loadtime.
- CSS styling

However, please do note that some url mappings for frontend is broken, hence the JSON responses for sentiment and prediction are not visibly reflected on the frontend side. We have been trying to fix this to the best of our abilities, and will update here once it is fixed.
For assessment on price prediction, please run predict.py and train.py under backend/NFT in your terminal and see the results.

Additional features/touch-up we would like to add before Splashdown:
- Fix urlmapping for frontend
- Refining the machine learning to be even more accurate
- Add a personal wallet
- Further CSS styling
