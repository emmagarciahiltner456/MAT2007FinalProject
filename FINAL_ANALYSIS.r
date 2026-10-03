### EMMA GARCIA HILTNER FINAL PROJECT MAT2007
# Entire code may not run by playing the run buttom on top right, if not go through line by line with command + enter (may vary by computer type)

# remove saved lists, etc
rm(list=ls())


### ~~~~~~~~~~~~~~~~~~ open/load data ~~~~~~~~~~~~~~~~~~~~~~~~~~

# read data, will need to change location for own computer
heart <- read.csv(
  "/Users/emmagarcia/Desktop/MAT2007/processed.cleveland.data", #find file of data
  header = FALSE, #tell R there are no headers/column name in file
  na.strings = "?" #find data file and say that file doesnt have headers (FALSE), ? means value is missing
)


### CATEGORIES
colnames(heart) <- c( #label columns (found in file heart-diseases.names)
  "age", #years
  "sex",
  "cp",
  "trestbps", #resting blood pressure (in mm Hg on admission to the hospital)
  "chol", #serum cholestoral in mg/dl
  "fbs",
  "restecg",
  "thalach", #maximum heart rate achieved
  "exang",
  "oldpeak", #ST depression induced by exercise relative to rest
  "slope",
  "ca",
  "thal",
  "num" #diagnosis of heart disease (angiographic disease status) - Value 0: < 50% diameter narrowing, Values 1-4: increasing disease category
)

head(heart) #show first few rows of values + column names, tests if data properly stored
dim(heart) #check dimensions of data (should be 303, 14)



### ~~~~~~~~~~~~~~~~~~~ Calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###### Which factor best distinguishes patients with and without coronary heart disease?

# when first downloading might ask for a CRAN mirror, pick 0, if that doesnt work copy:
# "install.packages("pROC", repos = "https://cloud.r-project.org")" into terminal (at > symbol)
#install.packages("pROC") #remove # on this line at first use
library(pROC) #needed for AUC analysis


# Variables to test
traits <- c(
  "age",
  "trestbps",
  "chol",
  "thalach",
  "oldpeak")


# Create binary disease variable, make only no disease or disease (no severity)
heart$disease <- ifelse(heart$num == 0, 0, 1)
#if heart$num = 0 (no disease) then TRUE = 0, otherwise FALSE = 1


### Uncertainty setup

# set seed so bootstrap results are the same every time code is run (for same confidence interval)
set.seed(123)

# number of bootstrap samples used for uncertainty of Spearman correlation
n_boot <- 1000


# Empty results table (give a place to store the answers)
results <- data.frame(
  Trait = traits, #column for traits
  AUC = NA, #make a column for the AUC scores, will input later
  AUC_lower = NA, #lower 95% confidence interval for AUC
  AUC_upper = NA, #upper 95% confidence interval for AUC
  Spearman = NA, #column for spearman coef
  Spearman_lower = NA, #lower 95% confidence interval for Spearman
  Spearman_upper = NA) #upper 95% confidence interval for Spearman


