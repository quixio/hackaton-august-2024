# Hackaton Quix visualization template

This basic template contains:

A real time data processing pipeline with these services:

 - Demo data source - Car telemetry data source just for the purpose to demonstrate the visualization template
 - Starter Visualization - A simple template that reads from Kafka topic and send it to a simple web page that can be refactored via ChatGPT to draw any visualization

## How the Starter Visualization works

This application receives data from a topic and send it to a Websocket connection directly without any transformation.
The same application holds an HTML webpage ./templates/index.html that reads from the Websocket and create a visualization on the webpage in realtime.

## How to use it

- Run the visualization application once your source is running
- You will see your timeseries data drawn in the screen
- Copy paste the content of the ./templates/index.html and paste it to ChatGPT indicating how you want your visualization to be
- Paste the result provided by ChatGPT to your ./templates/index.html and refresh the web page.
- Interate on this process until you get the visualization you want.

## Example

- This is the initial visualization provided by the template

![Initial visualization](image.png)

- This is the final visualization after a few interactions with ChatGPT (https://chatgpt.com/share/de44d4c7-fcbf-4eb5-8919-f999ab4b1bfb)




