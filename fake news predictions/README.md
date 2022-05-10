# The aim of this project is to predict if a news is fake or real provided that the author,title and text the news contain were given.

 During the data preprocessing stage,I made of of PorterStemmer class to stem the word(to get the root word),also a new variable called content was created which is the combination of the author's name and the title .This content was used as the thee feature varaible to predict the target.Also made use of a vectorizer to convert the text data into numerical data as machine learning algorithms understands numerical data better.

 ## MOdel training

 The model was trained using logistics regression as it used to perform well on binary classification problems. Logistic regression gives approximately 98% on the unseen data for this project.