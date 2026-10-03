### EMMA GARCIA HILTNER FINAL PROJECT MAT2007

# Import packages for data handling, plotting, and numerical operations
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


### ~~~~~~~~~~~~~~~~~~ open/load data ~~~~~~~~~~~~~~~~~~~~~~~~~
# Read results calculated in R
results = pd.read_csv(
    "/Users/emmagarcia/Desktop/MAT2007/heart_disease_results.txt", # change to own location if saved data from R file
    sep="\t")

# raw patient data exported from R
scatter_data = pd.read_csv(
    "/Users/emmagarcia/Desktop/MAT2007/heart_scatter_data.txt", # change to own location if saved from R file 
    sep="\t")

# Check that files loaded correctly
print(results)
print(scatter_data.head())


### ~~~~~~~~~~~~~~~ understandable trait names ~~~~~~~~~~~~~~~~~

# Create clearer names for the clinical traits
trait_names = {
    "age": "Age",
    "trestbps": "Resting blood pressure",
    "chol": "Serum cholesterol",
    "thalach": "Maximum heart rate",
    "oldpeak": "ST depression"}

# Match each original trait name with its clearer plot name
plot_names = [
    trait_names[trait]
    for trait in results["Trait"]]


### ~~~~~~~~~~~~~~~~~ general graph editing ~~~~~~~~~~~~~~~~~
# Set the default font size for all graphs
plt.rcParams["font.size"] = 10

# Define colors used in the graphs
normal_color = "#7FA6C9"
highlight_color = "#354F7C"
grid_color = "#D9D9D9"


### ~~~~~~~~~~~~~~~~~~~~~ Bar chart of AUC ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Calculate distance from the AUC value to the lower confidence limit
auc_lower_error = results["AUC"] - results["AUC_lower"]
# Calculate distance from the AUC value to the upper confidence limit
auc_upper_error = results["AUC_upper"] - results["AUC"]
# Combine lower and upper errors into format needed for error bars
auc_error = np.array([
    auc_lower_error,
    auc_upper_error])

# Find the row with the highest AUC
best_trait = results["AUC"].idxmax()

# Give all bars the normal color, then highlight the highest AUC
bar_colors = [normal_color] * len(results)
bar_colors[best_trait] = highlight_color

# Create the figure and plotting area
fig, ax = plt.subplots(figsize=(9, 5.5))

# Create horizontal bars with confidence interval error bars
bars = ax.barh(
    plot_names,
    results["AUC"],
    xerr=auc_error,
    capsize=3,
    color=bar_colors,
    edgecolor="none",
    height=0.65,
    error_kw={
        "elinewidth": 1.2,
        "capthick": 1.2})

# Add a dashed reference line at AUC = 0.5
ax.axvline(
    x=0.5,
    linestyle="--",
    color="gray",
    linewidth=1.2)

# Label AUC = 0.5 reference line above the graph
ax.text(
    0.5,
    1.01,
    "AUC = 0.5\nNo discrimination",
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
    fontsize=9,
    color="dimgray",
    bbox={
        "facecolor": "white",
        "edgecolor": "none",
        "pad": 2})

# Add each AUC value after the end of its confidence interval
for i, auc in enumerate(results["AUC"]):
# Set the text position just beyond the upper confidence limit
    text_x = results.loc[i, "AUC_upper"] + 0.015
# Add AUC value and bold the strongest result
    ax.text(
        text_x,
        i,
        f"{auc:.2f}",
        va="center",
        ha="left",
        fontsize=9,
        fontweight="bold" if i == best_trait else "normal"
    )

# X-axis label
ax.set_xlabel("AUC", fontsize=11)

# Add graph title with extra space above plot
ax.set_title(
    "Ability of Clinical Traits to Distinguish Heart Disease",
    fontsize=14,
    pad=35)

# Find largest upper AUC confidence limit
max_auc = results["AUC_upper"].max()

# Set the x-axis range and leave room for value labels
ax.set_xlim(
    0.4,
    max_auc + 0.10)

# Set x-axis tick marks in intervals of 0.1
ax.set_xticks(
    np.arange(
        0.4,
        max_auc + 0.11,
        0.1))

#Add vertical dotted grid lines
ax.xaxis.grid(
    True,
    linestyle=":",
    linewidth=0.8,
    alpha=0.6)

# Place the grid behind the bars
ax.set_axisbelow(True)

# Remove unnecessary graph borders (FALSE gets rid of it)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Remove tick marks beside the trait names
ax.tick_params(axis="y", length=0)

# Automatically improve spacing
plt.tight_layout()

# Save AUC graph as a high-resolution image
plt.savefig(
    "/Users/emmagarcia/Desktop/MAT2007/AUC_python.png", # change to own location 
    dpi=300,
    bbox_inches="tight"
)

plt.show()

