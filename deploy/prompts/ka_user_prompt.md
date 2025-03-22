<task>
You must optimize the achievements section of a CV/résumé document provided in the `cv` section of this prompt, with reference to the job description in the `jd` section.

<section>
<${section}>
</section>

Your task is to extract and enhance key achievements, returning a valid JSON object that adheres to the response_schema. Focus on highlighting accomplishments that demonstrate value relevant to the target role.
</task>

<instructions>
### Key Achievements Optimization Guidelines

#### Extraction Requirements
1. Extract all quantifiable achievements and significant accomplishments from the CV
2. Maintain data fidelity - only use information explicitly stated in the source CV
3. Focus on results, impact, and value delivered rather than responsibilities
4. Prioritize achievements from recent roles that demonstrate relevant skills for the target position

#### Achievement Enhancement Guidelines
1. Structure each achievement using the STAR method (Situation, Task, Action, Result)
2. Highlight quantifiable metrics where available (%, $, #, time savings, etc.)
3. Begin each achievement with strong action verbs
4. Connect achievements to skills and requirements mentioned in the job description
5. Include business context and impact to demonstrate value
6. Keep each achievement concise (maximum 300 characters)

#### Prioritization Criteria
1. Relevance to target role requirements (primary factor)
2. Recency of achievement (secondary factor)
3. Quantifiable impact (tertiary factor)
4. Uniqueness and distinction from other achievements (final factor)

#### Feedback Guidelines
- Include 3-5 specific strengths of the candidate's current achievements presentation
- Provide 3-5 actionable suggestions for improving the achievements' impact and relevance
- Base all feedback on actual content in the CV compared to the job description

#### Format Requirements
1. Maximum 6 distinct achievements
2. Each achievement should be expressed as a single, complete statement
3. Focus on clarity, specificity, and impact
4. Remove any vague or generic statements
5. Standardize tense (preferably past tense for completed achievements)

#### Response Structure
Return a JSON object with:
1. "status": Use "success" for normal results, "error" for fatal errors, "partial" for partial success
2. "errors": Array of error objects (null if no errors)
3. "data": Object containing:
   - "achievements": Array of achievement strings, prioritized by relevance to the target role
   - "feedback": Object containing:
     - "strengths": Array of strengths in the achievements presentation
     - "areas_to_improve": Array of suggestions for improvement

#### Error Handling
If achievements cannot be properly extracted or processed:
1. Set "status" to "error" or "partial" as appropriate
2. Include relevant error objects in the "errors" array
3. Return as much valid achievement data as possible in the "data" object
</instructions>

<cv>
<${cv}>
</cv>

<jd>
<${jd}>
</jd>
