# Project Report

Following is an executive summary of the current HW2.

## About the Task

The problem was quite challenging because the subtleties in this data are a bit hard to guage. 
- Primarily reason being, the entrie task hinges on predicting the errors of a blackbox model that is in business for sometime.
- Secondly, for most of the intutive features that one may thing are important indicators of prices of housings are sparse.
- Third there are composite data as well as simple data. Like some columns as in Zip code are good enough to infer city, region, state, neigbourhood etc., so there is redundancy.
- Categorical variables itself makes me quite un-comfortable, so the flood of such variables was a bit jarring so to say.

## Data Description
Analysis of the data showed that there are broadly 3 types of attributes in the data set. 
- Categorical, both numeric as well as strings.
- Numeric but non-quatized, and,
- Numeric discreet, as in quantized like count variables.

It was observed that some of the count data correlated well like bedroom and bathroom counts, while others had very slight dependence. 

Tax data - be is holistic, land, structure intuitively sounds like a good indicator but some cursory analysis shows infact the room-count is anti-correlated to total taxamount. Interestingly enough while there is a significant correlation between bedroom and bathroom count, there is not so much correlation among them and the room count.

It would make that trying to look at correlations of the logerror with other variables, but that turned up with very low correlation values, much to my dismay.

## Attribute selection
I personally leaned towards selecting:
- a majority of the count data like count of rooms, bathrooms, bedrooms; 
- the descriptive elements of a house like: Total living area, total free space around the house, total garage space etc.
- Apart from this I relied heavily on Tax elements as I was convinced that predicting the actual price is probably a completely different ball game as compared to predicting error of prices against a bloack box.
- Apart from this I decided to take in account some numeric categorical variables that seemed interesting like Air conditioning type, building quality rating and heating system. Some of these seemed like parameters that zillow system factor as they were not as scarce as many other data.
- One decision that was conciously taken was selection of variables that have very less amount of missing data. This would ensure minimal interferance on my part in massaging the data into shape.

## Handling the missing data
Given my choice of variables and way I selected them the data cleaning strategy was very straight forward.
- For Numeric quatities, I imputed the missing values by the median of the same quantiti observed in the collection. Then I have used the simple normalization of subtract mu and divide by Standard deviation.
- For Categorical yet numeric quantities, I decided to denote the missing data as a category as no-information. So I imputed these areas with 0. Now most models would probably interpret numeric categorical labels as some sort of rating. Better option has a higher numeric rating. Which is not always true, and also given the information available to me especially from the data-dictionary -- it was not very clear. So I decided to take up one hot encoding. Essentially for a column with n levels, we add n-1 extra columns each with a binary switch defined on each levels of the original columns..