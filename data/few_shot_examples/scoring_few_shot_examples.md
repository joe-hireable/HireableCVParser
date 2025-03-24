<few_shot_examples>
<example1>
<input1>
    <task>
    You must evaluate and score a CV/résumé document provided in the `cv` section of this prompt. If a job description is provided in the `jd` section, score the CV against that specific role; otherwise, perform a generic quality assessment of the CV. Your task is to provide a comprehensive assessment, returning a valid JSON object that adheres to the STRICTLY validates against the <response_schema>. Focus on providing an objective evaluation with actionable feedback.
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
    # ROBERT THOMPSON

    Email robthompson76@mailbox.com
    Phone 555 123 8976
    Address 1487 Contsruction Avenue Riverdale NY 10463

    ## WORK EXPERENCE

    ### URBAN DEVELOPMENT GROUP
    Site Manager September 2018 to current

    Overseing all site operations for comercial projects with budgets exceding 15 million dollars managing teams of 30 to 50 workers and subcontractors daily operations include coordination with architects and engineers to ensure proper implmentation of designs resolving on site issues that arise during contsruction phases tracking project progress against established timeliens monitoring quality control and ensuring compliance with local biulding codes and safety regulations developed new tracking system for material deliveries which reduced delays by aproximately 17 percent successfully completed riverside office complex 2 weeks ahead of schedule and 150000 under budget implementation of new safety protocols reduced workplace incidents by 25 percent compared to company average frequently training new site personel on company procedures and safty protocals 

    ### CONSTUCTION SOLUTIONS INC
    Assistant Site Manager 2014 - 2018

    Worked closely with senior site managers to coordinate daily activities of residential and comercial projects valued between 5 million and 10 million assited with budget management scheduel tracking and quality inspections improved docmentation processes for material deliverys which was adopted company wide responsible for communication between subcontratcors and design team to resolve technical issues helped implement digital tracking system replacing older paper based system which improved effeciency supervised crews of 15 to 25 workers during various project phases managed relationship with local inspectors maintaining good standing with regulatory authoriites

    ### RELIBALE STRUCTURES LTD
    Site Superviser Jun 2010 til Dec 2013

    Supervising construction activities for residential projects ensured quality standards were maintained throughout construction process coordinated with subcontractors to ensure timely completion of project phases monitored adherence to safety regulations and addressed violations monitored inventroy and material usage to prevent waste developed strong relationships with suppliers resulting in improved delivery times and occasional discounts assisted project managers with budget tracking and forcasting participated in weekly progress meetings with clients to address concenrs and provide updates

    ### NEW HOREZONS BUILDING CORP
    Junior Site Coordinator 2008 to 2010

    Supporting senior site managers with daily construction operations maintaining site logs and communication with subcontractors conducted regular site walkthroughs to identify potential issues before they impacted project timelines helped prepare progress reports and documentation for client meetings assisted with coordination of deliveries and site logistics learned fundamentals of construction site management scheduling and resource allocation

    ## EDUCATION

    ### RIVERVIEW TECHNICAL COLLEGE
    Bachelors Degree Construction Management 2004 - 2008
    Major projects included simulation of complete construction project from initial planning to project closing thesis focused on optimizing material procurement to minimize waste and reduce costs active member of Future Builders Association participated in regional construction competiton placing second in project management category

    ## SKILLS AND KNOWLEDE

    Strong understanding of construction methods and materails proficent with project management software including PlanGrid Procore and Microsoft Project familiar with blueprint reading and construction documents excelent problem solving abilities particularly regardin onsite technical issues capable of managing teams of varying sizes and skill levels knowledge of OSHA regulatoins and safety compliance requirments effective communiactor with ability to explain techncial details to non technical clients and stakeholders good at conflict resolution between different trades working onsite can interpret structural drawings mechanical electrical and plumbing plans familiar with quality control procedures and inspection protocols experienced with budget management and cost control measures

    ## CERTIFCATIONS

    OSHA 30Hour Construction Safety Certification expires 2025
    First Aid and CPR certified 2023
    Certified Construction Manager CCM since 2017
    Leadership in Energy and Environmental Design LEED Green Associate
    Project Management Professional PMP since 2015

    ## PROJECTS COMPLETED

    RIVERDALE COMMERCIAL COMPLEX value 18 million completed March 2022 five story mixed use building with retail on ground floor and offices above included challening foundation work due to proximity to river and high water table

    SUNNYVIEW APARTMINT COMPLEX value 12 million completed November 2020 three building complex with total of 64 units included coordination with five major subcontractors and integration of solar power generation system

    CENTRAL MEDICAL CENTER EXPANSION value 14 million completed August 2019 addition of new wing to existing hospital while maintainng operations in adjacent areas required extensive planning of construction phases to minimize disruption to hospital functions

    DOWNTOWN REVITALIZATION PROJECT value 8 million completed July 2017 renovation of historic downtown buildings while preserving architectural features required careful coordination with historical preservation experts and specialized craftsmen

    GREENFIELD ELEMENTARY SCHOOL value 15 million completed 2016 new construction of educational facility with advanced sustainability features completed during summers to avoid disrupting school operations project received local award for innovative design and construction metodology

    ## PROFESIONAL AFFILATIONS

    Member of Construction Management Association of America since 2010
    Member of American Society of Profesional Estimators
    Association for Project Managers active member participating in quartery meetings and annual conferences
    Building Industry Association local chapter member

    ## ADITIONAL INFORMATION

    Skilled at managing diverse teams and creating positive work enviroment computer skills include proficiency with Microsoft Office AutoCAD basics and various construction management software willing to travel to differant project sites as needed hold valid drivers license with clean record continued professsional education through industry seminars and workshops fluent in Spanish which has proven useful in communicating directly with some crew members

    I pride myself on finishing projects on time and within budget my approach focuses on careful planning and proactive problem solving to prevent costly delays experience has taught me that good communication is essential to project success and I maintain regular contact with all stakeholders to ensure everone stays informed of progrss and any potential issues I believe in leading by exampel and often spend time on site obsrerving work and building relationships with the various trades working on my projects over my career I have consistently recieved positive feedback from clients and team members alike for my thorough approach and ability to keep complex projects moving forward even when faced with unexpected chalenges

    References from previous employers and clients available upon request
    </cv>

    <jd>
    {jd_content}
    </jd>