# Calculate AUC and Spearman correlation for every variable using for loop (loops through each trait)
for (i in 1:length(traits)) {

  trait <- traits[i] #set current trait to test

  # Remove missing values for this trait ! keeps what is not missing
  complete <- !is.na(heart[[trait]]) & !is.na(heart$num)

  #dataset for only what is not missing, data_test is the cleaned data
  data_test <- heart[complete, ] # [row, column] blank column means keep when true


  ### Disease presence analysis
  # Build formula, for example disease ~ age
  formula <- as.formula( #formula runs disease against each trait in loop
    paste("disease ~", trait)) # ~ in statistics relates to predicted by

  # Logistic regression, still part of loop so formula gives current trait
  model <- glm( # generalized linear model
    formula,
    data = data_test,
    family = binomial) # since only disease absent (0) or present (1)

  # Predicted probability of disease using the glm model above
  prediction <- predict(
    model,
    type = "response") # so it returns probability
  
  # ROC curve for the data
  roc_result <- roc(
    data_test$disease, #the actual answer (if the individual did have CHD)
    prediction, # the models prediction for if an individual has CHD
    quiet = TRUE) # so pROC doesn't print a bunch of messages in console

  # Calculate and save AUC as "results"
  results$AUC[i] <- as.numeric( # as.numeric stores simple number for table, $ to make sure in correct row per trait
    auc(roc_result)) # calculating the area under the curve (AUC)


  ### Uncertainty for AUC
  # calculate 95% confidence interval for the AUC
  auc_ci <- ci.auc(roc_result)

  # save lower and upper confidence interval values
  results$AUC_lower[i] <- as.numeric(auc_ci[1])
  results$AUC_upper[i] <- as.numeric(auc_ci[3])


  ### Disease severity analysis
  results$Spearman[i] <- cor( #use spearman to test relationship strength between trait and CHD severity
    data_test[[trait]],
    data_test$num,
    method = "spearman") # evaluates the strength and direction of a monotonic relationship between two variables


  ### Uncertainty for Spearman correlation
  # empty vector to store Spearman correlations from bootstrap samples
  boot_cor <- numeric(n_boot)

  # repeat correlation calculation 1000 times using random samples
  for (b in 1:n_boot) {
    # randomly sample rows from data with replacement
    sample_rows <- sample(
      1:nrow(data_test),
      replace = TRUE)

    # create new dataset from the randomly sampled rows
    boot_data <- data_test[sample_rows, ]

    # calculate Spearman correlation for this bootstrap sample
    boot_cor[b] <- cor(
      boot_data[[trait]],
      boot_data$num,
      method = "spearman")}

  # calculate lower and upper 95% confidence interval
  spearman_ci <- quantile(
    boot_cor,
    c(0.025, 0.975),
    na.rm = TRUE)

  # save confidence interval values
  results$Spearman_lower[i] <- spearman_ci[1]
  results$Spearman_upper[i] <- spearman_ci[2]}



## Add absolute correlation strength, strongest predictors for table
# absolute value allows comparison of strength regardless of whether correlation is positive or negative
results$Severity_Strength <- abs(results$Spearman)

# Find which trait has the highest AUC before values are rounded
best_trait <- which.max(results$AUC)

# Find which trait has the strongest relationship with CHD severity before values are rounded
best_severity <- which.max(results$Severity_Strength)

# Print strongest results
cat("Best trait for distinguishing CHD presence:", results$Trait[best_trait], "\n")
cat("AUC:", round(results$AUC[best_trait], 3), "\n")
cat(
  "95% confidence interval:",
  round(results$AUC_lower[best_trait], 3),
  "to",
  round(results$AUC_upper[best_trait], 3),
  "\n\n")

cat("Strongest association with CHD severity:", results$Trait[best_severity], "\n")
cat("Spearman correlation:", round(results$Spearman[best_severity], 3), "\n")
cat(
  "95% confidence interval:",
  round(results$Spearman_lower[best_severity], 3), "to",
  round(results$Spearman_upper[best_severity], 3), "\n")

# Make a copy of results so values can be rounded for display without changing original values
display_results <- results

# Round values to visually better, to 3 decimal points
display_results$AUC <- round(display_results$AUC, 3)
display_results$AUC_lower <- round(display_results$AUC_lower, 3)
display_results$AUC_upper <- round(display_results$AUC_upper, 3)

display_results$Spearman <- round(display_results$Spearman, 3)
display_results$Spearman_lower <- round(display_results$Spearman_lower, 3)
display_results$Spearman_upper <- round(display_results$Spearman_upper, 3)

display_results$Severity_Strength <- round(
  display_results$Severity_Strength,
  3) # dont display entire number

print(display_results) # show table in terminal



### ~~~~~~~~~~~~~~~~~ Save data for Python ~~~~~~~~~~~~~~~~~~~~~~~~
### Save analysis results as ASCII file
# save results as tab-separated plain text file (.txt)
# this file will be opened in Python to make the AUC and Spearman graphs
write.table(
  results,
  "/Users/emmagarcia/Desktop/MAT2007/heart_disease_results.txt", # if you want save, change location
  sep = "\t",
  row.names = FALSE,
  quote = FALSE)



### Save raw data needed for Python scatterplot
# select variables needed for the scatterplot
scatter_data <- heart[, c(
  "age",
  "trestbps",
  "chol",
  "thalach",
  "oldpeak",
  "num")]

# save individual patient values as ASCII text file (.txt)
write.table(
  scatter_data,
  "/Users/emmagarcia/Desktop/MAT2007/heart_scatter_data.txt",
  sep = "\t",
  row.names = FALSE,
  quote = FALSE)