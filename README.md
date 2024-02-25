# RBA Financial Tables
Generates charts and information about the rba tables.

# Overview
- User selects the dataset they want to look at
    - This links to the 'select_dataset.yaml file, which provides a list of the required yaml files relevant for that selection. The list must only include the yaml files that exist in the 'dataset_yaml' folder. Each of the yaml files in the 'dataset_yaml' folder have a specific structure allowing you to download the required data. having this as a list allows you to downlaod multiple datasets if required for the charts you want to display.
- Function then loads data required for the selected dataset
    - Note the data is saved as pickel each run, therefore if the data is needed again it wont be re-loaded
- With the data avaiable, tabs and charts are maded and displayed to the user.

# Developer setup:

- #003366

1. Classic Blue and Gray Palette
Primary Color: Navy Blue (Hex: #003366) - Conveys trust and reliability.
Secondary Color: Slate Gray (Hex: #708090) - Adds a modern, neutral backdrop.
Accent Colors:
Light Blue (Hex: #8ABAD3FF) for highlights and to soften the overall look.
Silver (Hex: #C0C0C0) for charts and graphs to maintain neutrality and professionalism.
2. Professional Greens Palette
Primary Color: Hunter Green (Hex: #355E3B) - Represents growth and financial success.
Secondary Color: Sage Green (Hex: #B2C2B1) - Provides a calming, neutral base.
Accent Colors:
Emerald (Hex: #50C878) for key data points, symbolizing prosperity.
Cream (Hex: #F5F5DC) for backgrounds, to soften and balance the greens.
3. Earthy Neutrals Palette
Primary Color: Charcoal (Hex: #36454F) - Serious and grounded, great for text.
Secondary Color: Taupe (Hex: #483C32) - Warm and versatile for backgrounds.
Accent Colors:
Beige (Hex: #F5F5DC) to illuminate and create space.
Rust (Hex: #B7410E) for calls to action and important highlights, adding a touch of energy.
4. Modern Monochrome with Accents
Primary Color: Black (Hex: #000000) - Ultimate professionalism, excellent for text.
Secondary Color: Graphite (Hex: #1C1C1C) - Softens the harshness of black for backgrounds.
Accent Colors:
Platinum (Hex: #E5E4E2) for charts and separators, providing clarity.
Vibrant Teal (Hex: #30D5C8) for highlighting important data points, adding a modern twist.
5. Warm Corporate Tones Palette
Primary Color: Burgundy (Hex: #800020) - Exudes sophistication and depth.
Secondary Color: Sandstone (Hex: #786D5F) - Warm and inviting, great for backgrounds.
Accent Colors:
Gold (Hex: #FFD700) for premium highlights and key figures.
Cream (Hex: #FFFFF0) for a soft, clean background in charts and infographics.