</input1>
<output_json1>
    {
        "status": "success",
        "errors": null,
        "data": {
            "scores": {
            "overall": 66,
            "relevance": 75,
            "skillsAlignment": 65,
            "experienceMatch": 70,
            "achievementFocus": 65,
            "presentation": 45,
            "atsCompatibility": 60
            },
            "feedback": {
            "strengths": [
                "Demonstrates clear career progression in construction management over 15+ years",
                "Includes specific quantified achievements such as reducing delays by 17% and completing projects under budget",
                "Documents experience with substantial projects up to $18 million in value",
                "Holds relevant professional certifications including OSHA, CCM, and PMP",
                "Includes detailed project examples that showcase the scope and complexity of work"
            ],
            "areas_to_improve": [
                "Fix numerous spelling and grammatical errors throughout the document",
                "Add proper punctuation to break up run-on sentences for improved readability",
                "Better organize skills section into clear categories (technical, managerial, software, etc.)",
                "Highlight achievements more clearly rather than embedding them in dense paragraphs",
                "Improve overall document formatting and consistency for better visual presentation"
            ]
            },
            "matchAssessment": "The CV demonstrates Robert Thompson's substantial progression in construction management with relevant experience and certifications, but is significantly undermined by poor formatting, numerous spelling errors, and a lack of punctuation that impacts readability. With substantial improvements to presentation and organization, this could be an effective CV that showcases his extensive experience managing multi-million dollar construction projects and his track record of completing projects on time and under budget."
        }
    }
