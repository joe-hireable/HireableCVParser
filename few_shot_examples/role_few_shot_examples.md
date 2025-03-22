<few_shot_examples>
<example1>
<assessment1>
   ## Strengths
   - **Expanded Summary**: Added valuable context about working with international teams and maintaining consistency across platforms
   - **Improved Highlight Language**: Enhanced the impact of bullet points through stronger action verbs and more detailed explanations
   - **Comprehensive Self-Assessment**: Included thoughtful feedback with specific strengths and actionable improvement areas
   - **Perfect JSON Structure**: Maintained valid JSON formatting with appropriate nesting and syntax
   ## Areas to Improve
   - **Date hallucination - CRITICAL ERROR - automatic 0 score**: Added month to dates ("Jan 2017" - "Dec 2020" instead of just "2017"-"2020"). Any hallucinations will automatically cause a response score of 0/100.
   - **Spelling Inconsistency**: Used "visualisation" (UK spelling) in highlights while the original used "visualization" (US spelling) - should maintain consistency
   - **Missed Implementation Opportunity**: Suggested adding specific tools and more quantifiable achievements in the feedback section, but didn't incorporate these improvements in the actual optimization
   - **Feedback Inclusion**: The feedback section is likely meant as meta-information rather than content to be included in the final CV entry
   ## Notes
   The LLM successfully enhanced the employment entry by adding professional polish and more context while preserving the core accomplishments. The self-assessment component shows good critical thinking, though it would be more valuable if the LLM had implemented some of its own suggestions. Without seeing the full CV, it's difficult to assess alignment with overall document tone and style.
   ## Score (out of 100)
   0/100
</assessment1>
<input1>
   <task>
   You must optimize a specific work experience entry from the CV/résumé document provided in the `cv` section of this prompt, with reference to the job description in the `jd` section.
   <section>
   {
                     "company": "Global Banking Group",
                     "start": "2017",
                     "end": "2020",
                     "current": false,
                     "summary": "Led experience design initiatives across London and Singapore offices, focusing on improving digital banking interfaces and customer journeys.",
                     "highlights": [
                     "Revamped digital banking interfaces resulting in 37% improvement in customer satisfaction metrics.",
                     "Collaborated across international offices to implement consistent design systems that accommodated cultural differences in financial information visualization."
                     ],
                     "roles": [
                     {
                           "title": "Senior Experience Designer",
                           "start": "2017",
                           "end": "2020",
                           "current": false
                     }
                     ]
                  }
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
   <${jd}>
   </jd>
</input1>
<output_json1>
   {
      "status": "success",
      "errors": null,
      "data": {
         "company": "Global Banking Group",
         "start": "Jan 2017",
         "end": "Dec 2020",
         "current": false,
         "summary": "Led experience design initiatives across London and Singapore offices, focusing on improving digital banking interfaces and customer journeys. Worked with international teams to ensure design systems accommodated cultural differences while maintaining consistency across global platforms.",
         "highlights": [
               "Redesigned digital banking interfaces by implementing innovative user experience solutions, resulting in a significant 37% improvement in customer satisfaction metrics.",
               "Developed consistent design systems across international offices by collaborating with global teams to accommodate cultural differences in financial information visualisation."
         ],
         "roles": [
               {
                  "title": "Senior Experience Designer",
                  "start": "Jan 2017",
                  "end": "Dec 2020",
                  "current": false
               }
         ],
         "feedback": {
               "strengths": [
                  "Excellent quantitative achievement with the 37% improvement in customer satisfaction metrics",
                  "Clear demonstration of international experience across multiple offices",
                  "Strong emphasis on the intersection of design and cultural considerations",
                  "Highlights experience with financial information visualisation, which is relevant to data-focused roles",
                  "Shows leadership capabilities in experience design initiatives"
               ],
               "areas_to_improve": [
                  "Add more specific technical tools used (e.g., Figma, Sketch) that were applied in this role",
                  "Include more quantifiable achievements beyond the customer satisfaction metric",
                  "Mention specific financial products or services that were redesigned",
                  "Highlight collaboration with specific departments (e.g., product, marketing, development)",
                  "Add information about research methodologies or design frameworks employed in this position"
               ]
         }
      }
   }
