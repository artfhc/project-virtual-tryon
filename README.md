# Virtual Try-On Application 👗

A Streamlit-based virtual try-on application powered by Google's Gemini 2.0 Flash image generation model. Upload photos of yourself and clothing items to see realistic virtual try-on results.

## Features

- 📸 **Easy Upload Interface**: Simple drag-and-drop for user photos and clothing items
- 🤖 **AI-Powered Generation**: Uses Gemini 2.0 Flash for realistic virtual try-on results
- 🎨 **Image Processing**: Advanced pre/post-processing for optimal results
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 💾 **Download Results**: Save your virtual try-on images

## Project Structure

```
virtual-tryon-app/
├── app.py                 # Streamlit main entry point
├── requirements.txt       # Dependencies (streamlit, openai, pillow, etc.)
├── config.py              # API keys, model config, constants
├── services/
│   ├── gemini_client.py   # Wrapper for gemini-2.0-flash API calls
│   ├── image_utils.py     # Pre/post-processing (resize, mask, overlay)
│   └── pipeline.py        # Virtual try-on pipeline orchestration
├── assets/
│   ├── sample_user.jpg    # Example input
│   ├── sample_cloth.png   # Example clothing
│   └── logo.png
├── tests/
│   ├── test_pipeline.py   # Unit tests for try-on pipeline
│   └── test_utils.py
└── README.md              # How to run
```

## Prerequisites

- Python 3.8+
- Google AI API key (for Gemini access)
- pip or conda for package management

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd virtual-tryon-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Or export the environment variable:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Navigate to API keys section
4. Create a new API key
5. Copy and use it in your `.env` file

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Interface

1. **Upload User Photo**: Click "Choose your photo" and select an image of yourself
2. **Upload Clothing Item**: Click "Choose clothing item" and select the garment you want to try on
3. **Generate Try-On**: Click the "Generate Try-On" button
4. **Download Result**: Once generated, you can download the result image

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- Maximum file size: 10MB

## API Configuration

The application uses several configurable parameters in `config.py`:

```python
MODEL_CONFIG = {
    "model_name": "gemini-2.0-flash-exp",
    "temperature": 0.7,
    "max_output_tokens": 1024,
}

IMAGE_CONFIG = {
    "max_image_size": (1024, 1024),
    "supported_formats": ["JPEG", "PNG", "JPG"],
    "output_format": "PNG",
    "quality": 95
}
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python -m unittest tests/test_pipeline.py
python -m unittest tests/test_utils.py
```

### Project Architecture

- **`app.py`**: Streamlit frontend interface
- **`services/gemini_client.py`**: Handles API communication with Gemini
- **`services/image_utils.py`**: Image preprocessing and postprocessing utilities
- **`services/pipeline.py`**: Main virtual try-on pipeline orchestration
- **`config.py`**: Configuration management
- **`tests/`**: Unit tests for core functionality

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your Gemini API key is correctly set in the environment
   - Verify the key has proper permissions

2. **Image Upload Issues**
   - Check that images are in supported formats (JPEG, PNG)
   - Ensure images are under the maximum file size limit

3. **Generation Errors**
   - Try with different images if generation fails
   - Check your internet connection
   - Verify API quota limits

### Performance Tips

- Use high-quality, well-lit photos for best results
- Ensure clothing items have clear backgrounds when possible
- Optimal image size is around 512x512 to 1024x1024 pixels

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References

- [How to Build with Nano Banana - Complete Developer Tutorial](https://dev.to/googleai/how-to-build-with-nano-banana-complete-developer-tutorial-646)
- [Awesome Nano Banana Images](https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/main/README_en.md)

## Acknowledgments

- Google AI for the Gemini 2.0 Flash model
- Streamlit for the web framework
- PIL/Pillow for image processing capabilities