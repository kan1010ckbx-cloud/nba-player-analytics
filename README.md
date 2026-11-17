# NBA Analytics Project
#### Video Demo: <https://youtu.be/4Th8OrRKPEM>
#### Description:

This project is an NBA Analytics tool built with Python, pandas, seaborn, and matplotlib.  
It was created as my Final Project for CS50P: Introduction to Programming with Python.  

The purpose of this project is to give basketball fans and data enthusiasts a simple way to explore player statistics across different seasons. By using a command-line interface, users can load a dataset of NBA players and interact with it in three major ways: summarizing a single player’s stats, comparing two players on a chosen metric, and plotting seasonal trends using charts.

I chose this topic because basketball has always been a passion of mine, and I wanted to combine that interest with programming practice. Working with real-world data helped me connect coding concepts to something I care about. This made the project not only educational but also personally enjoyable. It also gave me the chance to experiment with pandas DataFrames, which are widely used in professional data science, and seaborn for data visualization.

The project provides three main features:
1. **Summary**: Show a player’s weighted average of points, rebounds, assists, and efficiency across their games. It also lists per-season stats for a clearer view of performance over time.  
2. **Compare**: Take two players as input and compare them on a chosen metric such as points, rebounds, or assists, with the program outputting the numerical difference.  
3. **Plot**: Plot one or more players’ seasonal stats as a line chart using seaborn. The chart can be displayed directly or saved as a PNG file for later use.

From a technical perspective, this project uses **argparse** for building the CLI interface, **pandas** for data loading and manipulation, **seaborn/matplotlib** for visualization, and **pytest** for automated testing. This combination demonstrates skills in CSV parsing, data cleaning, visualization, and software testing—all key areas for Python development.  

During development, I faced challenges such as converting CSV values into numeric types, filtering players correctly across multiple seasons, and ensuring that calculations like weighted averages were mathematically accurate. Writing pytest tests was especially helpful because it forced me to think about edge cases and confirm that the code was producing the correct results.  

In the future, I would like to expand this project by adding a larger dataset with more players and seasons, integrating SQL (such as SQLite or PostgreSQL) for more advanced queries, and improving the visualization with interactive dashboards. These upgrades would make the tool more powerful and closer to what analysts use in real sports analytics.  

Overall, this project reflects my learning journey in Python programming and shows how coding can be applied to real interests. It represents the progress I have made in combining problem-solving, data analysis, and creativity into one meaningful outcome.
