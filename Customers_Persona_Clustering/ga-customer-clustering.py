# Python Notebook - CRE - GA Customer Clustering

# Import library
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn import metrics
import pandas as pd
import numpy as np
from itertools import cycle, islice
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

datasets

df = datasets[3]
df.shape

df.head()

# Data summary
# Remove null rows
previous_rows = df.shape[0]
df = df.dropna()
after_rows = df.shape[0]
# Number of NA rows
print(previous_rows - after_rows)

# Select interesting features for K-Means
#features = ['PROPORTION_SEARCH_SALE', 'PROPORTION_SEARCH_LEASE', 'PROPORTION_SEARCH_SOLD', 'PROPORTION_SEARCH_BUSINESS', 'PROPORTION_LISTING_SALE', 'PROPORTION_LISTING_LEASE', 'PROPORTION_LISTING_SOLD', 'PROPORTION_LISTING_BUSINESS', 'PROPORTION_NEWS']
features = ['PROPORTION_SEARCH_SALE', 'PROPORTION_LISTING_SALE', 'PROPORTION_SEARCH_LEASE','PROPORTION_LISTING_LEASE', 'PROPORTION_SEARCH_BUSINESS',  'PROPORTION_LISTING_BUSINESS', 'NUMBER_OF_SUBURB']
select_df = df[features]
select_df.shape

select_df.describe().transpose()

plt.boxplot(select_df['NUMBER_OF_SUBURB'])

print(df.shape)
df.head()

# Scale data
X = StandardScaler().fit_transform(select_df)
X
random_state = 5
n = 10000
cap_silhouette = 20000
# Clustering - grid search of optimal hyperparameters
param_grid = np.array([(n_clusters, batch_size, score)
                       for n_clusters in range(5, 11)
                       for batch_size in [100, 500]
                       for score in [None]
                       ])
clusters = []
coefficient_scores = []

# Grid search of optimal parameters
for index, (n_clusters, batch_size, score) in enumerate(param_grid):
    #print('\nn_clusters = ' + str(n_clusters))
    #print('batch_size = ' + str(batch_size))
    model =  MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size, random_state=random_state)
    try:
        model.fit(X)
        labels = model.labels_
        score = metrics.silhouette_score(X, labels, sample_size = n if n < cap_silhouette else cap_silhouette)
        #print("Silhouette Coefficient: %0.3f" % score)
        param_grid[index, 2] = score
    except Exception as e:
        print(e)

df_param_grid = pd.DataFrame(param_grid,
                             columns=['n_clusters', 'batch_size', 'score'])\
    .sort_values(by=['score'], ascending=False)

# Show the Grid search of optimal parameters
grid1 = df_param_grid[df_param_grid['batch_size'] == 500]
grid1 = grid1.sort_values('n_clusters')
grid2 = df_param_grid[df_param_grid['batch_size'] == 100]
grid2 = grid2.sort_values('n_clusters')

x = grid1['n_clusters'].values
y1 = grid1['score'].values
y2 = grid2['score'].values

fig, ax = plt.subplots()

# Using set_dashes() to modify dashing of an existing line
line1, = ax.plot(x, y1, label='Batch size 500')
line1.set_dashes([2, 2, 10, 2])  # 2pt line, 2pt break, 10pt line, 2pt break
ax.scatter(grid1['n_clusters'].values, grid1['score'].values)

# Using plot(..., dashes=...) to set the dashing when creating a line
line2, = ax.plot(x, y2, dashes=[6, 2], label='Batch size 100')
ax.scatter(grid1['n_clusters'].values, grid2['score'].values)

plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Coefficient')
plt.title('Grid search of optimal parameters')
ax.legend(loc='lower right')
plt.show()

# The graph shows that 6, 7, or 8 clusters could be useful

# PERFORM CLUSTERING WITH 6 CLUSTERS

# Scale data
X = StandardScaler().fit_transform(select_df)

# Fit data into Kmean model with 6 clusters
kmeans = KMeans(n_clusters=6)
model = kmeans.fit(X)

df_x(:,)


# Characterise clusters
labels = model.labels_
df_x = df
df_x['cluster'] = labels
clusters_unique = np.unique(labels)
clusters_size = [None] * len(clusters_unique)
for cluster in clusters_unique:
    clusters_size[cluster] = len(df_x[df_x.cluster == cluster])

df_summary = pd.DataFrame(
    {
        'cluster': clusters_unique,
        'size': clusters_size,
        'prop_of_users': [x / n for x in clusters_size]
    }
)

# Get only number columns
df_culmulative =  df_x.iloc[:,1:20]
del df_culmulative['POPULAR_PROPERTY_STATE']


for index, cluster in enumerate(df_summary.cluster):
    for col_name in list(df_culmulative.columns.values):
        if col_name == 'NUMBER_OF_SUBURB':
            df_summary.loc[index, col_name] = np.median(df_x.loc[df_x.cluster == cluster, col_name])
        else:
            df_summary.loc[index, col_name] = np.mean(df_x.loc[df_x.cluster == cluster, col_name])

df_summary = df_summary.round(3)
df_summary = df_summary.round({
    'NUMBER_OF_SUBURB': 0
})
df_summary['label'] = ['Newsers',
                       'Sold Listings Viewers',
                       'Moderate Renters',
                       'Warm Buyers',
                       'Moderate Buyers',
                       'Home Price Guide']
df_summary

df = df_summary.iloc[:,3:10]
df.insert(loc=0, column='group', value=df_summary.iloc[:,0] )
df


# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# Set data
#df = pd.DataFrame({
#'group': ['A','B','C','D'],
#'var1': [38, 1.5, 30, 4],
#'var2': [29, 10, 9, 34],
#'var3': [8, 39, 23, 24],
#'var4': [7, 31, 33, 14],
#'var5': [28, 15, 32, 14]
#})


# ------- PART 1: Create background

# number of variable
categories=list(df)[1:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([0.2,0.3,0.6], ["0.2","0.4","0.6"], color="grey", size=7)
plt.ylim(0,1)

# ------- PART 2: Add plots

# Plot each individual = each line of the data

for i in range(N-1):
    values=df.loc[i].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', label="Cluster" + str(i))
    ax.fill(angles, values, 'b', alpha=0.1)
    

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(2, 1))

centers = df_summary.iloc[:,3:10]
centers = model.cluster_centers_
centers

# OTHER WAY TO VIEW CLUSTERS


# Function that creates a DataFrame with a column for Cluster Number

def pd_centers(featuresUsed, centers):
	colNames = list(featuresUsed)
	colNames.append('prediction')

	# Zip with a column called 'prediction' (index)
	Z = [np.append(A, index) for index, A in enumerate(centers)]

	# Convert to pandas data frame for plotting
	P = pd.DataFrame(Z, columns=colNames)
	P['prediction'] = P['prediction'].astype(int)
	return P

# Function that creates Parallel Plots

def parallel_plot(data):
	my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k', 'r']), None, len(data)))
	plt.figure(figsize=(30,8)).gca().axes.set_ylim([-1,3.5])
	parallel_coordinates(data, 'prediction', color = my_colors, marker='o')

P = pd_centers(features, centers)
P

parallel_plot(P)