</output_json1>
</example1>
<example2>
<assessment2>
   ## Strengths
   - **Data Integrity**: Maintains the exact date format from the original input (2017-2020) without hallucinating specificity
   - **Appropriate Summary Enhancement**: Adds relevant context about UX/UI expertise and cross-cultural design solutions without fabricating specific details
   - **Preserved Original Highlights**: Maintains the factual accuracy of the achievement bullet points
   - **Well-structured Feedback**: Provides thoughtful self-assessment with specific strengths and actionable improvement areas
   - **Valid JSON Format**: Maintains proper JSON structure throughout the response
   - **Consistency**: Preserves the original US spelling "visualization" throughout the document
   - **Date Correctness**: Correctly parses just the year (YYYY) date as months are not present in the input context.
   ## Areas to Improve
   - **Missed Implementation Opportunity**: Similar to the previous response, suggests improvements in the feedback section (like mentioning specific tools and methodologies) but doesn't incorporate these into the actual optimization
   ## Notes
   This response successfully enhances the employment entry while carefully avoiding hallucinations. It strikes a good balance between adding professional context and preserving factual accuracy. The LLM has clearly learned from previous mistakes regarding date formatting. The self-assessment shows good critical thinking about how the entry could be further improved, though implementing some of these suggestions directly would have demonstrated more initiative.
   ## Score (out of 100)
   95/100
</assessment2>
<input2>
   <task>
   You must optimize a specific work experience entry from the CV/résumé document provided in the `cv` section of this prompt, with reference to the job description in the `jd` section.
   <section>
   {
                     "company": "Global Banking Group",
                     "start": "2017",
                     "end": "2020",
                     "current": false,
                     "summary": "Led experience design initiatives across London and Singapore offices, focusing on improving digital banking interfaces and customer journeys.",
                     "highlights": [
                     "Revamped digital banking interfaces resulting in 37% improvement in customer satisfaction metrics.",
                     "Collaborated across international offices to implement consistent design systems that accommodated cultural differences in financial information visualization."
                     ],
                     "roles": [
                     {
                           "title": "Senior Experience Designer",
                           "start": "2017",
                           "end": "2020",
                           "current": false
                     }
                     ]
                  }
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
   <${jd}>
   </jd>
</input2>
<output_json2>
   {
      "status": "success",
      "errors": null,
      "data": {
         "company": "Global Banking Group",
         "start": "2017",
         "end": "2020",
         "current": false,
         "summary": "Led experience design initiatives across London and Singapore offices, focusing on improving digital banking interfaces and customer journeys. Applied UX/UI expertise to enhance financial service digital experiences and implement cross-cultural design solutions.",
         "highlights": [
               "Revamped digital banking interfaces resulting in 37% improvement in customer satisfaction metrics.",
               "Collaborated across international offices to implement consistent design systems that accommodated cultural differences in financial information visualization."
         ],
         "roles": [
               {
                  "title": "Senior Experience Designer",
                  "start": "2017",
                  "end": "2020",
                  "current": false
               }
         ],
         "feedback": {
               "strengths": [
                  "Includes a specific, measurable achievement with the 37% improvement in customer satisfaction metrics",
                  "Demonstrates cross-cultural design experience across international offices (London and Singapore)",
                  "Shows ability to work in the financial services sector which requires attention to detail",
                  "Indicates experience with customer journey mapping and interface design",
                  "Demonstrates ability to implement consistent design systems across different cultural contexts"
               ],
               "areas_to_improve": [
                  "Add specific banking products or platforms worked on (e.g., mobile banking app, online investment portal)",
                  "Include collaboration details with different departments (e.g., product, development, compliance)",
                  "Mention specific UX methodologies or frameworks utilized during the experience",
                  "Add more quantifiable achievements beyond the customer satisfaction metric",
                  "Specify relevant technologies, software or design tools used during this role"
               ]
         }
      }
   }
