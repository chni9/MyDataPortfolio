# PythonProjectDrugConsumption

Problematic :
- What caracterizes a drug consumer ?
- What drugs and substances are the most correlated ?
- Can we predict a future drug consumer using ML ?
- How to prevent the rise of new consumers ?

I - Data preprocessing :
- import dataframe
- import by webscraping into dataframes the 'values' and 'meanings' of each columns from https://archive.ics.uci.edu/ml/datasets/Drug+consumption+%28quantified%29
- create a dataframe with all 'meanings' and clean the NaN
- delete all 'semer' users reponses

II - Data visualization :

1- General : 
- one plot for each criteria (age, education, country, etc.)
- personnality distribution box plot
- drug use distribution box plot
- heatmap of correlations for all the substances

2-Age criteria
- 3 heatmaps : cigaret consumption, lsd consumption and caffeine consumption
- legal addictions by age
- light drugs by age
- hard drugs by age
- personnality by age
- substances use by age

3-Education criteria
- 3 heatmaps : cigaret consumption, lsd consumption and caffeine consumption
- legal addictions by education
- light drugs by education
- hard drugs by education
- personnality by education
- substances use by education

4-Gender criteria
- 3 heatmaps : cigaret consumption, lsd consumption and caffeine consumption
- legal addictions by gender
- light drugs by gender
- hard drugs by gender
- personnality by gender
- substances use by gender

5-Country criteria
- 3 heatmaps : cigaret consumption, lsd consumption and caffeine consumption
- legal addictions by Country
- light drugs by Country
- hard drugs by Country
- personnality by Country
- substances use by Country
- pie plot cannabis consumption in legal countries vs illegal countries

6-Ethnicity criteria
- personnality by ethnicity
- substances use by ethnicity

III - Machine Learning Model :
1- Choose a model (chosen model PCA)
- define variables
- define targets
- define and fit the PCA model
- scree plot and variance ratio to choose the number of components
- get the 3 PCs

2-Plot
- Graph of variables : PC1&PC2, PC1&PC3 and PC2&PC3
- Scatter plots for each criteria (age, gender, etc.) for PC1&PC2, PC1&PC3 and PC2&PC3

3-Applying the ML model
- generate train and test sets
- applying Linear SVC model
- for each criteria : train the model -> get the predictions -> obtain a score (percentage of right predictions) -> confusion matrix -> cross-validation score
- repeat the process with KNN model
- repeat the process with KNN optimized
- compare the models and choose the right one for each criteria
- fit the right model for each criteria

4- Predict an individual
- create a predict function that predicts an individual from 3 scores
- test the function and the models

IV - API :
- create a Flask API from the ML model

V - PowerPoint

Conclusion :
- Young people tend to be using more drugs.
- Men tend to be using more hard drugs but it is more or less equal for light drugs, alcohol and nicotine -> this can be explained by the opposite personalities between men and women.
- Education doesn't seem to make a big difference in drug use but does change for nicotine addiction.
- Cannabis is a gateway into using new drugs.
- Countries where cannabis is legal have more drug consumers.
- Personality does have a big impact on drug consumption, especially openness to experience, impulsiveness and sensation seeing.
