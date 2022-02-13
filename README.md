# DEEP WORK TRACKER
#### Video Demo:  https://youtu.be/2cY0h8IHdbo
#### Description:
After reading the book Deep Work by Cal Newport I a have leart about the importance of focus and purpose working.
I have created this web app to be able to record the number of daily 25 minutes work sessions I do with a social feature to be able to see and compare how much your friends are also working. The social aspect of the app allows for accountability accross peers one of the key features of sustainable habits.

I have used all the main web app tools learned in CS50 (CSS, JavaScript, SQL, Flask, Html). On top of this I have added the javasript chart library chart.js.


The program has an application.py where the backend logic is build.
I then has the different html screens saved on the templates folder. There are 3 main screen developed:
- index.html: where the basic summary of each customer is showed.
- login.html and register.html: where the login logic is build.
- social.html: where you can see a comparison of the performance of all users in the app.
- layout.html: with the basic looks and formatting of the html files.

I have tried to put duplicated logic all together in helper functions that are saved in the static folder containing contants.js, favicon.ico, styles.css tools.js and the helpers.py doc.

All the information is saved locally in a database file called deep.db

My plan now is to keep developing this app putting it online and mantaining It adding frequently new features. Initially I am looking to move the database to AWS, put the app in a docker container, deploy a haroku server. After that I will lauch the app to my close friends and start working with their feedback on improving the functionalities It has.

The main functionalities I have decided I want to add are:
- Friendship logic (request, accept, suggestions)
- Historic deep work view
- Load Sheets data into the app
- Think more clearly about how customers register their time worked
- Chronometer with add feature issue.

Cal Newport Deep work inspiration:

Like most people, you’re probably easily distracted by wandering thoughts or social media updates while trying to be productive. In Deep Work, Cal Newport teaches you how to develop your focus and resist distractions so that you can rise to the top of your field and drive toward your most important goals. He contends that focus is like a mental muscle: Through deliberate training, you can strengthen your focus and expand your mental capacity.

Newport explains why the ability to do deep work (work that requires intense concentration) is so important in our modern economy, and he shows how to make deep work a part of your life. In addition to exploring Newport’s ideas on how to eliminate distractions, this guide adds advice from other authors on how to work despite present distractions. We also include practical ways that everyday knowledge workers, not just academics like Newport, can prioritize deep work.


Thank you