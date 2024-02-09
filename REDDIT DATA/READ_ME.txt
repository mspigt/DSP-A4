Downloading the reddit data can be done from: https://academictorrents.com/details/89d24ff9d5fbc1efcdaf9d7689d72b7548f699fc
This data can be requested from the group (approx 1.34tb).

step 1: cleaning_1 
- these programs extract structured data from the .zst files
- ensure the folders are created and the program is pointed at the location of the reddit data.
- comments and submissions have been seperated and are able to be run at the same time to reduce run time

step 2: cleaning_2
- these programs create and flag drug-related chatter by street name and mention of drug
- both programs can be run at the same time

step 3: cleaning_3 
- this program groups all the flagged comments and posts and creates a balanced dataset that is appropriate for training 

step 4: Comment_training 4
these programs are labelled in order to be run:
1. creates the Naive bayes and the XG_boost model for the binary and multi for the reddit comments
2. create the creates the NN for the binary comments
3. create the NN_multi for the comments
4. create half the predictions for all the models
5. completes the other half of the predictions for the models.


step 5: POST_training_5
1. creates and predicts the navie bayes and the xg_Boost models (binary)
2. create the NN binary for the posts
3. create the naive bayes and XG_Boost post (multi) and predicts
4. creates and predicts the NN_multi for the posts.

step 6: summary stats 6
- this create the tables appropriate for the dashboard
- 