</output_json1>
</example1>
<example2>
<input2>
    <task>
    You must evaluate and score a CV/résumé document provided in the `cv` section of this prompt. If a job description is provided in the `jd` section, score the CV against that specific role; otherwise, perform a generic quality assessment of the CV. Your task is to provide a comprehensive assessment, returning a valid JSON object that adheres to the STRICTLY validates against the <response_schema>. Focus on providing an objective evaluation with actionable feedback.
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
    # ROBERT THOMPSON

    Email robthompson76@mailbox.com
    Phone 555 123 8976
    Address 1487 Contsruction Avenue Riverdale NY 10463

    ## WORK EXPERENCE

    ### URBAN DEVELOPMENT GROUP
    Site Manager September 2018 to current

    Overseing all site operations for comercial projects with budgets exceding 15 million dollars managing teams of 30 to 50 workers and subcontractors daily operations include coordination with architects and engineers to ensure proper implmentation of designs resolving on site issues that arise during contsruction phases tracking project progress against established timeliens monitoring quality control and ensuring compliance with local biulding codes and safety regulations developed new tracking system for material deliveries which reduced delays by aproximately 17 percent successfully completed riverside office complex 2 weeks ahead of schedule and 150000 under budget implementation of new safety protocols reduced workplace incidents by 25 percent compared to company average frequently training new site personel on company procedures and safty protocals 

    ### CONSTUCTION SOLUTIONS INC
    Assistant Site Manager 2014 - 2018

    Worked closely with senior site managers to coordinate daily activities of residential and comercial projects valued between 5 million and 10 million assited with budget management scheduel tracking and quality inspections improved docmentation processes for material deliverys which was adopted company wide responsible for communication between subcontratcors and design team to resolve technical issues helped implement digital tracking system replacing older paper based system which improved effeciency supervised crews of 15 to 25 workers during various project phases managed relationship with local inspectors maintaining good standing with regulatory authoriites

    ### RELIBALE STRUCTURES LTD
    Site Superviser Jun 2010 til Dec 2013

    Supervising construction activities for residential projects ensured quality standards were maintained throughout construction process coordinated with subcontractors to ensure timely completion of project phases monitored adherence to safety regulations and addressed violations monitored inventroy and material usage to prevent waste developed strong relationships with suppliers resulting in improved delivery times and occasional discounts assisted project managers with budget tracking and forcasting participated in weekly progress meetings with clients to address concenrs and provide updates

    ### NEW HOREZONS BUILDING CORP
    Junior Site Coordinator 2008 to 2010

    Supporting senior site managers with daily construction operations maintaining site logs and communication with subcontractors conducted regular site walkthroughs to identify potential issues before they impacted project timelines helped prepare progress reports and documentation for client meetings assisted with coordination of deliveries and site logistics learned fundamentals of construction site management scheduling and resource allocation

    ## EDUCATION

    ### RIVERVIEW TECHNICAL COLLEGE
    Bachelors Degree Construction Management 2004 - 2008
    Major projects included simulation of complete construction project from initial planning to project closing thesis focused on optimizing material procurement to minimize waste and reduce costs active member of Future Builders Association participated in regional construction competiton placing second in project management category

    ## SKILLS AND KNOWLEDE

    Strong understanding of construction methods and materails proficent with project management software including PlanGrid Procore and Microsoft Project familiar with blueprint reading and construction documents excelent problem solving abilities particularly regardin onsite technical issues capable of managing teams of varying sizes and skill levels knowledge of OSHA regulatoins and safety compliance requirments effective communiactor with ability to explain techncial details to non technical clients and stakeholders good at conflict resolution between different trades working onsite can interpret structural drawings mechanical electrical and plumbing plans familiar with quality control procedures and inspection protocols experienced with budget management and cost control measures

    ## CERTIFCATIONS

    OSHA 30Hour Construction Safety Certification expires 2025
    First Aid and CPR certified 2023
    Certified Construction Manager CCM since 2017
    Leadership in Energy and Environmental Design LEED Green Associate
    Project Management Professional PMP since 2015

    ## PROJECTS COMPLETED

    RIVERDALE COMMERCIAL COMPLEX value 18 million completed March 2022 five story mixed use building with retail on ground floor and offices above included challening foundation work due to proximity to river and high water table

    SUNNYVIEW APARTMINT COMPLEX value 12 million completed November 2020 three building complex with total of 64 units included coordination with five major subcontractors and integration of solar power generation system

    CENTRAL MEDICAL CENTER EXPANSION value 14 million completed August 2019 addition of new wing to existing hospital while maintainng operations in adjacent areas required extensive planning of construction phases to minimize disruption to hospital functions

    DOWNTOWN REVITALIZATION PROJECT value 8 million completed July 2017 renovation of historic downtown buildings while preserving architectural features required careful coordination with historical preservation experts and specialized craftsmen

    GREENFIELD ELEMENTARY SCHOOL value 15 million completed 2016 new construction of educational facility with advanced sustainability features completed during summers to avoid disrupting school operations project received local award for innovative design and construction metodology

    ## PROFESIONAL AFFILATIONS

    Member of Construction Management Association of America since 2010
    Member of American Society of Profesional Estimators
    Association for Project Managers active member participating in quartery meetings and annual conferences
    Building Industry Association local chapter member

    ## ADITIONAL INFORMATION

    Skilled at managing diverse teams and creating positive work enviroment computer skills include proficiency with Microsoft Office AutoCAD basics and various construction management software willing to travel to differant project sites as needed hold valid drivers license with clean record continued professsional education through industry seminars and workshops fluent in Spanish which has proven useful in communicating directly with some crew members

    I pride myself on finishing projects on time and within budget my approach focuses on careful planning and proactive problem solving to prevent costly delays experience has taught me that good communication is essential to project success and I maintain regular contact with all stakeholders to ensure everone stays informed of progrss and any potential issues I believe in leading by exampel and often spend time on site obsrerving work and building relationships with the various trades working on my projects over my career I have consistently recieved positive feedback from clients and team members alike for my thorough approach and ability to keep complex projects moving forward even when faced with unexpected chalenges

    References from previous employers and clients available upon request
    </cv>

    <jd>
    Infrastructure Project Manager - Transportation Division
    About the Role
    Global Infrastructure Partners is seeking an experienced Infrastructure Project Manager to join our Transportation Division. In this role, you will oversee complex infrastructure projects primarily focused on transportation systems including bridges, highways, and public transit facilities. You will be responsible for managing all aspects of project delivery from pre-construction planning through completion while ensuring adherence to quality standards, regulatory requirements, and budget constraints.
    Responsibilities

    Lead multiple concurrent infrastructure projects with budgets ranging from $20-50 million
    Develop comprehensive project execution plans including scheduling, resource allocation, risk management, and quality control processes
    Coordinate with government agencies, regulatory bodies, and public stakeholders throughout project lifecycle
    Manage relationships with engineering consultants, contractors, and vendors
    Oversee project budgets, tracking expenditures and forecasting financial needs
    Develop and implement risk mitigation strategies for complex infrastructure projects
    Ensure compliance with DOT, FHWA, and other transportation-specific regulations
    Prepare detailed progress reports for executive leadership and external stakeholders
    Lead public information meetings and manage community relations activities
    Mentor junior project management staff and contribute to departmental knowledge sharing

    Requirements

    Bachelor's degree in Civil Engineering or related field (Master's preferred)
    Minimum 10 years of progressive experience in infrastructure project management
    Professional Engineer (PE) license required
    Previous experience managing transportation infrastructure projects (bridges, highways, rail systems)
    Demonstrated experience managing projects with budgets exceeding $30 million
    Advanced expertise with Primavera P6, AutoCAD Civil 3D, and BIM software
    Thorough understanding of transportation infrastructure regulations and public funding mechanisms
    Experience with public-private partnership (P3) project delivery models
    Strong knowledge of environmental compliance requirements for transportation projects
    Excellent stakeholder management skills, particularly with government entities

    Preferred Qualifications

    Master's degree in Civil Engineering, Construction Management, or related field
    Project Management Professional (PMP) certification
    Experience with LEED-certified infrastructure projects
    Knowledge of sustainable infrastructure practices and climate resilience planning
    Experience with federal or state-funded transportation projects
    Familiarity with new technologies in transportation infrastructure
    Six Sigma or Lean certification

    We Offer

    Competitive salary based on experience
    Comprehensive benefits package including health, dental, and vision insurance
    401(k) with company match
    Performance-based bonuses
    Professional development opportunities
    Hybrid work environment with flexibility
    </jd>
