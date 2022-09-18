# Python Notebook - GA SCRUTINY

# Import library
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from itertools import cycle, islice
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
%matplotlib inline

datasets

df = datasets[2]
df.shape

import notebooksalamode as mode
df3 = datasets[3]
mode.export_csv(df3)


df.head()

# Data summary
df.describe().transpose()

df['POPULAR_PROPERTY_STATE'].unique()

# Remove null rows
previous_rows = df.shape[0]
df = df.dropna()
after_rows = df.shape[0]
# Number of NA rows
print(previous_rows - after_rows)


# Select interesting features for K-Means
#features = ['PROPORTION_SEARCH_SALE', 'PROPORTION_SEARCH_LEASE', 'PROPORTION_SEARCH_SOLD', 'PROPORTION_SEARCH_BUSINESS', 'PROPORTION_LISTING_SALE', 'PROPORTION_LISTING_LEASE', 'PROPORTION_LISTING_SOLD', 'PROPORTION_LISTING_BUSINESS', 'PROPORTION_NEWS']
features = ['PROPORTION_SEARCH_SALE', 'PROPORTION_SEARCH_LEASE', 'PROPORTION_SEARCH_BUSINESS', 'PROPORTION_LISTING_SALE', 'PROPORTION_LISTING_LEASE', 'PROPORTION_LISTING_BUSINESS']
select_df = df[features]
select_df.shape

select_df.describe().transpose()

# Scale data
X = StandardScaler().fit_transform(select_df)
X

# Fit data into Kmean model
kmeans = KMeans(n_clusters=6)
model = kmeans.fit(select_df) 
print(model)

y_kmeans = kmeans.predict(select_df)

clusters, counts = np.unique(y_kmeans, return_counts=True)
print(clusters)
print(counts)

# Cluster centers
centers = model.cluster_centers_
centers

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
	plt.figure(figsize=(30,8)).gca().axes.set_ylim([0,+1])
	parallel_coordinates(data, 'prediction', color = my_colors, marker='o')

P = pd_centers(features, centers)
P

parallel_plot(P)

random_state = 5
# Clustering - grid search of optimal hyperparameters
param_grid = np.array([(n_clusters, batch_size, score)
                       for n_clusters in range(6, 9)
                       for batch_size in [100, 500]
                       for score in [None]
                       ])

for index, (n_clusters, batch_size, score) in enumerate(param_grid):
    print('\nn_clusters = ' + str(n_clusters))
    print('batch_size = ' + str(batch_size))
    model =  MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size, random_state=random_state)
    try:
        model.fit(X)
        labels = model.labels_
        score = metrics.silhouette_score(X, labels, sample_size = n if n < cap_silhouette else cap_silhouette)
        print("Silhouette Coefficient: %0.3f" % score)
        param_grid[index, 2] = score
    except Exception as e:
        print(e)

df_param_grid = pd.DataFrame(param_grid,
                             columns=['n_clusters', 'batch_size', 'score'])\
    .sort_values(by=['score'], ascending=False)

# Clustering - optimal model
best_params = df_param_grid.ix[4]
best_model = MiniBatchKMeans(n_clusters=best_params[0], batch_size=best_params[1], random_state=random_state)
# best_model = MiniBatchKMeans(n_clusters=6, batch_size=500, random_state=random_state)
best_model.fit(X)
labels = best_model.labels_