</output_json2>
</example2>
<example3>
<assessment3>
   ## Strengths
   - **Content Enhancement**: Successfully transformed the original bullet points into more impactful statements using stronger action verbs ("Developed and implemented," "Spearheaded," "Cultivated")
   - **Professional Language**: Significantly improved the language quality while maintaining all factual information from the original CV
   - **Accurate Data Handling**: Preserved all key information including dates, company name, job title, project values, and team sizes without hallucination
   - **Strategic Consolidation**: Eliminated redundancy by removing the duplicated "Assisted with budget management" point that appeared in both summary and highlights
   - **Value Clarification**: Added dollar signs to project values ($5-10 million) for clearer presentation
   - **Comprehensive Feedback**: Provided specific, actionable improvement suggestions relevant to the construction industry
   ## Areas to Improve
   - **Highlight Ordering**: Changed the sequence of bullet points from the original section, though the reordering does create a more logical flow
   - **Implementation Gap**: Suggests improvements in the feedback section without implementing them in the actual optimization
   ## Notes
   This response demonstrates excellent judgment in enhancing the employment entry while strictly adhering to the factual information provided. The LLM successfully corrected numerous spelling errors present in the original CV and improved readability without fabricating details. The optimization focuses on strengthening language and presentation rather than adding unverifiable content, showing good restraint and accuracy awareness.
   ## Score (out of 100)
   95/100
</assessment3>
<input3>
   <task>
   You must optimize a specific work experience entry from the CV/résumé document provided in the `cv` section of this prompt, with reference to the job description in the `jd` section.

   <section>
   {
                     "company": "Construction Solutions Inc",
                     "start": "2014",
                     "end": "2018",
                     "current": false,
                     "summary": "Worked closely with senior site managers to coordinate daily activities of residential and commercial projects valued between $5-10 million. Assisted with budget management, schedule tracking, and quality inspections.",
                     "highlights": [
                     "Improved documentation processes for material deliveries, which was adopted company-wide.",
                     "Helped implement digital tracking system replacing older paper-based system, improving efficiency.",
                     "Supervised crews of 15-25 workers during various project phases.",
                     "Managed relationships with local inspectors, maintaining good standing with regulatory authorities.",
                     "Responsible for communication between subcontractors and design team to resolve technical issues.",
                     "Assisted with budget management, schedule tracking, and quality inspections."
                     ],
                     "roles": [
                     {
                           "title": "Assistant Site Manager",
                           "start": "2014",
                           "end": "2018",
                           "current": false
                     }
                     ]
                  }
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
   <${jd}>
   </jd>
</input3>
<output_json3>
   {
      "status": "success",
      "errors": null,
      "data": {
         "company": "Construction Solutions Inc",
         "start": "2014",
         "end": "2018",
         "current": false,
         "summary": "Coordinated daily operations for residential and commercial construction projects valued at $5-10 million, collaborating with senior management to ensure timely completion. Managed budget tracking, schedule optimization, and quality control inspections while facilitating communication between design teams and subcontractors to resolve technical issues.",
         "highlights": [
               "Developed and implemented improved documentation processes for material deliveries that was recognized for its effectiveness and adopted company-wide, enhancing overall procurement efficiency.",
               "Spearheaded transition from paper-based to digital tracking system, significantly improving project monitoring efficiency and real-time data accessibility across project teams.",
               "Effectively supervised diverse construction crews of 15-25 workers during critical project phases, ensuring adherence to safety protocols and quality standards.",
               "Cultivated strong relationships with local building inspectors and regulatory authorities, maintaining company's excellent compliance record and facilitating timely approvals.",
               "Served as key liaison between subcontractors and design team, successfully resolving technical issues to prevent delays and maintain project momentum."
         ],
         "roles": [
               {
                  "title": "Assistant Site Manager",
                  "start": "2014",
                  "end": "2018",
                  "current": false
               }
         ],
         "feedback": {
               "strengths": [
                  "Clear demonstration of project value range ($5-10 million) establishes scale of responsibility",
                  "Experience supervising sizeable crews (15-25 workers) demonstrates leadership capacity",
                  "Shows initiative through improvement of documentation processes and system implementation",
                  "Highlights ability to maintain positive relationships with regulatory authorities, which is crucial in construction",
                  "Demonstrates cross-functional communication skills between technical teams and subcontractors"
               ],
               "areas_to_improve": [
                  "Add specific metrics on efficiency improvements from the digital tracking system implementation (e.g., percentage of time saved)",
                  "Include more specific details about budget management responsibilities and any cost savings achieved",
                  "Quantify the impact of the improved documentation processes (e.g., reduction in material delivery delays)",
                  "Elaborate on specific technical issues resolved between subcontractors and design team to showcase problem-solving abilities",
                  "Incorporate more construction-specific terminology relevant to residential and commercial projects to demonstrate industry expertise"
               ]
         }
      }
   }