</input2>
<output_json2>
    {
        "status": "success",
        "errors": null,
        "data": {
            "scores": {
            "overall": 57.5,
            "relevance": 55,
            "skillsAlignment": 60,
            "experienceMatch": 50,
            "achievementFocus": 65,
            "presentation": 55,
            "atsCompatibility": 70
            },
            "feedback": {
            "strengths": [
                "Extensive construction management experience (16 years) with progressive responsibility increases",
                "Holds relevant certifications including PMP and LEED Green Associate, which align with job preferences",
                "Demonstrated ability to manage multi-million dollar projects and lead large teams of workers and subcontractors",
                "Track record of delivering projects ahead of schedule and under budget, with quantifiable achievements",
                "Experience in stakeholder coordination and communication with various project participants"
            ],
            "areas_to_improve": [
                "Add experience with transportation infrastructure projects (bridges, highways, or transit facilities)",
                "Highlight knowledge of transportation-specific regulations (DOT, FHWA) if applicable",
                "Emphasize experience with larger budget projects (>$30 million) or explain transferability of skills",
                "Correct numerous spelling and grammatical errors that undermine professionalism",
                "Include experience with required software (Primavera P6, AutoCAD Civil 3D, BIM) or equivalent tools"
            ]
            },
            "matchAssessment": "Robert Thompson has solid construction management experience but lacks the specific transportation infrastructure background required for this position. His experience with commercial and residential projects up to $18 million doesn't fully align with the transportation focus and larger project scales ($20-50 million) required. Additionally, he lacks the Civil Engineering degree and PE license that are mandatory qualifications. While his project management skills are transferable, the significant domain mismatch makes him underqualified for this specific role."
        }
    }
