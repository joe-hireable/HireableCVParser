<task>
You must evaluate and score a CV/résumé document provided in the `cv` section of this prompt. If a job description is provided in the `jd` section, score the CV against that specific role; otherwise, perform a generic quality assessment of the CV. Your task is to provide a comprehensive assessment, returning a valid JSON object that adheres to the response_schema. Focus on providing an objective evaluation with actionable feedback.
</task>

<instructions>
### CV Scoring Guidelines

#### Scoring Requirements
1. Evaluate the CV across multiple dimensions, scoring each on a scale of 0-100:
   - **Relevance**: How well the CV matches the job requirements when provided, otherwise how well the CV communicates a clear professional focus
   - **Skills Alignment**: How well the candidate's skills align with role requirements (if job provided) or how well skills are presented and organized (if generic assessment)
   - **Experience Match**: How well the candidate's experience matches position needs (if job provided) or how effectively experience demonstrates career progression (if generic assessment)
   - **Achievement Focus**: How effectively the CV demonstrates concrete achievements and results
   - **Presentation**: How professional, readable, and well-structured the CV appears
   - **ATS Compatibility**: How likely the CV is to pass through Applicant Tracking Systems
2. Calculate an overall weighted score based on these dimensions
3. Provide specific strengths and improvement suggestions based on the evaluation
4. Include a high-level match assessment indicating the candidate's fit for the role (when job description is provided) or overall CV effectiveness (when no job description is provided)

#### Scoring Methodology
1. **Relevance Scoring (0-100)**:
   
   *When job description is provided:*
   - Match rate of key terms and phrases from job description
   - Alignment of professional summary with job requirements
   - Industry and domain language appropriateness
   - Focus on requirements mentioned multiple times in the job description
   
   *When no job description is provided:*
   - Clarity of professional identity and career focus
   - Consistency of narrative throughout the CV
   - Appropriateness of industry and domain language
   - Effective communication of value proposition

2. **Skills Alignment Scoring (0-100)**:
   
   *When job description is provided:*
   - Coverage of required technical skills
   - Coverage of required soft skills
   - Depth of skill representation (beginner vs. expert)
   - Presence of bonus/desired skills beyond requirements
   
   *When no job description is provided:*
   - Organization and categorization of skills
   - Balance between technical and soft skills
   - Clear indication of proficiency levels
   - Relevance of skills to the candidate's career path

3. **Experience Match Scoring (0-100)**:
   
   *When job description is provided:*
   - Years of relevant experience compared to requirements
   - Industry/domain experience relevance
   - Role responsibility overlap with job requirements
   - Management/leadership experience if relevant
   - Project scale and complexity match
   
   *When no job description is provided:*
   - Clear demonstration of career progression
   - Consistent employment history without unexplained gaps
   - Appropriate detail level for experience descriptions
   - Relevance of highlighted experience to career trajectory
   - Balance between responsibilities and achievements

4. **Achievement Focus Scoring (0-100)**:
   - Ratio of achievement statements to responsibility statements
   - Presence of quantified results (metrics, percentages, amounts)
   - Demonstration of relevant problem-solving
   - Evidence of recognition or promotion
   - Impact and value demonstrated in previous roles

5. **Presentation Scoring (0-100)**:
   - Clarity and conciseness of language
   - Effective organization and structure
   - Consistent formatting and style
   - Appropriate length and detail level
   - No grammatical or spelling errors

6. **ATS Compatibility Scoring (0-100)**:
   - Presence of job-specific keywords in context
   - Standard section headings
   - Simple formatting without complex tables or graphics
   - Proper handling of acronyms and technical terms
   - Appropriate file format and parsing ease

#### Overall Score Calculation
Calculate the weighted overall score using the following weights:
- Relevance: 25%
- Skills Alignment: 25%
- Experience Match: 20%
- Achievement Focus: 15%
- Presentation: 10%
- ATS Compatibility: 5%

The overall score should indicate the candidate's fit for the role with these general interpretations:
- 90-100: Exceptional match, highly qualified
- 80-89: Strong match, well-qualified
- 70-79: Good match, qualified
- 60-69: Partial match, somewhat qualified
- Below 60: Weak match, significantly underqualified

#### Feedback Guidelines
- Include 3-5 specific strengths of the candidate's CV relevant to the target role
- Provide 3-5 actionable suggestions for improving the CV's impact and relevance
- Base all feedback on actual content in the CV compared to the job description
- Be specific about which keywords, skills, or experiences are missing or need enhancement
- Suggest concrete changes or additions that would improve the score

#### Match Assessment
*When job description is provided:*
Provide a high-level assessment in 2-3 sentences that summarizes:
- The candidate's overall suitability for the role
- Key strengths that make them a good fit
- Any significant gaps that might need to be addressed
- Whether to recommend proceeding with the candidate based on CV evaluation

*When no job description is provided:*
Provide a high-level assessment in 2-3 sentences that summarizes:
- The overall effectiveness and quality of the CV
- Key strengths of the CV's presentation and content
- Major areas that could be improved
- General employability impression based on the CV quality

#### Response Structure
Return a JSON object with:
1. "status": Use "success" for normal results, "error" for fatal errors, "partial" for partial success
2. "errors": Array of error objects (null if no errors)
3. "data": Object containing:
   - "scores": Object with numerical scores for each dimension and overall score
   - "feedback": Object containing arrays of strengths and improvement suggestions
   - "matchAssessment": String summarizing the candidate's fit for the role

#### Error Handling
If the CV or job description cannot be properly evaluated:
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