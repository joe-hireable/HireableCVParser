import logging
import azure.functions as func
import os
import requests
from openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobClient
import json
import re
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        logging.info(f'Request body: {req_body}')
    except ValueError as e:
        logging.error(f'Error parsing JSON: {e}')
        return func.HttpResponse(
            "Please pass a JSON object in the body",
            status_code=400
        )

    file_url = req_body.get('file_url')
    if not file_url:
        logging.error('No file URL provided')
        return func.HttpResponse(
            "Please pass a file URL in the body",
            status_code=400
        )

    # Download the file
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        logging.info(f'File downloaded from {file_url}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to download the file: {e}')
        return func.HttpResponse(
            "Failed to download the file",
            status_code=400
        )

    file_content = response.content
    file_name = os.path.basename(file_url)

    # Upload to Azure Blob Storage using access key
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "cvparsercontainer"
    
    blob_client = BlobClient.from_connection_string(connect_str, container_name, file_name)

    try:
        blob_client.upload_blob(file_content, overwrite=True)
        logging.info(f'File uploaded to blob storage: {file_name}')
    except Exception as e:
        logging.error(f"Failed to upload blob: {e}")
        return func.HttpResponse(
            "Failed to upload the file to blob storage",
            status_code=500
        )

    # Parse the document (OpenAI integration)
    endpoint = os.getenv("OPENAI_ENDPOINT")
    api_key = os.getenv("OPENAI_KEY")

    try:
        client = OpenAIClient(endpoint, AzureKeyCredential(api_key))
        response = client.completions.create(
            engine="gpt-4",  # Replace with GPT-4o engine identifier when available
            prompt=(
                "Parse the following CV document and extract the following information in JSON format:\n"
                "- Personal Information:\n"
                "  - First Name (text)\n"
                "  - Surname (text)\n"
                "  - Email Address (email)\n"
                "  - Address (location)\n"
                "  - Mobile Number (text)\n"
                "- Profile:\n"
                "  - Profile Statement/Summary (text)\n"
                "- Achievements:\n"
                "  - Key Achievements (list of texts)\n"
                "- Skills:\n"
                "  - Core Skills (list of texts)\n"
                "- Education History (list of objects):\n"
                "  - Institution Name (text)\n"
                "  - Qualification (text)\n"
                "  - Field of Study (text)\n"
                "  - Grade (text)\n"
                "  - Start Date (UNIX Date formatted as mmm yyyy)\n"
                "  - End Date (UNIX Date formatted as mmm yyyy)\n"
                "- Career History (list of objects):\n"
                "  - Company Name (text)\n"
                "  - Job Title (text)\n"
                "  - Start Date (UNIX Date formatted as mmm yyyy)\n"
                "  - End Date (UNIX Date formatted as mmm yyyy)\n"
                "  - Description (text)"
            )
        )

        parsed_data = extract_data(response.choices[0].text)
        logging.info(f'Parsed data: {parsed_data}')
    except Exception as e:
        logging.error(f"Error in OpenAI call: {e}")
        return func.HttpResponse(
            "Error processing the CV document",
            status_code=500
        )

    return func.HttpResponse(
        json.dumps(parsed_data),
        mimetype="application/json",
        status_code=200
    )

def extract_data(parsed_text):
    data = {
        "FirstName": extract_field(parsed_text, "First Name"),
        "Surname": extract_field(parsed_text, "Surname"),
        "EmailAddress": extract_field(parsed_text, "Email Address"),
        "Address": extract_field(parsed_text, "Address"),
        "MobileNumber": extract_field(parsed_text, "Mobile Number"),
        "ProfileStatement": extract_field(parsed_text, "Profile Statement"),
        "KeyAchievements": extract_list(parsed_text, "Key Achievements"),
        "CoreSkills": extract_list(parsed_text, "Core Skills"),
        "EducationHistory": extract_education_history(parsed_text),
        "CareerHistory": extract_career_history(parsed_text)
    }
    return data

def extract_field(text, field_name):
    pattern = rf"{field_name}: (.+)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""

def extract_list(text, field_name):
    pattern = rf"{field_name}:(.+?)(?:\n\n|$)"
    match = re.search(pattern, text, re.DOTALL)
    return [item.strip() for item in match.group(1).split("\n") if item.strip()] if match else []

def extract_education_history(text):
    pattern = r"Education History:\n(.+?)(?:\n\n|$)"
    match = re.search(pattern, text, re.DOTALL)
    education_history = []
    if match:
        for item in match.group(1).split("\n\n"):
            education = {
                "InstitutionName": extract_sub_field(item, "Institution Name"),
                "Qualification": extract_sub_field(item, "Qualification"),
                "FieldOfStudy": extract_sub_field(item, "Field of Study"),
                "Grade": extract_sub_field(item, "Grade"),
                "StartDate": convert_to_unix_date(extract_sub_field(item, "Start Date")),
                "EndDate": convert_to_unix_date(extract_sub_field(item, "End Date"))
            }
            education_history.append(education)
    return education_history

def extract_career_history(text):
    pattern = r"Career History:\n(.+?)(?:\n\n|$)"
    match = re.search(pattern, text, re.DOTALL)
    career_history = []
    if match:
        for item in match.group(1).split("\n\n"):
            career = {
                "CompanyName": extract_sub_field(item, "Company Name"),
                "JobTitle": extract_sub_field(item, "Job Title"),
                "StartDate": convert_to_unix_date(extract_sub_field(item, "Start Date")),
                "EndDate": convert_to_unix_date(extract_sub_field(item, "End Date")),
                "Description": extract_sub_field(item, "Description")
            }
            career_history.append(career)
    return career_history

def extract_sub_field(text, sub_field_name):
    pattern = rf"{sub_field_name}: (.+)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""

def convert_to_unix_date(date_str):
    try:
        return int(datetime.strptime(date_str, "%b %Y").timestamp())
    except ValueError:
        return None
