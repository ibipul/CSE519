# Project Report

Following is an executive summary of the current HW2.

## Model Building

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


