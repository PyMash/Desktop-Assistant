# Miami Desktop Assistant

Miami is a powerful desktop assistant designed to respond to voice commands using Porcupine wake word detection. This repository provides the necessary instructions to run Miami on your system.

## Prerequisites

- [Porcupine](https://picovoice.ai/docs/quick-start/getting-started-porcupine/)
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/miami-desktop-assistant.git
    cd miami-desktop-assistant
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Download Porcupine wake word engine and place it in the project directory. You can obtain the engine from [Porcupine's official website](https://picovoice.ai/console/).

4. Run Miami with the following command:

    ```bash
    porcupine_demo_mic --access_key "your porcupine accesskey" --keywords miami --audio_device_index 1
    ```

Make sure to replace the `--access_key` parameter with your Porcupine access key.

## Usage

Once Miami is running, it will be listening for the wake word "Miami." When it detects the wake word, it will be ready to receive voice commands.

Feel free to customize and extend Miami according to your preferences and use case.

## License

This project is licensed under the [MIT License](LICENSE).