</output_json3>
</example3>
<example4>
<assessment4>
# Assessment of LLM Response
## Strengths
- **Factual Accuracy**: All added details are supported by the CV (company name "Inc." suffix, technologies, testing metrics)
- **Multiple Role Identification**: Correctly identifies that the user has held multiple roles within the same company and returns the correct resultant JSON structure.
- **Enhanced Technical Specificity**: Added relevant technologies (React, Redux, Node.js, Express) that showcase specific expertise
- **Improved Completeness**: Added the missing highlight about "automated testing strategies achieving 85% code coverage" from the CV
- **Maintained Quantifiable Achievements**: Preserved all important metrics (95% reduction, $2.4M savings, 78% downtime reduction)
- **Comprehensive Self-Assessment**: Provided thoughtful analysis of strengths and potential improvements
- **Valid JSON Structure**: Maintained proper formatting and structure throughout
## Areas to Improve
- **Highlight Reordering**: Changed the sequence of achievements without clear strategic reasoning
- **Implementation Gap**: The feedback suggests improvements (like adding more about scale and fintech domain knowledge) that could have been incorporated from the CV
## Notes
This response demonstrates excellent attention to detail by pulling in specific technologies and achievements that were present in the CV but not included in the original section. The LLM showed good judgment in identifying which details would strengthen the employment entry without fabricating information. It correctly identified the company name as including "Inc." based on the CV header. The addition of specific technologies and the testing achievement significantly enhances the technical specificity and value of the entry.
## Score (out of 100)
94/100
</assessment4>
<input4>
   <task>
   You must optimize a specific work experience entry from the CV/résumé document provided in the `cv` section of this prompt, with reference to the job description in the `jd` section.
   <section>
   {
                     "company": "Fintech Startup",
                     "start": "2019",
                     "end": null,
                     "current": true,
                     "summary": "Led payment processing infrastructure handling millions of transactions daily and managed a team of 5 engineers implementing microservices architecture. Developed responsive web interfaces and RESTful APIs.",
                     "highlights": [
                     "Redesigned authentication system reducing unauthorized access attempts by 95%",
                     "Implemented real-time fraud detection using machine learning models, saving approximately $2.4M annually",
                     "Established CI/CD pipeline improving deployment frequency from biweekly to daily",
                     "Led migration from monolithic architecture to microservices, reducing system downtime by 78%",
                     "Mentored junior engineers through weekly code reviews and pair programming sessions"
                     ],
                     "roles": [
                     {
                           "title": "Senior Software Engineer / Tech Lead",
                           "start": "2020",
                           "end": null,
                           "current": true
                     },
                     {
                           "title": "Full Stack Engineer",
                           "start": "2019",
                           "end": "2020",
                           "current": false
                     }
                     ]
                  }
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
   # ALEXANDER CHEN
   alex.chen1984@email.example.com | 415.555.7890
   San Francisco Bay Area
   ## **SKILLS & EXPERTISE**
   Programming Languages: Python, JavaScript, TypeScript, Go, C++, Java, Ruby, Rust, PHP
   Frameworks & Libraries: React, Vue.js, Angular, Django, Flask, Express.js, Spring Boot
   Data & ML: TensorFlow, PyTorch, Pandas, scikit-learn, SQL, Spark, Hadoop
   Cloud: AWS (Certified Solutions Architect), Google Cloud Platform, Azure, Kubernetes, Docker
   DevOps: Jenkins, CircleCI, GitHub Actions, Terraform, Ansible, Puppet
   Other: Agile methodologies, System Design, REST APIs, GraphQL, Microservices
   ## **ABOUT ME**
   Versatile software engineer with a passion for building scalable, resilient systems and tackling challenging technical problems. Over 10+ years experience spanning startups and large enterprises across fintech, e-commerce, and social media sectors. Known for improving system performance, mentoring junior engineers, and delivering complex projects on time. Looking for opportunities to leverage my technical leadership skills in high-growth environments.
   I've spent countless hours optimizing databases and refactoring legacy codebases to improve performance. While I enjoy the technical aspects of software engineering, I find the most satisfaction in collaborating with cross-functional teams and creating software that solves real business problems. My approach combines pragmatic solutions with forward-thinking architecture, ensuring systems can scale while maintaining reliability.
   ## **WORK HISTORY**
   ### **FINTECH STARTUP, INC** 
   *Senior Software Engineer / Tech Lead*
   Responsible for the entire payment processing infrastructure handling millions of transactions daily. Led a team of 5 engineers building microservices architecture.
   Key Contributions:
   - Redesigned authentication system reducing unauthorized access attempts by 95%
   - Implemented real-time fraud detection using machine learning models, saving approximately $2.4M annually
   - Established CI/CD pipeline improving deployment frequency from biweekly to daily
   - Led migration from monolithic architecture to microservices, reducing system downtime by 78%
   - Mentored junior engineers through weekly code reviews and pair programming sessions
   *Full Stack Engineer*
   2019-2020
   - Developed responsive web interfaces using React and Redux
   - Built RESTful APIs with Node.js and Express
   - Implemented automated testing strategies achieving 85% code coverage
   ### **SOCIAL MEDIA GIANT**
   *Software Development Engineer II* | Jan 2017 - Nov 18
   Led backend development for user engagement features reaching 50M+ daily active users. Collaborated with product managers and designers to define technical specifications.
   * Architected and implemented notification delivery system processing 500M+ notifications/day
   * Reduced database query latency by 70% through query optimization and proper indexing
   * Led migration from REST to GraphQL, improving mobile client performance by 35%
   * Developed real-time analytics dashboard for monitoring feature adoption and performance
   * Contributed to open-source projects as company representative
   ### **RETAIL ANALYTICS CORP**
   *Data Engineer*
   2013 to 2015
   - Designed ETL pipelines processing 5TB of daily transaction data from 500+ retail locations
   - Implemented data lake architecture on AWS S3 reducing storage costs by 60%
   - Created customizable dashboard using D3.js allowing business users to visualize sales trends
   - Optimized Spark jobs reducing processing time from 4 hours to 45 minutes
   - Collaborated with data science team to implement machine learning models for demand forecasting
   ### **TECHNOLOGY CONSULTING GROUP**
   *Technical Consultant* 
   Focused on helping mid-sized businesses modernize legacy systems and implement cloud-based solutions.
   Main projects:
   - Led cloud migration for healthcare provider moving on-premise systems to AWS, resulting in 40% cost savings
   - Implemented DevOps practices for manufacturing client reducing deployment time from weeks to days
   - Developed custom CRM integration for financial services firm improving customer service response time by 65%
   - Conducted technical training sessions for client engineering teams
   ### **E-COMMERCE PLATFORM**
   *Software Engineer* | 2015-Dec 2016
   - Led development of inventory management system supporting 10,000+ SKUs
   - Designed and implemented search functionality with Elasticsearch improving response time by 300%
   - Created automated pricing algorithm accounting for competitor prices, demand, and inventory levels
   - Implemented A/B testing framework allowing product team to optimize conversion rates
   - Reduced infrastructure costs by 25% through serverless architecture adoption
   *Junior Developer*
   - Maintained product catalog APIs
   - Fixed bugs in checkout process
   - Implemented frontend features using jQuery and Backbone.js
   - Participated in daily stand-ups and sprint planning
   - Generated weekly performance reports for stakeholders
   ## EARLIER EXPERIENCE
   ### **LARGE ENTERPRISE CORPORATION**
   *Associate System Analyst* | January 2011 - March 2013
   Supported enterprise resource planning systems serving 5,000+ employees across 20 locations.
   - Troubleshot and resolved system issues affecting business operations
   - Automated weekly reporting processes saving 15 person-hours per week
   - Collaborated with vendors to implement system upgrades and patches
   - Documented system architectures and created training materials
   - Participated in 24/7 on-call rotation supporting mission-critical systems
   ### **STARTUP ACCELERATOR**
   *Technical Intern*
   Summer 2010
   - Assisted early-stage startups with technical implementations
   - Developed prototype applications based on founder specifications
   - Conducted technical due diligence for potential investments
   - Created technical documentation for various projects
   - Participated in pitch preparation sessions providing technical validation
   ## **EDUCATION**
   ### STANFORD UNIVERSITY
   **Master of Science, Computer Science**
   2010
   Thesis: "Distributed Consensus Algorithms in Unreliable Networks"
   Relevant Coursework: Advanced Algorithms, Machine Learning, Distributed Systems, Database Management Systems, Computer Graphics
   ### UNIVERSITY OF CALIFORNIA, BERKELEY
   **Bachelor of Science, Electrical Engineering and Computer Science**
   Graduated: 2008
   GPA: 3.85/4.0
   Honors Thesis: "Energy-Efficient Routing Protocols for Wireless Sensor Networks"
   Activities: ACM Programming Team, Robotics Club, Undergraduate Research Assistant
   ## **CERTIFICATIONS & PROFESSIONAL DEVELOPMENT**
   * AWS Certified Solutions Architect – Professional (2021)
   * Google Cloud Professional Data Engineer (2020)
   * Certified Kubernetes Administrator (2019)
   * MongoDB Certified Developer (2018)
   * Certified Scrum Master (2016)
   * Advanced TensorFlow Certification (January 2022)
   * CompTIA Security+ (2017)
   ## **PROJECTS**
   ### **OPEN SOURCE CONTRIBUTIONS**
   * **Scalable Task Queue** – Creator and maintainer of distributed task queue system with 2,000+ GitHub stars
   * Implemented in Go with support for multiple backends (Redis, RabbitMQ, Kafka)
   * Features priority queuing, job scheduling, and dead letter queues
   * Used in production by 10+ companies handling millions of tasks daily
   * **React Component Library** – Contributor to popular UI component library
   * Implemented responsive data table component
   * Fixed accessibility issues in form components
   * Improved test coverage from 70% to 92%
   * **Python Data Processing Framework** – Core contributor
   * Designed and implemented streaming API enabling processing of infinitely large datasets
   * Optimized core algorithms reducing memory usage by 40%
   * Added comprehensive documentation and examples
   ## **SIDE PROJECTS**
   * **Personal Finance Tracker** – Full-stack application for tracking expenses and investments
   * Built with React, Node.js, and MongoDB
   * Features include budget planning, investment tracking, and expense categorization
   * 500+ active users
   * **Real-time Collaborative Editor** – WebSocket-based collaborative text editor
   * Implemented Operational Transformation algorithms for conflict resolution
   * Built with Vue.js, Express, and Socket.io
   * Open-sourced with 150+ GitHub stars
   ## **PATENTS & PUBLICATIONS**
   * Patent: "Method and System for Real-time Fraud Detection in Payment Processing" (US Patent #9,XXX,XXX)
   * Publication: "Scaling Microservices at Fintech: Lessons Learned" – InfoQ, 2020
   * Publication: "Optimizing Database Performance in High-Throughput Applications" – ACM Queue, 2018
   * Conference Talk: "Building Resilient Payment Systems" – QCon San Francisco, 2019
   * Workshop: "Practical Machine Learning for Fraud Detection" – PyData, 2018
   ## **TECHNICAL LEADERSHIP & MENTORSHIP**
   * Mentored 15+ junior engineers who progressed to senior roles
   * Led technical interview process at Fintech Startup, hiring 20+ engineers
   * Created internal training program for new engineering hires
   * Guest lecturer for "Advanced Web Development" course at local coding bootcamp
   * Organized monthly technical talks inviting industry experts
   ## **ADDITIONAL ACCOMPLISHMENTS**
   * Reduced AWS costs by 45% at Fintech Startup through architecture optimization
   * Implemented CI/CD pipeline at Social Media Giant reducing deployment time from days to hours
   * Received "Technical Excellence Award" at E-Commerce Platform for inventory system redesign
   * Led successful migration of legacy monolith to microservices at Retail Analytics Corp
   * Created internal tool at Technology Consulting Group used by 100+ consultants for project management
   ## Languages
   English (Native)
   Mandarin Chinese (Fluent)
   Spanish (Intermediate)
   French (Basic)
   I spent two years working in Shanghai as part of a special project for Large Enterprise Corporation which helped me develop my Chinese language skills. I've been taking Spanish classes for the last 3 years and can hold basic conversations. I studied French in high school and can understand simple phrases.
   ## **INVOLVEMENT & INTERESTS**
   * Organize local meetup group for Go programming language (500+ members)
   * Volunteer coding instructor for underrepresented youth in technology
   * Hackathon judge for university competitions
   * Avid rock climber and trail runner
   * Amateur photographer specializing in landscape and street photography
   ## **REFERENCES**
   Professional references available upon request. Previous managers and colleagues can attest to my technical abilities, leadership skills, and work ethic.
   The projects I'm most proud of involved solving complex technical challenges while delivering significant business value. At Fintech Startup, our team rebuilt the payment processing system while maintaining 99.99% uptime, processing over $5B in annual transactions. At Social Media Giant, I led the implementation of a notification system that improved user engagement by 23% across all platforms.
   I'm particularly interested in roles where I can continue to grow as a technical leader while mentoring the next generation of engineers. I believe strongly in building resilient systems that can scale with business needs and adapt to changing requirements.
   # TECHNICAL SKILLS BREAKDOWN
   ## Programming Languages
   - Python: 9+ years, expert-level proficiency
   - JavaScript/TypeScript: 8+ years, expert-level proficiency
   - Go: 5+ years, advanced proficiency
   - Java: 7+ years, advanced proficiency
   - C++: 4+ years, intermediate proficiency
   - Ruby: 3+ years, intermediate proficiency
   - Rust: 2+ years, intermediate proficiency
   - PHP: 3+ years, intermediate proficiency
   ## Frontend Technologies
   - React: Expert (7+ years)
   - Vue.js: Advanced (4+ years)
   - Angular: Intermediate (3+ years)
   - HTML5/CSS3: Expert (10+ years)
   - Redux/Vuex: Advanced (5+ years)
   - Webpack/Babel: Advanced (5+ years)
   - Jest/Testing Library: Advanced (4+ years)
   - Responsive Design: Expert (7+ years)
   ## Backend Technologies
   - Node.js/Express: Expert (6+ years)
   - Django/Flask: Advanced (5+ years)
   - Spring Boot: Intermediate (3+ years)
   - RESTful API Design: Expert (8+ years)
   - GraphQL: Advanced (4+ years)
   - Microservices Architecture: Expert (5+ years)
   - Message Queues (RabbitMQ, Kafka): Advanced (5+ years)
   - WebSockets: Advanced (4+ years)
   ## Database & Data Technologies
   - SQL (PostgreSQL, MySQL): Expert (9+ years)
   - NoSQL (MongoDB, Cassandra): Advanced (6+ years)
   - Redis: Advanced (5+ years)
   - Elasticsearch: Advanced (5+ years)
   - Data Warehousing: Intermediate (4+ years)
   - ETL Pipelines: Advanced (5+ years)
   - Big Data (Hadoop, Spark): Intermediate (3+ years)
   - Time-series Databases: Intermediate (2+ years)
   ## Cloud & DevOps
   - AWS (EC2, S3, Lambda, etc.): Expert (7+ years)
   - Docker: Expert (6+ years)
   - Kubernetes: Advanced (4+ years)
   - Terraform/CloudFormation: Advanced (5+ years)
   - CI/CD (Jenkins, GitHub Actions): Expert (6+ years)
   - Monitoring & Observability: Advanced (5+ years)
   - Infrastructure as Code: Expert (5+ years)
   - Site Reliability Engineering: Advanced (4+ years)
   ## Machine Learning & AI
   - TensorFlow/PyTorch: Intermediate (3+ years)
   - scikit-learn: Advanced (4+ years)
   - NLP: Intermediate (2+ years)
   - Recommendation Systems: Advanced (3+ years)
   - Fraud Detection: Expert (4+ years)
   - Data Visualization: Advanced (5+ years)
   - Statistical Analysis: Advanced (4+ years)
   - Feature Engineering: Advanced (4+ years)
   CONTACT INFORMATION:
   1234 Tech Avenue
   San Francisco, CA 94107
   415.555.7890
   alex.chen1984@email.example.com
   LinkedIn: linkedin.com/in/alexchen
   GitHub: github.com/alexchen
   Twitter: @alexchen_tech
   I can start immediately and am willing to relocate for the right opportunity. I prefer hybrid work models with 2-3 days in office per week. I'm authorized to work in the United States without sponsorship.
   </cv>
   <jd>
   <${jd}>
   </jd>
</input4>
<output_json4>
   {
   "status": "success",
   "errors": null,
   "data": {
      "company": "Fintech Startup, Inc.",
      "start": "2019",
      "end": null,
      "current": true,
      "summary": "Led payment processing infrastructure handling millions of daily transactions and managed a team of 5 engineers implementing microservices architecture. Developed responsive web interfaces using React and Redux, built RESTful APIs with Node.js and Express, and implemented automated testing strategies.",
      "highlights": [
         "Implemented real-time fraud detection using machine learning models, saving approximately $2.4M annually",
         "Led migration from monolithic architecture to microservices, reducing system downtime by 78%",
         "Redesigned authentication system reducing unauthorized access attempts by 95%",
         "Established CI/CD pipeline improving deployment frequency from biweekly to daily",
         "Mentored junior engineers through weekly code reviews and pair programming sessions",
         "Implemented automated testing strategies achieving 85% code coverage"
      ],
      "roles": [
         {
         "title": "Senior Software Engineer / Tech Lead",
         "start": "2020",
         "end": null,
         "current": true
         },
         {
         "title": "Full Stack Engineer",
         "start": "2019",
         "end": "2020",
         "current": false
         }
      ],
      "feedback": {
         "strengths": [
         "Strong quantifiable achievements with clear metrics (95% reduction, $2.4M savings, 78% downtime reduction)",
         "Demonstrates leadership experience through team management and mentoring junior engineers",
         "Showcases technical expertise across full stack development, microservices architecture, and security",
         "Highlights experience with modern development practices (CI/CD, automated testing)",
         "Shows clear career progression from Full Stack Engineer to Senior/Tech Lead role"
         ],
         "areas_to_improve": [
         "Specify technologies used in the payment processing infrastructure for better keyword matching",
         "Include more details about the scale of operations (transaction volume, user base, etc.)",
         "Add specifics about fintech domain knowledge and industry-specific challenges overcome",
         "Elaborate on the technical implementation of the fraud detection system (algorithms, data sources)",
         "Mention cross-functional collaboration with product/business teams to show broader business impact"
         ]
      }
   }
   }
</output_json4>
</example4>
</few_shot_examples>