</output_json2>
</example2>
<example3>
<input3>
    <task>
    You must evaluate and score a CV/résumé document provided in the `cv` section of this prompt. If a job description is provided in the `jd` section, score the CV against that specific role; otherwise, perform a generic quality assessment of the CV. Your task is to provide a comprehensive assessment, returning a valid JSON object that adheres to the STRICTLY validates against the <response_schema>. Focus on providing an objective evaluation with actionable feedback.
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
    # DR. SOPHIA J. TAYLOR-WILLIAMS, PHD
    ##### UX/UI DESIGN | DATA SCIENCE | MIXED MEDIA ARTIST
    -------------------

    sjwilliams@creativeemail-example.co.uk & sophiatw82@personalemail-example.com  
    +44 7911 123456 | +1 (415) 555-0127  
    Currently: Digital Nomad (Last location: Bali, Indonesia)  
    Permanent Address: Flat 3B, 72 Creative Quarter, Bristol BS1 5TF, United Kingdom  
    LinkedIn: in/sophia-taylor-williams | Portfolio: www.sophia-creates.example.com

    ## MY JOURNEY

    2020-Present: FREELANCE DATA VISUALIZATION CONSULTANT & UX DESIGNER
    * Working with Fortune 500 clients to transform complex data into intuitive visual stories
    * Leading workshops on data-driven design thinking (Google, Microsoft, Local Government)
    * Developing proprietary visualization framework using D3.js and React

    2019-Present: ADJUNCT LECTURER, BRISTOL SCHOOL OF DIGITAL ARTS
    Teaching undergraduate and graduate courses in Information Visualization (remote)

    2018-Present: CO-FOUNDER, DATAVIZ COLLECTIVE
    Building community platform connecting 3,000+ data visualization specialists worldwide

    2017-2020: SENIOR EXPERIENCE DESIGNER, GLOBAL BANKING GROUP
    London & Singapore offices
    Revamped digital banking interfaces resulting in 37% improvement in customer satisfaction

    2016-2018: UX RESEARCH FELLOW, UNIVERSITY INNOVATION LAB
    Bristol, UK
    Conducted groundbreaking research on cognitive load in information dashboard design

    2015-2017: DATA SCIENTIST, TECH STARTUP ACCELERATOR
    Analyzed startup performance metrics and developed predictive models for investment decisions

    Jan-Apr 2014: VISITING RESEARCHER, MIT MEDIA LAB
    Cambridge, Massachusetts
    Collaborated on experimental data sonification projects

    2010-2015: DIGITAL DESIGNER, CREATIVE AGENCY NETWORK
    Progressively responsible positions:
    * 2014-2015: Lead Designer (New York office)
    * 2012-2014: Senior Designer (London office)
    * 2010-2012: Junior Designer (Bristol office)

    2008-2010: VARIOUS INTERNSHIPS & FREELANCE PROJECTS
    Including BBC Digital, Small Design Studio, Self-initiated art installations

    ## ACADEMIC CREDENTIALS

    PhD, Human-Computer Interaction, University of Bristol (2012-2016)
    Thesis: "Cognitive Processing of Multi-dimensional Data Visualizations"
    Supervisor: Prof. Jonathan Richards, Director of Human Perception Lab

    MSc, Computational Arts, Goldsmiths University of London (2010-2011)
    Distinction
    Dissertation: "Algorithmic Aesthetics: Computer-Generated Art Systems"

    BA (Hons), Graphic Design & Psychology (Joint Honours), University of the Arts London (2007-2010)
    First Class Honours

    Self-Directed Learning:
    * Certified Data Scientist - Prestigious Online Academy (2018)
    * Advanced Statistical Analysis - Continuing Education (2017)
    * Machine Learning Specialization - MOOC Completion (2016)
    * Japanese Language - Intermediate Level - Tokyo Cultural Institute (2019-2020)

    ## TECHNICAL TOOLKIT & COMPETENCIES

    Design Tools: Adobe Creative Suite, Figma, Sketch
    Programming: Python, R, JavaScript (D3.js, React), SQL, HTML/CSS
    Data Analysis: Statistical analysis, A/B testing, SQL queries, R, Tableau, Power BI
    Languages: English (native), Japanese (intermediate), French (basic), Spanish (conversational)
    Methodologies: Design thinking, Agile, User-centered design, Design sprints
    Emerging Tech: Working knowledge of AR/VR prototyping, Generative AI systems

    ## NOTABLE PROJECTS & ACCOMPLISHMENTS

    Developed "DataSymphony" - An award-winning data sonification system translating financial market movements into musical compositions. Featured in WIRED magazine March 2019.

    Created "Visualizing Climate Change" - Interactive installation exhibited at Science Museum London 2018, COP26 Glasgow 2021, and Tokyo Design Week 2022. Visitor engagement averaged 17 minutes (industry average: 5 minutes).

    Published "Cognitive Load in Information Dashboard Design" in ACM CHI Conference Proceedings 2017. Paper has 200+ citations.

    TED Talk: "Making Data Human" at TEDxBristol 2019. 1.2M+ YouTube views.

    Patents pending:
    * "Method for Multi-sensory Data Representation" (US Patent Application #2019-0123456)
    * "Interactive Dashboard System with Adaptive User Interface" (EU Patent Application #EP31122024)

    ## WORKSHOPS & SPEAKING

    2022: Keynote Speaker, International Visualization Conference, Barcelona
    2021: Panel Moderator, "Future of Data Experience," Design Week, Amsterdam
    2020-Present: Monthly workshop facilitator, "Data Design for Non-Designers"
    2018-2019: Guest lectures at Royal College of Art, Copenhagen Institute of Design, RISD

    ## SELECTED PUBLICATIONS & MEDIA

    Taylor-Williams, S., Richards, J. (2019). Beyond Visual: Multi-sensory Data Experiences. Journal of Information Design, 12(3), 45-67.

    Taylor-Williams, S. (2018). Designing for Cognitive Ease. UX Magazine, September Issue.

    "Meet the Designer Making Data Beautiful" - Profile in Creative Review, June 2020

    "40 Under 40: Design Innovators" - Listed in Design Week, 2021

    ## SKILLS MATRIX

    DESIGN EXPERTISE:
    Information Design (Expert)
    UX/UI Design (Expert)
    Visual Communication (Expert)
    Interaction Design (Advanced)
    Service Design (Intermediate)
    Design Research (Expert)

    DATA EXPERTISE:
    Data Visualization (Expert)
    Statistical Analysis (Advanced)
    Data Storytelling (Expert)
    Machine Learning Application (Intermediate)
    Database Management (Basic)
    Business Intelligence (Advanced)

    TECHNICAL EXPERTISE:
    D3.js (Expert)
    Python Data Stack (Advanced)
    React.js (Intermediate)
    R Statistical Computing (Advanced)
    SQL (Intermediate)
    Tableau/Power BI (Expert)

    ## INDUSTRY EXPERIENCE

    Tech & Startups (7 years)
    Financial Services (3 years)
    Education (5 years)
    Healthcare (2 years project-based)
    Government/Public Sector (1 year consulting)
    Arts & Culture (4 years project-based)

    ## PERSONAL PROJECTS & INTERESTS

    Founder of "Data for Good Bristol" - Pro bono data visualization services for local NGOs

    Exhibiting mixed-media artist - Solo exhibitions at Bristol Contemporary 2019, Tokyo Small Gallery 2020

    Marathon runner - Completed London, Boston, and Tokyo marathons (2018-2022)

    Mentor for Women in Data UK - Supporting early-career women in data visualization and analytics

    Weekend baker specializing in experimental sourdough - Finalist in Local Baking Competition 2021

    ## ADDITIONAL INFORMATION

    Dual citizenship (UK/Canada)
    Available for international travel and remote collaboration
    Current driver's license (UK & International)
    References available upon request from academia, industry, and clients

    Note: I maintain a flexible working schedule across multiple time zones to accommodate global clients and teaching responsibilities. My work style blends academic rigor with creative exploration, resulting in solutions that are both evidence-based and aesthetically compelling.
    </cv>

    <jd>
    OPPORTUNITY: DIRECTOR OF INFORMATION ARCHITECTURE & VISUAL ANALYTICS
    ABOUT US
    Immersive Insights International (III) is a global consultancy at the intersection of computational analytics, information architecture, and human-centered interface development. We partner with Fortune 500 companies, academic institutions, and government agencies to transform complex information into intuitive user experiences. With offices in London, New York, Singapore, and remote team members across 12 countries, we embrace flexible work arrangements and value diverse perspectives.
    THE OPPORTUNITY
    We seek a Director of Information Architecture & Visual Analytics to lead groundbreaking projects for our global client base. The successful candidate will merge academic rigor with practical application, oversee our vector graphics development team, and contribute to our thought leadership initiatives. This role offers significant autonomy with the opportunity to develop proprietary frameworks while serving as a public ambassador for our methodologies.
    CORE RESPONSIBILITIES

    Lead cross-functional teams delivering computational analytics solutions for enterprise clients
    Transform complex business intelligence into accessible visual assets using proprietary frameworks
    Conduct training sessions for Fortune 500 executives on insight communication and decision support systems
    Enhance customer satisfaction metrics through interface refinement and human factors engineering
    Serve as adjunct faculty for our corporate learning academy
    Nurture our community of 3,000+ visual analytics practitioners
    Oversee development of interactive dashboards using contemporary web frameworks
    Publish research on cognitive assessment of multidimensional information displays
    Present at international symposia on information design and computational aesthetics
    Mentor junior team members in learning algorithms and statistical frameworks

    QUALIFICATIONS

    Doctoral qualification in Human Factors Engineering, Cognitive Computing, or equivalent field
    Master's degree in Digital Aesthetics, Computational Sciences, or related discipline
    Undergraduate studies combining visual communication and behavioral science
    10+ years progressive experience in information design roles
    Proven expertise with vector graphics tools, web frameworks, and computational languages
    Experience developing learning algorithms for predictive modeling
    Teaching experience at tertiary level
    Demonstrated history of executive-level workshop facilitation
    Publication record in peer-reviewed journals on information processing
    Experience with insight communication for financial institutions
    Proficiency in multiple programming environments and statistical packages

    TECHNICAL COMPETENCIES REQUIRED

    Vue.js, Angular, or similar component-based frameworks (expert level)
    Numpy, Pandas, Scikit-learn ecosystem (advanced proficiency)
    NumericJS, MathJS or equivalent computational libraries
    Statistical computing environments (advanced)
    RDBMS query optimization (intermediate)
    Executive reporting platforms (expert)

    IDEAL CANDIDATE PROFILE

    Combines academic credentials with practical implementation experience
    International perspective with cross-cultural communication skills
    Multilingual capabilities valued (especially East Asian languages)
    Comfortable with asynchronous collaboration across time zones
    Balance of analytical rigor and creative problem-solving
    Public speaking experience including high-profile idea forums
    Interest in multi-sensory information representation
    Registered intellectual property or patented methodologies
    Evidence of pro bono work applying analytics for social impact
    Diverse industry exposure including technology, finance, and education sectors

    WE OFFER

    Competitive compensation package with profit-sharing
    Flexible location arrangement with quarterly team gatherings
    Professional development stipend for continued learning
    Conference presentation and publication support
    Sabbatical program for independent research pursuits
    International project opportunities
    Collaborative, intellectually stimulating environment
    </jd>
</input3>
<output_json3>
    {
        "status": "success",
        "errors": null,
        "data": {
            "scores": {
            "overall": 72,
            "relevance": 65,
            "skillsAlignment": 70,
            "experienceMatch": 85,
            "achievementFocus": 88,
            "presentation": 92,
            "atsCompatibility": 58
            },
            "feedback": {
            "strengths": [
                "Extensive experience leading projects and teams in related fields demonstrates readiness for Director position",
                "Academic credentials perfectly match requirements with PhD, MSc, and BA in relevant disciplines",
                "Strong record of public speaking, workshops, and thought leadership aligns with ambassador aspect of role",
                "International experience and language skills support the global nature of the position",
                "Publication record and TED talk demonstrate thought leadership required for the role"
            ],
            "areas_to_improve": [
                "Incorporate terminology like 'Information Architecture' instead of 'UX/UI Design' to better match industry-specific language",
                "Add references to 'Visual Analytics' rather than 'Data Visualization' to align with current job market terminology",
                "Include experience with 'Vue.js or Angular' as mentioned in requirements rather than only 'React'",
                "Emphasize 'Human Factors Engineering' experience instead of 'UX Research' to match technical vocabulary in the field",
                "Reframe 'Machine Learning' experience as 'Learning Algorithms for Predictive Modeling' to match job description terminology"
            ]
            },
            "matchAssessment": "Dr. Taylor-Williams has the right qualifications, experience, and achievements for this role, making her a strong candidate in terms of actual capabilities. However, her CV uses significantly different terminology than the job description, which may cause ATS systems to miss important qualifications. While her experience with Fortune 500 clients, academic publishing, and global work perfectly matches the job requirements functionally, the keyword misalignment could prevent her application from being surfaced to hiring managers. With terminology adjustments, she would likely be considered an excellent match for this position."
        }
    }
</output_json3>
</example3>
<example4>
    <input4>
    <task>
    You must evaluate and score a CV/résumé document provided in the `cv` section of this prompt. If a job description is provided in the `jd` section, score the CV against that specific role; otherwise, perform a generic quality assessment of the CV. Your task is to provide a comprehensive assessment, returning a valid JSON object that adheres to the STRICTLY validates against the <response_schema>. Focus on providing an objective evaluation with actionable feedback.
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
    # DR. SOPHIA J. TAYLOR-WILLIAMS, PHD
    ##### UX/UI DESIGN | DATA SCIENCE | MIXED MEDIA ARTIST
    -------------------

    sjwilliams@creativeemail-example.co.uk & sophiatw82@personalemail-example.com  
    +44 7911 123456 | +1 (415) 555-0127  
    Currently: Digital Nomad (Last location: Bali, Indonesia)  
    Permanent Address: Flat 3B, 72 Creative Quarter, Bristol BS1 5TF, United Kingdom  
    LinkedIn: in/sophia-taylor-williams | Portfolio: www.sophia-creates.example.com

    ## MY JOURNEY

    2020-Present: FREELANCE DATA VISUALIZATION CONSULTANT & UX DESIGNER
    * Working with Fortune 500 clients to transform complex data into intuitive visual stories
    * Leading workshops on data-driven design thinking (Google, Microsoft, Local Government)
    * Developing proprietary visualization framework using D3.js and React

    2019-Present: ADJUNCT LECTURER, BRISTOL SCHOOL OF DIGITAL ARTS
    Teaching undergraduate and graduate courses in Information Visualization (remote)

    2018-Present: CO-FOUNDER, DATAVIZ COLLECTIVE
    Building community platform connecting 3,000+ data visualization specialists worldwide

    2017-2020: SENIOR EXPERIENCE DESIGNER, GLOBAL BANKING GROUP
    London & Singapore offices
    Revamped digital banking interfaces resulting in 37% improvement in customer satisfaction

    2016-2018: UX RESEARCH FELLOW, UNIVERSITY INNOVATION LAB
    Bristol, UK
    Conducted groundbreaking research on cognitive load in information dashboard design

    2015-2017: DATA SCIENTIST, TECH STARTUP ACCELERATOR
    Analyzed startup performance metrics and developed predictive models for investment decisions

    Jan-Apr 2014: VISITING RESEARCHER, MIT MEDIA LAB
    Cambridge, Massachusetts
    Collaborated on experimental data sonification projects

    2010-2015: DIGITAL DESIGNER, CREATIVE AGENCY NETWORK
    Progressively responsible positions:
    * 2014-2015: Lead Designer (New York office)
    * 2012-2014: Senior Designer (London office)
    * 2010-2012: Junior Designer (Bristol office)

    2008-2010: VARIOUS INTERNSHIPS & FREELANCE PROJECTS
    Including BBC Digital, Small Design Studio, Self-initiated art installations

    ## ACADEMIC CREDENTIALS

    PhD, Human-Computer Interaction, University of Bristol (2012-2016)
    Thesis: "Cognitive Processing of Multi-dimensional Data Visualizations"
    Supervisor: Prof. Jonathan Richards, Director of Human Perception Lab

    MSc, Computational Arts, Goldsmiths University of London (2010-2011)
    Distinction
    Dissertation: "Algorithmic Aesthetics: Computer-Generated Art Systems"

    BA (Hons), Graphic Design & Psychology (Joint Honours), University of the Arts London (2007-2010)
    First Class Honours

    Self-Directed Learning:
    * Certified Data Scientist - Prestigious Online Academy (2018)
    * Advanced Statistical Analysis - Continuing Education (2017)
    * Machine Learning Specialization - MOOC Completion (2016)
    * Japanese Language - Intermediate Level - Tokyo Cultural Institute (2019-2020)

    ## TECHNICAL TOOLKIT & COMPETENCIES

    Design Tools: Adobe Creative Suite, Figma, Sketch
    Programming: Python, R, JavaScript (D3.js, React), SQL, HTML/CSS
    Data Analysis: Statistical analysis, A/B testing, SQL queries, R, Tableau, Power BI
    Languages: English (native), Japanese (intermediate), French (basic), Spanish (conversational)
    Methodologies: Design thinking, Agile, User-centered design, Design sprints
    Emerging Tech: Working knowledge of AR/VR prototyping, Generative AI systems

    ## NOTABLE PROJECTS & ACCOMPLISHMENTS

    Developed "DataSymphony" - An award-winning data sonification system translating financial market movements into musical compositions. Featured in WIRED magazine March 2019.

    Created "Visualizing Climate Change" - Interactive installation exhibited at Science Museum London 2018, COP26 Glasgow 2021, and Tokyo Design Week 2022. Visitor engagement averaged 17 minutes (industry average: 5 minutes).

    Published "Cognitive Load in Information Dashboard Design" in ACM CHI Conference Proceedings 2017. Paper has 200+ citations.

    TED Talk: "Making Data Human" at TEDxBristol 2019. 1.2M+ YouTube views.

    Patents pending:
    * "Method for Multi-sensory Data Representation" (US Patent Application #2019-0123456)
    * "Interactive Dashboard System with Adaptive User Interface" (EU Patent Application #EP31122024)

    ## WORKSHOPS & SPEAKING

    2022: Keynote Speaker, International Visualization Conference, Barcelona
    2021: Panel Moderator, "Future of Data Experience," Design Week, Amsterdam
    2020-Present: Monthly workshop facilitator, "Data Design for Non-Designers"
    2018-2019: Guest lectures at Royal College of Art, Copenhagen Institute of Design, RISD

    ## SELECTED PUBLICATIONS & MEDIA

    Taylor-Williams, S., Richards, J. (2019). Beyond Visual: Multi-sensory Data Experiences. Journal of Information Design, 12(3), 45-67.

    Taylor-Williams, S. (2018). Designing for Cognitive Ease. UX Magazine, September Issue.

    "Meet the Designer Making Data Beautiful" - Profile in Creative Review, June 2020

    "40 Under 40: Design Innovators" - Listed in Design Week, 2021

    ## SKILLS MATRIX

    DESIGN EXPERTISE:
    Information Design (Expert)
    UX/UI Design (Expert)
    Visual Communication (Expert)
    Interaction Design (Advanced)
    Service Design (Intermediate)
    Design Research (Expert)

    DATA EXPERTISE:
    Data Visualization (Expert)
    Statistical Analysis (Advanced)
    Data Storytelling (Expert)
    Machine Learning Application (Intermediate)
    Database Management (Basic)
    Business Intelligence (Advanced)

    TECHNICAL EXPERTISE:
    D3.js (Expert)
    Python Data Stack (Advanced)
    React.js (Intermediate)
    R Statistical Computing (Advanced)
    SQL (Intermediate)
    Tableau/Power BI (Expert)

    ## INDUSTRY EXPERIENCE

    Tech & Startups (7 years)
    Financial Services (3 years)
    Education (5 years)
    Healthcare (2 years project-based)
    Government/Public Sector (1 year consulting)
    Arts & Culture (4 years project-based)

    ## PERSONAL PROJECTS & INTERESTS

    Founder of "Data for Good Bristol" - Pro bono data visualization services for local NGOs

    Exhibiting mixed-media artist - Solo exhibitions at Bristol Contemporary 2019, Tokyo Small Gallery 2020

    Marathon runner - Completed London, Boston, and Tokyo marathons (2018-2022)

    Mentor for Women in Data UK - Supporting early-career women in data visualization and analytics

    Weekend baker specializing in experimental sourdough - Finalist in Local Baking Competition 2021

    ## ADDITIONAL INFORMATION

    Dual citizenship (UK/Canada)
    Available for international travel and remote collaboration
    Current driver's license (UK & International)
    References available upon request from academia, industry, and clients

    Note: I maintain a flexible working schedule across multiple time zones to accommodate global clients and teaching responsibilities. My work style blends academic rigor with creative exploration, resulting in solutions that are both evidence-based and aesthetically compelling.
    </cv>

    <jd>
    SKILLED BRICKLAYER / MASONRY SPECIALIST
    COMPANY OVERVIEW
    Cornerstone Construction Services is a well-established masonry contractor specializing in commercial and high-end residential construction projects across the Southeast region. With 25 years in business, we've built a reputation for quality craftsmanship, on-time project completion, and exceptional structural integrity. We're currently expanding our team to meet growing demand.
    JOB DESCRIPTION
    We are seeking experienced Bricklayers to join our team on multiple construction sites. The successful candidate will be responsible for constructing and repairing walls, partitions, arches, fireplaces, chimneys, and other structures using bricks, concrete blocks, and natural stone. This is a physically demanding role requiring extensive hands-on experience with masonry techniques and tools.
    KEY RESPONSIBILITIES

    Lay and bind building materials such as bricks, concrete blocks, and natural stones using mortar and other substances
    Measure, mark, and cut bricks and blocks to required size using power saws or hand tools
    Mix mortar, concrete, and grout according to specific project requirements
    Construct and repair walls, partitions, arches, fireplaces, chimneys, and other structures
    Interpret blueprints and construction plans to determine dimensions and specifications
    Ensure proper alignment of structures using levels, plumb bobs, and laser levels
    Clean excess mortar from surfaces using appropriate tools
    Install insulation, vapor barriers, and flashing
    Set up and break down scaffolding and work platforms
    Maintain a clean and safe work area
    Train and supervise apprentices and laborers as required

    QUALIFICATIONS

    Minimum 5 years of verifiable experience as a bricklayer or mason
    Completion of a recognized apprenticeship program or vocational training in masonry
    Thorough knowledge of construction materials, methods, and tools related to masonry
    Ability to read and interpret construction blueprints and technical documents
    Strong mathematical skills for accurate measurements and calculations
    Physical stamina to work in all weather conditions and perform heavy lifting (50+ lbs regularly)
    Valid driver's license and reliable transportation to job sites
    OSHA 10-hour or 30-hour certification preferred
    Scaffold safety certification preferred

    REQUIRED SKILLS

    Proficiency with masonry tools (brick hammers, trowels, jointers, levels, etc.)
    Experience with different bond patterns (running, Flemish, English, stack, etc.)
    Knowledge of mortar mixing ratios for different applications
    Expertise in cutting techniques for various materials
    Ability to construct corners, openings, and special features
    Understanding of moisture management and structural integrity principles
    Experience with stone masonry techniques
    Familiarity with construction site safety protocols
    Basic scaffolding assembly and use

    PHYSICAL REQUIREMENTS

    Must be able to stand, kneel, and bend for extended periods
    Regularly lift and move materials weighing up to 50 pounds
    Work at heights on scaffolding and ladders
    Perform repetitive movements and maintain balance
    Work outdoors in various weather conditions
    Wear required personal protective equipment throughout shift

    COMPENSATION & BENEFITS

    Competitive hourly wage based on experience ($22-$35/hour)
    Performance-based bonuses
    Health insurance
    401(k) with company match
    Paid time off
    Tool allowance
    Opportunity for advancement to Foreman or Project Supervisor
    Regular, full-time hours with overtime availability

    WORK ENVIRONMENT

    Active construction sites
    Outdoor work in various weather conditions
    Exposure to dust, noise, and construction materials
    Variable locations requiring daily travel to job sites

    Cornerstone Construction Services is an Equal Opportunity Employer committed to hiring a diverse workforce and sustaining an inclusive culture.
    </jd>
</input4>
<output_json4>
    {
        "status": "success",
        "errors": null,
        "data": {
            "scores": {
            "overall": 18,
            "relevance": 10,
            "skillsAlignment": 5,
            "experienceMatch": 5,
            "achievementFocus": 15,
            "presentation": 85,
            "atsCompatibility": 12
            },
            "feedback": {
            "strengths": [
                "Excellent presentation of CV with clear organization and professional formatting",
                "Demonstrates strong project management capabilities that could potentially transfer to construction project contexts",
                "Shows ability to work with diverse teams which is valuable in any workplace environment",
                "Record of completing projects successfully indicates reliability and results-orientation",
                "International experience suggests adaptability to different working environments"
            ],
            "areas_to_improve": [
                "Missing masonry experience: Consider enrolling in a masonry vocational program or weekend workshops to gain fundamental bricklaying skills and knowledge of materials",
                "Lack of physical construction experience: Volunteer with organizations like Habitat for Humanity to gain hands-on construction experience while leveraging your existing project management skills",
                "No construction certifications: Pursue entry-level OSHA 10-hour construction safety certification online (approximately 2 days) as a first step toward industry credentials",
                "No demonstrated knowledge of construction tools: Take introductory courses at local community colleges or home improvement stores that offer basic construction tool training",
                "Digital focus without construction application: Explore how your data visualization skills could be applied to construction planning or BIM (Building Information Modeling) as a transitional career path before moving into hands-on roles"
            ]
            },
            "matchAssessment": "Dr. Taylor-Williams' CV reveals a complete mismatch for the Bricklayer position. Her background is entirely in digital design, data visualization, and academic research with no construction experience whatsoever. While she demonstrates excellent communication and project management skills, these alone are insufficient for the role. If genuinely interested in transitioning to construction, she would need to pursue formal training through an apprenticeship program (typically 3-4 years), gain physical construction experience, and obtain relevant certifications. Alternatively, she might consider roles that bridge her digital expertise with construction, such as construction technology implementation or BIM coordination, as a more feasible career transition path."
        }
    }
</output_json4>
</example4>
</few_shot_examples>