# CV Optimizer Cloud Function

This Cloud Function uses Google's Gemini 2.0 Flash Lite model to optimize CVs and provide analysis based on job descriptions.

## Deployment Instructions

### Local Testing

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the function locally:
   ```
   functions-framework --target=cv_optimizer
   ```

3. The function will be available at http://localhost:8080

### Deployment to Google Cloud Functions

1. Make sure you have the Google Cloud SDK installed and configured:
   ```
   gcloud auth login
   gcloud config set project hireable-places
   ```

2. Deploy the function:
   ```
   gcloud functions deploy parser \
     --gen2 \
     --runtime=python311 \
     --region=europe-west2 \
     --source=. \
     --entry-point=cv_optimizer \
     --trigger-http \
     --allow-unauthenticated
   ```

3. Once deployed, the function will be available at the URL provided in the deployment output.

## Project Structure

- `main.py`: Main function code
- `config.py`: Configuration settings
- `utils/`: Utility modules
  - `document_processor.py`: Document handling
  - `storage.py`: Google Cloud Storage operations
  - `gemini_client.py`: Gemini AI API client
- `prompts/`: Prompt templates
- `schemas/`: JSON schemas for responses
- `few_shot_examples/`: Examples for few-shot learning

## Important Notes

- The function expects resource directories (`prompts/`, `schemas/`, `few_shot_examples/`) to be present at the same level as the main.py file.
- Make sure these directories are included in your deployment.
- All imports should use the flat structure (e.g., `import config` not `import src.config`) 