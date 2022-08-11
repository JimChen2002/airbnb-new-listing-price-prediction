# Overview
This repository contains the frontend (Vue.js, Quasar) and backend (FastAPI) code for the webpage that takes inputs and predicts the price of a new AirBnB listing in Boston.

The instructions to run the code are in the frontend and backend directories. 

# Workflow

## Input

- Number of people it accommodates
- Number of bedrooms
- Number of beds
- Neighbourhood (in Boston)
- Bathroom type
- Property type
- Room type
- Amenties

There is no input for reviews because it aims to provide feedback for new listings.

## Output

- Price in dollars (regression)
- Price range (classification)

 Regression solution has a median absolute error of $26 and classification solution has an accuracy of 72% (on average of 5-fold cross validation).

 # Preview

 ![preview](https://github.com/JimChen2002/airbnb-new-listing-price-prediction/blob/master/images/preview.png)