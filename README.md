# Hackathon Quix Visualization Template

This basic template includes:

A real-time data processing pipeline with the following services:

- **Demo Data Source**: A car telemetry data source for demonstration purposes.
- **Starter Visualization**: A simple template that reads from a Kafka topic and sends data to a web page. This page can be customized via ChatGPT to create various visualizations.

## How the Starter Visualization Works

This application receives data from a Kafka topic and sends it to a WebSocket connection without any transformation. The same application serves an HTML webpage located at `./templates/index.html`, which reads from the WebSocket and creates a real-time visualization.

## How to Use It

1. **Start the Visualization Application**: Ensure your data source is running.
2. **View Initial Visualization**: The time-series data will be displayed on the screen.
3. **Customize Visualization**:
    - Copy the content of `./templates/index.html` and paste it into ChatGPT, describing how you want your visualization to be customized.
    - Use the modified code provided by ChatGPT to replace the content in `./templates/index.html`.
    - Refresh the webpage to see the updated visualization.
4. **Iterate**: Repeat this process until you achieve the desired visualization.

## Example

- **Initial Visualization**: This is the default visualization provided by the template.

  ![Initial visualization](./images/image.png)

- **ChatGPT conversation**: [View Conversation](https://chatgpt.com/share/de44d4c7-fcbf-4eb5-8919-f999ab4b1bfb)

- **Improved Visualization**: After a few iterations with ChatGPT, the visualization was enhanced. However, there's potential to achieve even more with additional creativity and imagination.

  ![Improved visualization](./images/image-1.png)
