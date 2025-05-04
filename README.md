# German Syllable Splitter

## Overview
The German Syllable Splitter is a tool designed to split German words into their respective syllables. This can be useful for linguistic analysis, educational purposes, or text-to-speech applications.

## Features
- Splits German words into syllables accurately.
- Supports integration with other applications via an API.
- Lightweight and easy to use.

## Project Structure
- **api/**: Contains the API implementation for the syllable splitter.
  - `syllable_splitter/`: Core logic for splitting syllables.
  - `utilities/`: Helper functions and utilities.
- **app/**: Frontend application files.
  - `globals.css`: Global styles using Tailwind CSS.
  - `layout.tsx`, `page.tsx`: Layout and main page components.
- **dictionary/**: Contains German dictionary files (`de_DE.aff`, `de_DE.dic`) used for linguistic processing.
- **public/**: Static assets like icons.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/german-syllable-splitter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd german-syllable-splitter
   ```
3. Install dependencies using pnpm:
   ```bash
   pnpm install
   ```

## Usage
### Running the Application
1. Start the development server:
   ```bash
   pnpm dev
   ```
2. Open your browser and navigate to `http://localhost:3000`.

### API Usage
The API provides endpoints for splitting German words into syllables. Refer to the `api/` folder for implementation details.

## Flask Integration
This project also uses Python Flask for the backend API. Flask is a lightweight WSGI web application framework in Python. It is used here to handle API requests for splitting German words into syllables.

### Running the Flask API
1. Navigate to the `api/` directory:
   ```bash
   cd api
   ```
2. Run the Flask application:
   ```bash
   flask run
   ```
3. The API will be available at `http://127.0.0.1:5000` by default.

### Flask API Endpoints
- **`/split`**: Accepts a POST request with a German word and returns its syllables.

Refer to the `index.py` file in the `api/` directory for more details on the Flask implementation.

## Technologies Used
- **Next.js**: Framework for building the frontend.
- **Tailwind CSS**: Utility-first CSS framework.
- **TypeScript**: For type-safe JavaScript development.
- **pnpm**: Fast, disk space-efficient package manager.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.