start with creating a .env file and add the OPENAI_API_KEY="your_API_key"
create a virtual env using python3 -m venv myenv
then, source myenv/bin/activate
then, pip install -r requirements.txt

run streamlit apps by streamlit run filename.py

For github, first create repository. Run pipreqs (or pipreqs --ignore bin,etc,include,lib,lib64) for the requirements.txt file
add .gitigignore where you add your .env and other secrets.

For streamlit, create .strimlit folder and add secrets.toml file. Add OPENAI_API_KEY="sk--------------"

In your main streamlit app, add import streamlit as st and 
openai.api_key = st.secrets["OPENAI_API_KEY"]

go to your directory and files and then git init
git add .
git commit -m "first commit"
git remote add origin <githib url link>
git push origin master 

deploy in streamlit! Don't forget advanced settings and add your api key, same format as secrets.toml

|reach app here|https://studybuddyuta.streamlit.app/|
https://studybuddyuta.streamlit.app/

to push changes, git add .
git commit -m "second/third/etc commit"
git push origin master 