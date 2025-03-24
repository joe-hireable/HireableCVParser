<task>
You must extract structured information from the CV/résumé document in the `<cv>` section of this prompt and return a valid JSON object adherent to the provided response_schema. Your task is to accurately parse all relevant information while following the detailed extraction guidelines below.
</task>

<instructions>
### **Responsibilities:**
1. Extract and preserve ALL employment history entries:
   - Every work experience item from the source CV must be represented in either the 'experience' or 'earlierCareer' fields.
   - For each company, determine the overall start and end dates that encompass all roles held there.
   - Within each company object, include a 'roles' array where each role object contains its own 'title', 'start' date, and 'end' date.
   - Company-level 'highlights' should summarise achievements across roles.
   - While you may rephrase content, do not completely exclude any entries from these sections: experience, earlierCareer, education, certifications.
   - Maintain complete data fidelity even when reformatting.

2. Content Organization:
   - Reorder and rephrase entries to maximise relevance to target job requirements.
   - Place the most relevant achievements and experience.highlights at the beginning of their respective arrays.
   - Do not generate new information or embellish existing content.
   - Only use information explicitly present in the source CV.

3. Output Structure and Validation:
   - Format all output according to the provided JSON schema.
   - Verify schema compliance before returning the response.
   - Maintain chronological ordering within the following arrays:
     - experience/earlierCareer
     - education
     - certifications

### Field Extraction Guidelines:

#### Personal Information
- "firstName", "surname": Extract from the header/contact section. Split full names at the last space unless a clear indication suggests otherwise.
- "email": Must match the standard email format (user@domain.tld). Convert to lowercase.
- "phone": Convert ALL numbers to international format (+[country code][number]). Remove spaces and special characters.
- "links": Include only professional URLs (LinkedIn, Portfolio, GitHub). Validate URL format.
- "location": Extract city, country, and postal code only if explicitly stated. Do not infer from company locations.
- "headline": Limit to 75 characters. Prioritise the current role/specialisation. Format as "[Role] specialising in [Domain]".
- "profileStatement": Maximum 750 characters. Focus on career progression, key expertise areas, and notable achievements.

#### Skills
- Populate core skills in "skills", each as an object containing:
  - "name": The skill name.
  - "proficiency": Beginner, Average, Intermediate, Advanced or Expert.
  - "skillType": Either "hard" or "soft". Only include explicitly mentioned skills.
- Include a maximum of 14 distinct skills.
- Standardise variations (e.g., "React.js" → "React").

#### Professional Memberships
- Extract professional memberships (e.g., CIPD, CIOB, MCIPS/FCIPS) explicitly mentioned in the CV.
- Populate the 'memberships' field as an array of objects, each with 'name' and 'institution' properties.

#### Career Progression
- "experience" (past 10 years):
  - For each company, use the full legal name (removing legal suffixes unless part of the common name).
  - Include an overall "start" and "end" date that covers the full duration of employment at the company.
  - Within the company object, include a "roles" array. Each role object must contain:
      - "title": The specific job title held.
      - "start": Role start date (MMM YYYY, or just YYYY if only year is displayed).
      - "end": Role end date (MMM YYYY, or just YYYY if only year is displayed).
  - "current" remains at the company level, set to true only if explicitly stated as current or if the end date is missing.
  - "summary": Maximum 400 characters. Focus on the scope of the role(s) and responsibilities.
  - "highlights": Maximum 6 items, 200 characters each. Prioritise quantifiable achievements (e.g., %, £, metrics) using the STAR method where possible.

- "earlierCareer" (roles that ended over 10 years ago):
  - For each company, include an overall "start" and "end" date, along with a "roles" array containing the specific roles (each with "title", "start", and "end").
  - Do not include a "current" field as these roles are historical.

#### Achievements
- Maximum 6 distinct achievements.
- Each achievement should not exceed 300 characters and follow the STAR method (Situation, Task, Action, Result).
- Prioritise quantifiable results and list the most relevant items first.

#### Education
- "institution": Use the full official name.
- "qualifications": Group multiple qualifications under the same institution.
- Dates: Use the "MMM YYYY format, or just YYYY if only year is displayed". Set to null if unclear.
- "publications": Include only if explicitly academic or research related.

#### Certifications
- "name": Use the official certification name (avoid abbreviations).
- "issuer": Use the full organisation name.
- "date": Use the "MMM YYYY format, or just YYYY if only year is displayed", reflecting the award date rather than an expiry date.

#### Languages
- "name": Use the English name for languages (e.g., "Spanish" not "Español").
- "level": Map proficiency to the defined enum values: Native, Fluent, Advanced, Intermediate, Basic.

#### Additional Details
- "addDetails": A text array for any additional information that does not naturally fit into the specified schema sections. Can include anything relevant such as side projects, patents, extra-curricular, etc.

### **Validation Rules:**

**1. Required Fields Check:**
   - Ensure all required fields have values (use null if not found).
   - Required fields include: headline, profileStatement, skills, achievements, experience, education, certifications, languages, firstName, surname.

**2. Length Validation:**
   - headline: ≤ 75 characters.
   - profileStatement: ≤ 750 characters.
   - experience.summary: ≤ 400 characters.
   - experience.highlights: ≤ 200 characters each.
   - achievements: ≤ 300 characters each.

**3. Array Size Limits:**
   - skills: ≤ 14 items.
   - achievements: ≤ 6 items.
   - addDetails: ≤ 15 items.
   - experience.highlights: ≤ 6 items per company.

**4. Date Format Consistency:**
   - All dates must follow the "MMM YYYY format, or just YYYY if only year is displayed".
   - For current positions, the end date must be null.
   - Start dates must precede end dates.
   - Experience dates must fall within the past 10 years.
   - Earlier career dates must be from over 10 years ago.

**5. Enumeration Validation:**
   - language.level must match one of the defined enum values.
   - status must be one of: "success", "error", "partial".
   - error.severity must be either "error" or "warning".
</instructions>

<cv>
{cv_content}
</cv>

<jd>
{jd_content}
</jd>

{few_shot_examples}