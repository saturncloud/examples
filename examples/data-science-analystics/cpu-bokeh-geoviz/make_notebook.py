import json

# Define the notebook structure with your new standard format
notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<div align=\"left\">\n",
    "  <img src=\"./bokeh-geo-icon.png\" width=\"80\">\n",
    "</div>\n",
    "\n",
    "# 🌍 Bokeh Notebook — Geo Visualization\n",
    "\n",
    "### **Template Review**\n",
    "This template provides a production-ready setup for geospatial data analysis and interactive mapping on **Saturn Cloud**. Optimized for **CPU resources**, it demonstrates how to process geographic coordinates and render high-performance interactive maps. The primary goal is to showcase \"Map Incidents\" with interactive hover filters, allowing users to inspect localized data points dynamically.\n",
    "\n",
    "### **Dataset Overview**\n",
    "The template utilizes a **Geospatial Incident** toy dataset. This dataset contains simulated event coordinates (latitude and longitude), incident types, and severity levels. It serves as a benchmark for testing spatial joins, coordinate reference system (CRS) transformations, and interactive glyph rendering in a mapping environment.\n",
    "\n",
    "### **Tech Stack**\n",
    "* **Python**: The core language for spatial logic and data processing.\n",
    "* **GeoPandas**: Extends Pandas to allow spatial operations on geometric types, handling the transformation of raw coordinates into map-ready shapes.\n",
    "* **Bokeh**: A powerful visualization library used here to create interactive, web-ready maps with custom hover tools and real-time filtering capabilities.\n",
    "\n",
    "---\n",
    "\n",
    "## 🚀 Quick Start\n",
    "The Saturn Cloud environment is pre-configured for Jupyter. Run the following cells to install the specialized geospatial libraries and launch the interactive map.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### **Step 1: Install Required Libraries**\n",
    "In this step, we install the specific libraries needed for geospatial visualization. This includes **Bokeh** for the interactive mapping engine and **GeoPandas** for handling spatial data structures."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Install geospatial and interactive visualization libraries\n",
    "!pip install bokeh geopandas shapely"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### **Step 2: Load and Prepare Geospatial Data**\n",
    "We initialize a GeoDataFrame containing incident coordinates. We ensure the data is projected into the Web Mercator format (EPSG:3857), which is the standard coordinate system used by Bokeh and most web-based map tiles."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import geopandas as gpd\n",
    "from shapely.geometry import Point\n",
    "import pandas as pd\n",
    "\n",
    "# Create toy incident data\n",
    "data = {\n",
    "    'Incident_ID': [1, 2, 3, 4],\n",
    "    'Type': ['Maintenance', 'Emergency', 'Inquiry', 'Maintenance'],\n",
    "    'Severity': ['Low', 'High', 'Medium', 'Low'],\n",
    "    'lat': [37.7749, 37.7849, 37.7649, 37.7549],\n",
    "    'lon': [-122.4194, -122.4094, -122.4294, -122.4394]\n",
    "}\n",
    "\n",
    "df = pd.DataFrame(data)\n",
    "# Convert to GeoDataFrame\n",
    "gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs=\"EPSG:4326\")\n",
    "\n",
    "# Project to Web Mercator for Bokeh compatibility\n",
    "gdf = gdf.to_crs(\"EPSG:3857\")\n",
    "gdf['x'] = gdf.geometry.x\n",
    "gdf['y'] = gdf.geometry.y\n",
    "gdf.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### **Step 3: Build the Interactive Map with Hover Filters**\n",
    "Using Bokeh, we render a map background (tile provider) and overlay the incident points. We configure a **HoverTool** to display incident details when the user moves their cursor over a point."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bokeh.plotting import figure, show\n",
    "from bokeh.models import HoverTool\n",
    "from bokeh.io import output_notebook\n",
    "\n",
    "output_notebook()\n",
    "\n",
    "# Initialize the map figure\n",
    "p = figure(x_axis_type=\"mercator\", y_axis_type=\"mercator\", \n",
    "           title=\"Incident Map: Localized Hover Filters\",\n",
    "           active_scroll=\"wheel_zoom\")\n",
    "\n",
    "# Add OpenStreetMap background tiles\n",
    "p.add_tile(\"OSM\")\n",
    "\n",
    "# Plot incidents as circles\n",
    "p.circle(x='x', y='y', size=10, color=\"red\", alpha=0.7, source=gdf)\n",
    "\n",
    "# Add Hover Tool with filters for ID, Type, and Severity\n",
    "hover = HoverTool()\n",
    "hover.tooltips = [\n",
    "    (\"ID\", \"@Incident_ID\"),\n",
    "    (\"Type\", \"@Type\"),\n",
    "    (\"Severity\", \"@Severity\")\n",
    "]\n",
    "p.add_tools(hover)\n",
    "\n",
    "show(p)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🔗 Resources and Support\n",
    "For further information on the platform or the libraries used in this template, please refer to the following official links:\n",
    "\n",
    "* **Platform**: [Saturn Cloud Dashboard](https://saturncloud.io/)\n",
    "* **Support**: [Saturn Cloud Documentation](https://saturncloud.io/docs/)\n",
    "* **Library**: [Bokeh Documentation](https://docs.bokeh.org/)\n",
    "* **Library**: [GeoPandas Documentation](https://geopandas.org/)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

# Save as .ipynb
with open("bokeh_geo_visualization.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1)

print("SUCCESS: bokeh_geo_visualization.ipynb has been created!")