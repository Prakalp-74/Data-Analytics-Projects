# Netflix Movies & TV Shows Analysis
# Goal: Explore trends in content type, release patterns, 
# countires, durations, and more
import pandas as pd
import matplotlib.pyplot as plt

# Load Dateset
df = pd.read_csv("netflix_titles.csv")

# Drop duplicates
df = df.drop_duplicates()

# Fill missing values with simple replacements
df["country"] = df["country"].fillna("Unknown")
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")

# Fill date_added with most common date
df["date_added"] = df["date_added"].fillna(df["date_added"].mode()[0])

# Fill duration with most common duration
df["duration"] = df["duration"].fillna(df["duration"].mode()[0])

# Convert date_added to datetime
df["date_added"] = df["date_added"].str.strip()
df["date_added"] = pd.to_datetime(df["date_added"])

# Extract year and month
df["year"] = df["date_added"].dt.year
df["month"] = df["date_added"].dt.month

# create subplot (4 rows * 2 columns)
fig, axes = plt.subplots(4, 2, figsize=(14, 20))
fig.suptitle("Netflix Data Analysis", fontsize=15, fontweight="bold")

fig.text(0.01, 0.05,
"Conclusion:\n"
    "- Netflix has more Movies than TV Shows.\n"
    "- Content growth increased after 2015.\n"
    "- Most movies are between 80–120 minutes.\n"
    "- TV Shows mostly have 1–3 seasons.\n"
    "- Content is uploaded consistently every month.",
    ha='left', va='bottom',
    fontsize=12
)

# Bar chart of Movies and TV Series
counts = df["type"].value_counts()
colors = ["b", "c"]
axes[0, 0].bar(counts.index, counts.values, edgecolor ="k", width=0.6, color=colors)
axes[0, 0].set_title("Movies and TV series Graph")
axes[0, 0].set_xlabel("Types")
axes[0, 0].set_ylabel("Number of Movies and TV series")


#  Pie chart of Movies and TV Series
axes[0, 1].pie(counts.values, labels = counts.index, shadow=True, autopct="%.2f%%")
axes[0, 1].set_title("Distribution of Content Type")

# Line graph Yearly Content Growth
yearly = df.groupby("year")["title"].count()
axes[1, 0].plot(yearly.index, yearly.values, c="r")
axes[1, 0].set_title( "Netflix Content Added per Year")
axes[1, 0].set_xlabel("years")
axes[1, 0].set_ylabel("Number of titles")
axes[1, 0].grid(True)


# Bar chart: Monthly Release Trend
monthly = df.groupby("month")["title"].count()
axes[1, 1].bar(monthly.index,monthly.values, edgecolor="k")
axes[1, 1].set_title("Netflix Content Added per month")
axes[1, 1].set_xlabel("Months")
axes[1, 1].set_ylabel("Number of titles")


# Histogram: Movies Durations
movie_df = df[df["type"] == "Movie"].copy()
# Clean duration column (remove "min" and convert to number)
movie_df["duration"] = movie_df["duration"].str.replace("min","").str.strip()
movie_df["duration"] = pd.to_numeric(movie_df["duration"], errors="coerce")
axes[2, 0].hist(movie_df["duration"], bins=20, edgecolor="k",color="c")
axes[2, 0].set_title("Distribution of Movie Durations")
axes[2, 0].set_xlabel("Duration (minutes)")
axes[2, 0].set_ylabel("Frequency")

# Bar chart of TV Series Duration
tv_df = df[df["type"] == "TV Show"].copy()
# Clean duration column (remove "Seasons", "seanson" to "")
tv_df["duration"] = tv_df["duration"].str.replace("Seasons", "")
tv_df["duration"] = tv_df["duration"].str.replace("Season", "")
tv_df["duration"] = tv_df["duration"].str.strip()
tv_df["duration"] = pd.to_numeric(tv_df["duration"], errors="coerce")
season_counts = tv_df["duration"].value_counts().sort_index()
axes[2, 1].bar(season_counts.index, season_counts.values, color="y", edgecolor="k")
axes[2, 1].set_title("Number of Seasons in TV Shows")
axes[2, 1].set_xlabel("Seasons")
axes[2, 1].set_ylabel("counts")

# 7 & 8 . Empty plots (remove and hidden)
axes[3, 0].axis("off") 
axes[3, 1].axis("off")

plt.tight_layout()
# It automatically adjust spacing between subplots
plt.show()
