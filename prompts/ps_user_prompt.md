<task>
You must optimize the profile statement section of a CV/résumé document provided in `<section></section>` of this prompt, with reference to the job description in the `jd` section if one is provided. If you feel the optimised profile statement would benefit from pulling additional or alternative information from the rest of the cv (provided in `<cv></cv>`) - you may refactor the information accordingly.

<section>
<${section}>
</section>

Your task is to critically assess and optimise the profile statement provided in `<section></section>`, returning a valid JSON object that adheres to the response_schema. This content should effectively position the candidate for the target role or relevant roles in general.
</task>

<instructions>
### Profile Statement Optimization Guidelines

#### Profile Statement Requirements
1. Craft a compelling, targeted profile statement (maximum 750 characters)
2. Structure in 3-4 concise sentences or bullet points covering:
   - Professional identity and years of relevant experience
   - Key areas of expertise relevant to the target role
   - Notable achievements or credentials that differentiate the candidate
   - Career goals or value proposition aligned with the target role
3. Use present tense for current skills/qualities and past tense for experience/achievements
4. Incorporate relevant keywords from the job description

#### Content Alignment Priorities
1. Match profile statement content to specific requirements in the job description
2. Emphasize transferable skills when pivoting to a new role or industry
3. Highlight domain expertise and industry knowledge relevant to the target role
4. Include relevant metrics, credentials, or notable projects when appropriate
5. Ensure tone and language align with the industry/role conventions

#### Optimization Guidelines
1. Focus on value and impact rather than responsibilities
2. Use active voice and strong action verbs
3. Avoid clichés, generic statements, and first-person pronouns
4. Remove any content not directly supporting candidacy for the target role
5. Ensure readability with appropriate sentence structure and flow

#### Feedback Guidelines
- Include 3-5 specific strengths of the candidate's current profile statement
- Provide 3-5 actionable suggestions for improving the profile statement's impact and relevance
- Base all feedback on actual content in the CV compared to the job description

#### Response Structure
Return a JSON object with:
1. "status": Use "success" for normal results, "error" for fatal errors, "partial" for partial success
2. "errors": Array of error objects (null if no errors)
3. "data": Object containing:
   - "profileStatement": Optimized professional profile statement string (maximum 750 characters)
   - "feedback": Object containing:
     - "strengths": Array of strengths in the profile statement
     - "areas_to_improve": Array of suggestions for improvement

#### Error Handling
If the profile statement cannot be properly created:
1. Set "status" to "error" or "partial" as appropriate
2. Include relevant error objects in the "errors" array
3. Return as much valid data as possible in the "data" object
</instructions>

<cv>
<${cv}>
</cv>

<jd>
<${jd}>
</jd>
