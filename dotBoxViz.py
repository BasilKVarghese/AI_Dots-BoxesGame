import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv("GameReport.csv")
df = df.drop_duplicates()
df['AgentWin'] = np.where(df['AgentWin'] == 1,1,0)
rename_vals = {"minimax":"Minimax","AB":"AlphaBeta","expt":"Expectimax","expcal":"CalExpectimax"}
df=df.replace({"Algorithm": rename_vals})
df['Algorithm'] = pd.Categorical(df['Algorithm'],
                                   categories=["Minimax", "AlphaBeta",'Expectimax','CalExpectimax'],
                                   ordered=True)

#df['Algorithm'].cat.categories = ["minimax", "AB",'expt','exptcal']
df_3 = df[df['Board_Size'] == '3 X 3']

df_3 = df_3.groupby(['Algorithm','Board_Size','Depth']).agg({'reaction_time':'mean','nodes':'mean','AgentWin':'mean'}).reset_index()
print(df_3)
df_3['AgentWin'] = df_3['AgentWin'] * 100 
plot_3_time = sns.lineplot(x="Algorithm", y="reaction_time", data=df_3, hue = 'Depth' ).get_figure()
plt.xlabel("Algorithms")
plt.ylabel("Reaction Time(ms)")
plt.title("Reaction Time by Algorithm on 3 X 3 board")
plot_3_time.savefig('3_Algo_time.png')
plt.cla()

plot_3_nodes = sns.lineplot(x="Algorithm", y="nodes", data=df_3, hue = 'Depth' ).get_figure()
plt.xlabel("Algorithms")
plt.ylabel("Number of Nodes Expanded")
plt.title("Nodes Expanded by Algorithm on 3 X 3 board")
plot_3_nodes.savefig('3_Algo_nodes.png')
plt.cla()

plot_3_win = sns.lineplot(x="Algorithm", y="AgentWin", data=df_3, hue = 'Depth' ).get_figure()
plt.xlabel("Algorithms")
plt.ylabel("Percentage of Wins")
plt.title("Percentage of wins by Algorithm on 3 X 3 board")
plot_3_win.savefig('3_Algo_Wins.png')
plt.cla()




df_4 = df[df['Board_Size'] == '4 X 4']
df_4 = df_4.groupby(['Algorithm','Board_Size','Depth']).agg({'reaction_time':'mean','nodes':'mean','AgentWin':'mean'}).reset_index()
df_4['AgentWin'] = df_4['AgentWin'] * 100 
print(df_4)
plot_4_time = sns.lineplot(x="Algorithm", y="reaction_time", data=df_4, hue = 'Depth' ).get_figure()
plt.xlabel("Algorithms")
plt.ylabel("Reaction Time(ms)")
plt.title("Reaction Time by Algorithm on 4 X 4 board")
plot_4_time.savefig('4_Algo_time.png')
plt.cla()

plot_4_nodes = sns.lineplot(x="Algorithm", y="nodes", data=df_4, hue = 'Depth' ).get_figure()
plt.xlabel("Algorithms")
plt.ylabel("Number of Nodes Expanded")
plt.title("Nodes Expanded by Algorithm on 4 X 4 board")
plot_4_nodes.savefig('4_Algo_nodes.png')
plt.cla()

plot_4_win = sns.lineplot(x="Algorithm", y="AgentWin", data=df_4, hue = 'Depth' ).get_figure()
plt.xlabel("Algorithms")
plt.ylabel("Percentage of Wins")
plt.title("Percentage of wins by Algorithm on 4 X 4 board")
plot_4_win.savefig('4_Algo_Wins.png')
plt.cla()