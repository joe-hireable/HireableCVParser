<task>
You must optimize a specific work experience entry from the CV/résumé document provided in the `cv` section of this prompt, with reference to the job description in the `jd` section.

<section>
{section}
</section>

Your task is to enhance and structure this specific work experience entry, returning a valid JSON object that adheres to the response_schema. Focus on highlighting relevant achievements and responsibilities for the target role.
</task>

<instructions>
### Work Experience Optimization Guidelines

#### Experience Extraction Requirements
1. Extract and optimize the specific work experience entry highlighted in the `<section>` tag
2. Maintain data fidelity - only use information explicitly stated in the source CV
3. Structure the experience according to the schema requirements:
   - Company name (use full legal name without suffixes unless part of common name)
   - Overall employment period (start and end dates covering all roles at the company)
   - Current status (set to true only if explicitly stated as current or if end date is missing)
   - Roles array (all positions held at this company with individual start/end dates)
   - Summary of responsibilities (maximum 400 characters)
   - Key highlights/achievements (maximum 6 items, 200 characters each)

#### Role Structuring Guidelines
1. For each role within the company:
   - Use the exact job title as stated in the CV
   - Standardize common abbreviations (e.g., "Sr." to "Senior")
   - Include precise start and end dates for that specific position
   - Mark as current only if it's the latest role with no end date

#### Date Formatting Rules
1. Format all dates as "MMM YYYY" (e.g., "Jan 2020")
2. For current positions, set end date to null and "current" flag to true
3. For past positions, include precise end date and set "current" flag to false
4. Maintain chronological consistency within roles (most recent first)

#### Summary Optimization
1. Create a concise summary (maximum 400 characters) that:
   - Focuses on scope of responsibilities relevant to the target role
   - Highlights key accountabilities and areas of oversight
   - Uses active voice and strong action verbs
   - Avoids unnecessary jargon or overly technical language unless relevant
   - Emphasizes transferable skills that align with the job description

#### Achievements Enhancement
1. Identify and optimize up to 6 key achievements that:
   - Demonstrate measurable impact and results (with metrics where available)
   - Follow the STAR method (Situation, Task, Action, Result)
   - Begin with strong action verbs and focus on outcomes
   - Are most relevant to the requirements in the job description
   - Include quantifiable results (percentages, monetary values, time savings)
   - Each achievement should not exceed 200 characters

#### Feedback Guidelines
- Include 3-5 specific strengths of the candidate's current role description
- Provide 3-5 actionable suggestions for improving the role presentation and relevance
- Base all feedback on actual content in the CV compared to the job description

#### Relevance Prioritization
1. Reorder and emphasize aspects of the experience that align with the target role
2. Place the most relevant achievements at the beginning of the highlights array
3. Focus on responsibilities and achievements that demonstrate transferable skills
4. Highlight industry-specific knowledge and expertise relevant to the job description

#### Response Structure
Return a JSON object with:
1. "status": Use "success" for normal results, "error" for fatal errors, "partial" for partial success
2. "errors": Array of error objects (null if no errors)
3. "data": Object containing:
   - "company": Company name string
   - "start"/"end": Date strings in "MMM YYYY" format (end is null if current)
   - "current": Boolean indicating if this is a current position
   - "summary": Concise description of responsibilities (maximum 400 characters)
   - "highlights": Array of achievement strings (maximum 6 items, 200 characters each)
   - "roles": Array of role objects each with title, start, end, and current status
   - "feedback": Object containing:
     - "strengths": Array of strengths in the role description
     - "areas_to_improve": Array of suggestions for improvement

#### Error Handling
If the experience entry cannot be properly processed:
1. Set "status" to "error" or "partial" as appropriate
2. Include relevant error objects in the "errors" array
3. Return as much valid data as possible in the "data" object
</instructions>

<cv>
{cv_content}
</cv>

<jd>
{jd_content}
</jd>

{few_shot_examples}
