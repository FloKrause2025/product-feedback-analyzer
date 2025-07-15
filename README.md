# Here you can find a detailed explanation about this workflow

# External data sources:
* reddit
* Product Hunt

# Potential other external sources
* Google Reviews
* Social Media Accounts
* Community Forums
* Trustpilot Reviews
* Proven Expert reviews
* G2 review 
* etc

# Internal data sources 
* Customer support tickets
* Chatbot Conversations

**This is the real game changer!** 

By adding internal datasets as of the above mentioned sources, you can merge external and internal data into something extremly valuable for your Business.
Since external sources are quite subjective and sometimes based out of frustration, internal data sources can make the big different. 

**I encourage you and your company to make PROPER use of internal data sources. YOU ARE IN TOUCH WITH THE CUSTOMER, which is possibily the best way to improve your product**

# What API's endpoints do you need for this workflow

* LLM API = we have used ChatGPT 
* External Sources API = In our use-case we have used the reddit & Product hunt API. 

**If you want to connect other data sources to this workflow you simply need to add the API keys in your .env and add the right strings to your main script**

# Explanation of the "analyzer.ipynb" Script

Before the actual script start install the following packages:

* !/your directory/ -m pip install praw requests python-dotenv
* !/your directory/ -m pip install pip install nltk
* !/your directory/ -m pip install openai

After that make sure you are importing:

* import os
* from dotenv import load_dotenv

and loading all API from your internal and external sources

# Make sure you are testing all connection beforehand
We would recommend that you are testing all API connections before you run the next cell. This is what we have done at "Connection to Reddit"

Lets skip all other parts since they are described in the Jupiter notebook and jump right into the functionality of the script.

# These are core steps in this workflow (Explained for beginners like us :D)

**Step 1: Gather all feedback**
The script starts by collecting every single comment from all the Reddit posts and all the Product Hunt reviews and puts them into one big master list

**Step 2: Analyze each comment with full context**
For every comment in the master list, the script sends it to the AI (in our case ChatGPT) along with the original post it was replying to. This is the **most important step**, as it gives the AI the full background story for the comment.

**Step 3: Label the comment and filter for relevance (happens at the same time)**
Based on the full context from Step 2, the AI performs two jobs in a single action:

* It first decides if the comment is actually about the n8n product. If it's just a "thank you" or a complaint about the subreddit, it labels it as Irrelevant.
* If the comment is about n8n, it gives it a useful label like "Feature Request" or "Struggle / Confusion". The script then saves only the relevant items.

**Step 4: Summarize the final, relevant results**
As the very last step, after all the comments have been analyzed and filtered, the script takes the lists of relevant feedback (e.g., all "Struggle / Confusion" items) and sends them back to the AI to ask it to write the final, actionable summaries for your dashboard.

The final result is a CSV file which will be created. This particular CSV will be used in the "dasboard.py" to display the findings in a visual appealing way. 
