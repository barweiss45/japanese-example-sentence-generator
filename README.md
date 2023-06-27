# Japanese Example Sentence Generator

## Installation

**Before you start!** You will need a [Openai API key](https://platform.openai.com/overview) and [Forvo API key](https://api.forvo.com/). Please refer to the [.env_template](.env_template) file.

1. First, clone this repository.

    ```git
    git clone https://github.com/barweiss45/japanese-example-sentence-generator.git
    ```

2. Once you have set up your OpenAI and Forvo API accounts you will need create a `.env` file in the root directory of the repository.

3. If you would like to run this application in a container, then you will need to have docker installed on your system. See these instructions for further infomation about Docker. Once Docker is installed run the following commands.

    ```docker
    docker compose build
    docker compose up -d
    ```

4. If you are running docker, then open your browser to [http://localhost:8501](http://localhost:8501) and enjoy. If you want to run the application with out Docker then you will need to run the following commands in the repository.

   ```bash
   pip install -r requirements.txt
   streamlit run Home.py
   ```

## License

This application uses the MIT Opensource software licensing, and is open source. Contributions to code are welcome.