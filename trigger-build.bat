@echo off
echo Triggering Cloud Build deployment...

REM Submit the build job to Cloud Build
gcloud builds submit --config=cloudbuild.yaml .

echo Build submitted. Check the Cloud Build console for progress. 