### ~~~~~~~~~~~~~~~~~~~~~ Bar chart severity ~~~~~~~~~~~~~~~~~~~~~~~~

# Calculate the distance to the lower Spearman confidence limit
spearman_lower_error = (
    results["Spearman"] -
    results["Spearman_lower"]
)
# Calc the distance to the upper Spearman confidence limit
spearman_upper_error = (
    results["Spearman_upper"] -
    results["Spearman"]
)
# Combine lower and upper errors for the error bars
spearman_error = np.array([
    spearman_lower_error,
    spearman_upper_error
])

# Find the strongest correlation regardless of whether it is positive or negative
best_severity = results["Spearman"].abs().idxmax()
# Give all bars the normal color, then highlight the strongest correlation
severity_colors = [normal_color] * len(results)
severity_colors[best_severity] = highlight_color

# Create the figure and plotting area
fig, ax = plt.subplots(figsize=(9, 5.5))

# Create horizontal bars with confidence interval error bars
bars = ax.barh(
    plot_names,
    results["Spearman"],
    xerr=spearman_error,
    capsize=3,
    color=severity_colors,
    edgecolor="none",
    height=0.65,
    error_kw={
        "elinewidth": 1.2,
        "capthick": 1.2})

# Add a dashed reference line at correlation = 0
ax.axvline(
    x=0,
    linestyle="--",
    color="gray",
    linewidth=1.2)

# Add each correlation value outside its confidence interval
for i, value in enumerate(results["Spearman"]):

# Put positive values after upper confidence limit
    if value >= 0:
        text_x = results.loc[i, "Spearman_upper"] + 0.025
        horizontal = "left"

# Put negative values before lower confidence limit
    else:
        text_x = results.loc[i, "Spearman_lower"] - 0.025
        horizontal = "right"

# correlation value and bold strongest result
    ax.text(
        text_x,
        i,
        f"{value:.2f}",
        va="center",
        ha=horizontal,
        fontsize=9,
        fontweight="bold" if i == best_severity else "normal")

# Add x-axis label
ax.set_xlabel(
    "Spearman correlation",
    fontsize=11)

# Add graph title
ax.set_title(
    "Association of Clinical Traits with CHD Severity",
    fontsize=14,
    pad=15)

#largest absolute confidence interval value
max_spearman = max(
    abs(results["Spearman_lower"].min()),
    abs(results["Spearman_upper"].max()))

# Symmetrical x-axis + leave room for value labels
ax.set_xlim(
    -max_spearman - 0.18,
    max_spearman + 0.18
)

# Vertical dotted grid line
ax.xaxis.grid(
    True,
    linestyle=":",
    linewidth=0.8,
    alpha=0.6)

# Place grid behind the bars
ax.set_axisbelow(True)

# Remove unnecessary graph borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Remove tick marks beside trait names
ax.tick_params(axis="y", length=0)

# Automatically improve spacing
plt.tight_layout()

# Save severity graph as a high-resolution image
plt.savefig(
    "/Users/emmagarcia/Desktop/MAT2007/Severity_python.png", # change to own location
    dpi=300,
    bbox_inches="tight")

plt.show()

### ~~~~~~~~~~~~~~~~~~~~~~~~ scatterplot ~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define colors for CHD categories 0-4
disease_colors = [
    "#D9D9D9",
    "#E5B168",
    "#D87962",
    "#A94F74",
    "#57417C"]

# Create the figure and plotting area
fig, ax = plt.subplots(figsize=(9, 5.5))

# Loop, each CHD category
for category in range(5):

# Select only patients belonging to the current category
    category_data = scatter_data[
        scatter_data["num"] == category]

# Plot max heart rate against ST depression
    ax.scatter(
        category_data["thalach"],
        category_data["oldpeak"],
        color=disease_colors[category],
        label=str(category),
        s=50,
        alpha=0.75,
        edgecolor="white",
        linewidth=0.6)

# x-axis label
ax.set_xlabel(
    "Maximum heart rate",
    fontsize=11)

# y-axis label
ax.set_ylabel(
    "ST depression",
    fontsize=11)

# Add graph title
ax.set_title(
    "Maximum Heart Rate vs ST Depression by CHD Category",
    fontsize=14,
    pad=15)

# Add the CHD category legend outside the plotting area
ax.legend(
    title="CHD category",
    frameon=False,
    bbox_to_anchor=(1.02, 1),
    loc="upper left")

# Add dotted grid lines
ax.grid(
    True,
    linestyle=":",
    linewidth=0.8,
    alpha=0.45)

# Place grid behind the data points
ax.set_axisbelow(True)

# Remove unnecessary graph borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Automatically improve spacing
plt.tight_layout()

# Save scatterplot as a high-resolution image
plt.savefig(
    "/Users/emmagarcia/Desktop/MAT2007/Scatter_python.png", # change to own location 
    dpi=300,
    bbox_inches="tight")

plt.show()