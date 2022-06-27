# NUS Orbital'22 DogeTTM Overview

A project created under NUS module CP2106: Independent Software Development Project (Gemini Level looking to upgrade to Apollo 11).

Team Members: <br />
Liu Zixin <br />
Ong Seeu Sim

## Description

DogeTTM is a webapp that uses social media sentiment analysis to provide NFT investors with price insights on their NFT studio/token, through 3 main features:
1. Dashboard showing top 5 performing NFTs of the week (filterable by percentage price change, absolute price change and volume)
2. Search bar displaying information and performance of a specific NFT token/studio.
3. Historical prediction accuracy rate for each NFT studio.

Note: NFT studio refers to the brand/creator of NFT tokens, an example of which would be the Bored Apt Yacht Club.

## Tech Stack
Front-End - Typescript with Preact <br />
Back-End - Django, TensorFlow, Rarify API, Heroku

## User Story
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
We use simple linear regression algorithm under supervised learning to train our price prediction model, with sentiment scores over time and price over time as our parameters.

## Design Principles and Diagrams

Architectural Style: For this project, we use a mix of client-server architectural style and n-tier architectural style on the server-side.

UML Diagram: 
![src_diagram (2)](https://user-images.githubusercontent.com/25603844/175934696-46c957dd-5184-47b2-a60c-4465ba92494e.png)

Design Approach : We adopt the bottom-up agile design approach by focusing on creating a minimum viable product(MVP) with a basic home page first, then expanding our feature list, starting from individual NFT page, to searchbar, to dashboard, then lastly price prediction model.

![agile](https://user-images.githubusercontent.com/25603844/175925496-a9435b13-1cf4-4079-bead-4470f53e1530.png)

UI/UX : We focused on ease of use for users, making it as easy as possible to understand and interact with the features as possible. For example:
- Home Page is accessible by a simple click of the header logo -> No need for unnecessary routing.
- Reduced number of pages to just 2 (Dashboard and Single Collection Page). -> Easy navigation and clear structure, minimises navigation and button clicks. 
- Dashboard information is on a single-page and displayed on click for the default home page. -> No need to renavigate for different data.

Hence, with just 2 main pages and simple workflow, the user design is straightforward and easy to remember for users.


## Problems Encountered 
 
1. Some functions and images are very computation-intensive/resource-intensive, so end data take a long time to load.
Solution : We implemented async functions wherever possible, changed rendering order/structure to optimise load time, and reduced total number of times the data is routed to the end function, through reviewing the UML class diagram.

2. Even though the API functions output the correct data format, some NFT tokens are very new, so they are missing in some data values. Fetching code returns incomplete data, and the API call will return an error when we use it for subsequent functions.
Solution : It is not a pressing problem that affects the end user that much, since it constitutes a small and insignificant portion of NFT collections. But we looking into solutions and other APIs, such as OpenSea as a possible API to add to/migrate to.

## Testing and Evaluation 
For Milestone 2 we have performed developer testing as well as system testing. For subsequent milestone 3 we will integrate automated testing into our code, with the focus being on behaviour testing using Selenium and Behave in Python.

During milestone 2, we performed installation and set-up on 4 different OS machines (Windows, Linux, Mac, Ubuntu), and updated the dependencies and settings to suit all machines, as well as updating README to be OS-independent.

We also manually tested how the Typescript components interact with one another and with the system as a whole, whether the pages are routed correctly; as well as testing the input from the fetch API to the output graphs and JSON objects displayed at the end.

### Example Testcases:
1) When on the `Home` page, the data should load when I click the `See My Data!` button.
2) When I select the different ranking metrics and re-click the `See My Data!` button, the data should re-render according to the metric chosen.
3) When I click on the collection name hyperlink, I should navigate to a page displaying the token metadata.
4) The token metadata page should have a graph showing the price data.
5) When I click on the Logo at the top left, I should navigate back to the main page.
Other features, such as changing the price data time range via dropdown, search, sentiment analysis and price prediction, have yet to be implemented and as such are unable to be tested.
Looking forward, a Continuous Integration (CI) workflow will be implemented to automatically test the code for each push to GitHub. This speeds up testing procedures.   
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
- Debug and finish our search bar feature.
- Test different ML models (linear regression, CNN, RNN) and document their respective accuracy rates.
- Optimise our fetch requests for NFT data for faster loadtime.
- User authentication system and possibly a personal wallet 
- CSS styling
