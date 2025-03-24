<task>
You must optimize the core skills section of a CV/résumé provided in the `cv` section of this prompt, with reference to the job description in the `jd` section. 

<section>
{section}
</section>

Your task is to extract and enhance the skills section, returning a valid JSON object that adheres to the response_schema. Focus on matching skills to the job requirements while maintaining truthfulness.
</task>

<instructions>
### Core Skills Optimization Guidelines

#### Extraction Requirements
1. Extract all relevant skills from the source CV
2. Maintain data fidelity - only use skills explicitly mentioned in the CV
3. Map each skill to appropriate proficiency levels:
   - Beginner: Basic knowledge, limited practical experience
   - Intermediate: Solid experience, comfortable with common applications
   - Advanced: Deep understanding, can handle complex scenarios
   - Expert: Extensive knowledge, acknowledged authority on the subject
4. Categorize each skill as either:
   - "hard" (technical skills, measurable abilities, software competencies)
   - "soft" (interpersonal qualities, character traits, people skills)

#### Job Alignment Priorities
1. Prioritize skills that directly match the job description requirements
2. Elevate skills that demonstrate particular value for the target role
3. Include transferable skills that may apply to the new position
4. Keep industry-specific terminology if relevant to the target position

#### Skill Standardization Rules
1. Normalize skill names (e.g., "React.js" → "React")
2. Remove duplicates and closely related variations
3. Convert vague descriptors into specific, recognized skill names
4. Break compound skills into separate, distinct entries when appropriate
5. Include only the most relevant skills, between 5-14 distinct skills

#### Feedback Guidelines
- Include 3-5 specific strengths of the candidate's current skills presentation relevant to the target role
- Provide 3-5 actionable suggestions for improving skills presentation and alignment with job requirements
- Base all feedback on actual content in the CV compared to the job description

#### Response Structure
Return a JSON object with:
1. "status": Use "success" for normal results, "error" for fatal errors, "partial" for partial success
2. "errors": Array of error objects (null if no errors)
3. "data.skills": Array of skill objects, each containing:
   - "name": The standardized skill name
   - "proficiency": One of "Beginner", "Average", "Intermediate", "Advanced", or "Expert"
   - "skillType": Either "hard" or "soft"
4. "data.feedback": Object containing:
   - "strengths": Array of strengths in the skills presentation
   - "areas_to_improve": Array of suggestions for improvement

#### Error Handling
If skills section cannot be properly extracted or processed:
1. Set "status" to "error" or "partial" as appropriate
2. Include relevant error objects in the "errors" array
3. Return as much valid skills data as possible in the "data" object
</instructions>

<cv>
{cv_content}
</cv>

<jd>
{jd_content}
</jd>

{few_shot_examples}