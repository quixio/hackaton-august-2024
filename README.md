# Hackathon Quix visualization template

This template includes a real-time data processing pipeline with the following services:

- **`demo-data-source`**: A car telemetry data source for demonstration purposes.
- **`starter-visualization`**: A simple template that reads from a Kafka topic and sends data to a web page. This page can be customized via ChatGPT to create various visualizations.

```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR;
demo-data-source[fa:fa-rocket demo-data-source &#8205] --> f1-data{{ fa:fa-arrow-right-arrow-left f1-data &#8205}}:::topic;
f1-data{{ fa:fa-arrow-right-arrow-left f1-data &#8205}}:::topic --> starter-visualization[fa:fa-rocket starter-visualization &#8205];


classDef default font-size:110%;
classDef topic font-size:80%;
classDef topic fill:#3E89B3;
classDef topic stroke:#3E89B3;
classDef topic color:white;
```

## How the starter-visualization works

This application receives data from a Kafka topic and sends it to a WebSocket connection without any transformation. The same application serves an HTML webpage located at `./templates/index.html`, which reads from the WebSocket and creates a real-time visualization.

## How to use it

1. **Run the visualization application**: Ensure your data source is running.
2. **View initial visualization**: The time-series data will be displayed on the screen.
3. **Customize the visualization**:
    - Copy the content of `./templates/index.html` and paste it into ChatGPT, describing how you want your visualization to be customized.
    - Use the modified code provided by ChatGPT to replace the content in `./templates/index.html`.
    - Refresh the webpage to see the updated visualization.
4. **Iterate**: Repeat this process until you achieve the desired visualization.

## Example

- **Initial visualization**: This is the default visualization provided by the template.

  ![Initial visualization](./images/image.png)

- **ChatGPT conversation**: [View Conversation](https://chatgpt.com/share/de44d4c7-fcbf-4eb5-8919-f999ab4b1bfb)

- **Improved visualization**: After a few iterations with ChatGPT, the visualization was enhanced. However, there's potential to achieve even more with additional creativity and imagination.

  ![Improved visualization](./images/image-1.png)
