<few_shot_examples>
<example1>
<assessment1>
    # Strengths
    - Perfect adherence to the response schema structure
    - The optimized profile statement successfully implements 4 out of 5 identified areas for improvement
    - Added impressive quantifiable achievements (78% system downtime reduction, $2.4M savings)
    - Incorporated specific programming languages and the AWS certification
    - Specified system scale (processing millions of daily transactions)
    - Well within the 750 character limit while being comprehensive
    - Maintains professional tone with appropriate tense usage
    # Areas to Improve
    - The optimized statement omits the candidate's prestigious educational background (Stanford MS, Berkeley BS) despite this being correctly identified as an area to improve and information being available in the CV
    # Notes
    The response demonstrates excellent implementation of the feedback. The optimized profile statement successfully addresses most weaknesses in the original statement by incorporating specific metrics, technical skills, certifications, and system scale information from the CV. The only missed opportunity was including the candidate's impressive educational credentials.
    # Score (out of 100)
    95/100 - Nearly perfect implementation of improvements with just one significant omission.
</assessment1>
<input1>
    <task>
    You must optimize the profile statement section of a CV/résumé document provided in `<section></section>` of this prompt, with reference to the job description in the `jd` section if one is provided. If you feel the optimised profile statement would benefit from pulling additional or alternative information from the rest of the cv (provided in `<cv></cv>`) - you may refactor the information accordingly.
    <section>
    Versatile software engineer with 10+ years of experience spanning startups and large enterprises across fintech, e-commerce, and social media sectors. Expert in building scalable, resilient systems with a focus on microservices architecture, cloud solutions, and performance optimization. Proven track record of technical leadership, improving system performance, mentoring junior engineers, and delivering complex projects on time. Seeking opportunities to leverage technical expertise in high-growth environments.
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
</input1>
<output_json1>
    {
    "status": "success",
    "errors": null,
    "data": {
        "profileStatement": "Technical leader and software engineer with 10+ years of experience across fintech, e-commerce, and social media sectors. Expert in building scalable microservices architectures, cloud solutions (AWS Certified Solutions Architect), and performance optimization that has reduced system downtime by 78% and saved $2.4M annually through fraud detection implementations. Proven track record of mentoring 15+ engineers while developing mission-critical systems processing millions of daily transactions. Skilled in Python, JavaScript, Go, and Java with deep expertise in distributed systems, RESTful APIs, and GraphQL. Seeking technical leadership opportunities in high-growth environments.",
        "feedback": {
        "strengths": [
            "Successfully communicates extensive experience across diverse sectors (fintech, e-commerce, social media)",
            "Effectively highlights expertise in high-demand technical areas (microservices, cloud, performance optimization)",
            "Balances technical abilities with leadership experience (mentoring, project delivery)",
            "Maintains concise length and professional tone",
            "Includes a clear career objective aligned with the candidate's expertise"
                ],
        "areas_to_improve": [
            "Add specific quantifiable achievements to demonstrate impact (e.g., percentage improvements, financial outcomes)",
            "Include specific in-demand programming languages and technologies from the CV (Python, JavaScript, Go, etc.)",
            "Incorporate prestigious educational background (Stanford MS, Berkeley BS) as a differentiator",
            "Mention relevant certifications, particularly AWS Certified Solutions Architect",
            "Specify the scale of systems worked on (e.g., processing millions of transactions daily)"
                ]
            }
        }
    }
</output_json1>
</example1>
<example2>
<assessment2>
    # Strengths
    - Perfect adherence to schema structure and character limitations
    - All identified areas for improvement have been fully implemented in the optimized statement
    - Successfully incorporated key certifications (CCM, PMP, LEED) from the CV
    - Added specific project types (healthcare, educational, mixed-use) showing versatility
    - Included language skills (Spanish fluency) as a valuable differentiator
    - Mentioned technical proficiency with industry software (PlanGrid, Procore)
    - Retained the powerful metrics from the original statement (17% delay reduction, 25% safety improvement)
    - Improved overall flow and professional tone
    # Notes
    The response demonstrates excellent optimization. The profile statement effectively implements all suggested improvements while maintaining the strongest elements of the original statement. All additions are properly sourced from the CV without fabrication, creating a comprehensive and powerful professional summary.
    # Score (out of 100)
    100/100 - Perfect implementation of all suggested improvements while maintaining character limits and professional tone.
</assessment2>
<input2>
    <task>
    You must optimize the profile statement section of a CV/résumé document provided in `<section></section>` of this prompt, with reference to the job description in the `jd` section if one is provided. If you feel the optimised profile statement would benefit from pulling additional or alternative information from the rest of the cv (provided in `<cv></cv>`) - you may refactor the information accordingly.
    <section>
    Experienced Construction Manager with over 15 years of progressive responsibility in commercial and residential project management. Specialized expertise in managing large-scale commercial projects with budgets exceeding $15 million and teams of up to 50 workers. Proven track record of completing projects ahead of schedule and under budget, with a focus on safety and quality control. Skilled at implementing efficiency-improving processes, reducing project delays by 17% and workplace incidents by 25%.
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
</input2>
<output_json2>
    {
    "status": "success",
    "errors": null,
    "data": {
        "profileStatement": "Certified Construction Manager (CCM, PMP, LEED) with over 15 years of progressive experience in commercial and residential projects valued up to $18 million. Expert in managing diverse teams of 50+ workers across healthcare, educational, and mixed-use developments, consistently delivering projects ahead of schedule and under budget. Proven record of implementing efficiency-improving processes, reducing project delays by 17% and workplace incidents by 25%. Proficient with industry software including PlanGrid and Procore, with Spanish fluency that enhances communication with all stakeholders.",
        "feedback": {
        "strengths": [
            "Effectively quantifies experience (15+ years), project budgets ($15 million), and team management scope (50 workers)",
            "Includes specific, measurable achievements (17% reduction in delays, 25% reduction in workplace incidents)",
            "Clearly identifies the candidate's role and areas of expertise in construction management",
            "Demonstrates both technical project management capabilities and focus on safety/quality control",
            "Presents information in a concise, well-structured format with good flow"
        ],
        "areas_to_improve": [
            "Include relevant professional certifications (PMP, CCM, LEED) to strengthen credibility and demonstrate continued professional development",
            "Reference specific project types (medical centers, educational facilities) to showcase versatility and domain expertise",
            "Highlight language skills (Spanish fluency) which add significant value in construction management roles",
            "Incorporate mention of technical proficiency with industry-specific software (PlanGrid, Procore)",
            "Emphasize communication skills that enhance stakeholder management and project coordination"
        ]
        }
    }
    }
</output_json2>
</example2>
<example3>
<assessment3>
    # Strengths
    - Excellent implementation of all five suggested areas for improvement
    - Successfully added multiple specific metrics (37% improvement in banking, 17-minute engagement vs. 5-minute industry standard, 1.2M+ views, 3,000+ community members)
    - Incorporated specific technical tools (D3.js, Python data stack)
    - Clearly articulated value proposition combining academic rigor with industry expertise
    - Highlighted leadership in community building (DataViz Collective)
    - Maintained professional tone with strong keyword optimization
    - Well within character limits while being comprehensive
    # Notes
    The response demonstrates perfect optimization of the original profile statement. Every suggested area for improvement has been implemented using accurate information from the CV. The statement effectively communicates Dr. Taylor-Williams' unique value proposition by balancing academic credentials with industry impact and technical expertise. The incorporation of specific metrics significantly strengthens the statement's impact.
    # Score (out of 100)
    100/100 - Perfect implementation of all feedback points while maintaining character limits and professional tone.
</assessment3>
<input3>
    <task>
    You must optimize the profile statement section of a CV/résumé document provided in `<section></section>` of this prompt, with reference to the job description in the `jd` section if one is provided. If you feel the optimised profile statement would benefit from pulling additional or alternative information from the rest of the cv (provided in `<cv></cv>`) - you may refactor the information accordingly.
    <section>
    Data visualization expert with PhD in Human-Computer Interaction, combining academic research with industry practice across Fortune 500 clients. Specialist in transforming complex data into intuitive visual experiences through evidence-based design. Versatile career spanning freelance consultancy, higher education teaching, and leadership roles in banking and tech sectors. Award-winning creator of data visualization systems with international recognition, featured speaker, and published author with extensive technical expertise in UX/UI design and data science.
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
</input3>
<output_json3>
    {
    "status": "success",
    "errors": null,
    "data": {
        "profileStatement": "Award-winning Data Visualisation Expert with PhD in Human-Computer Interaction and 12+ years' experience transforming complex data into intuitive visual experiences for Fortune 500 clients. Combines academic rigour with industry expertise as lecturer, researcher, and consultant across financial services, tech, and public sectors. Creator of internationally recognised visualisation systems featured in WIRED and exhibited at Science Museum London and COP26. Technical authority in D3.js, Python data stack, and UX/UI design with proven impact on user engagement (17-minute average versus 5-minute industry standard). TED speaker (1.2M+ views) leading a global community of 3,000+ data visualisation specialists.",
        "feedback": {
        "strengths": [
            "Effectively establishes academic credentials and expert status in data visualisation",
            "Showcases breadth of experience across both academic and industry settings",
            "Mentions recognition in the field through speaking engagements and media features",
            "Includes reference to technical expertise in UX/UI design and data science",
            "Demonstrates versatility across multiple sectors including banking and tech"
        ],
        "areas_to_improve": [
            "Add specific metrics demonstrating business impact (e.g., 37% improvement in customer satisfaction from banking interface revamp)",
            "Incorporate more specific technical tools where expertise lies (D3.js, React, Tableau)",
            "Articulate a clearer value proposition focusing on evidence-based design approach",
            "Highlight leadership capabilities demonstrated through DataViz Collective community building",
            "Include more quantifiable achievements such as publication citation counts or patent applications"
        ]
        }
    }
    }
</output_json3>
</example3>
<example4>
<assessment4>
    # Strengths
    - Excellent implementation of four out of five suggested improvements
    - Added multiple impressive quantifiable achievements (£2 billion in transactions, 99.99% uptime, 40% improved reliability, 45% fraud reduction)
    - Successfully emphasized current role as Senior Software Architect and specialized expertise
    - Incorporated critical keywords for ATS optimization (microservices, cloud-native, AWS/Azure)
    - Added industry-specific expertise particularly relevant to fintech and regulated environments
    - Maintained all original strengths while significantly enhancing impact through specificity
    - Well structured with logical flow from identity to technical expertise to business value
    # Areas to Improve
    - Did not explicitly mention certifications (AWS Certified Solutions Architect, Azure Solutions Architect Expert) that would strengthen credibility
    # Notes
    The optimized statement effectively transforms a general technology leadership profile into a powerful, specific value proposition backed by impressive metrics. The addition of quantifiable achievements and technical specificity significantly increases impact while maintaining the character limit. The only minor missed opportunity was explicitly mentioning certifications.
    # Score (out of 100)
    95/100 - Excellent implementation of feedback with only one minor omission.
</assessment4>
<input4>
    <task>
    You must optimize the profile statement section of a CV/résumé document provided in `<section></section>` of this prompt, with reference to the job description in the `jd` section if one is provided. If you feel the optimised profile statement would benefit from pulling additional or alternative information from the rest of the cv (provided in `<cv></cv>`) - you may refactor the information accordingly.
    <section>
    Dedicated Technology Leader with 15+ years in software development, digital transformation, and team leadership. Successfully guided cross-functional teams to deliver innovative solutions across financial services, healthcare, and e-commerce sectors. Expertise spans full-stack development, cloud migration, and implementing agile methodologies that enhance operational efficiency. Exceptional capability in translating complex technical concepts into actionable strategies aligned with business objectives. Passionate about mentoring junior developers and establishing robust processes that foster innovation while maintaining quality and security compliance.
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
    # JENNIFER MARIE RODRIGUEZ-THOMPSON
    jenniferrt@emailprovider.co | Mobile: +44 7700 900129 | London, UK SW1A 1AA
    ## PROFESSIONAL PROFILE
    Dedicated and results-driven Technology Leader with a robust track record spanning more than 15 years in software development, digital transformation, and team leadership. I have successfully guided cross-functional teams in delivering innovative solutions across financial services, healthcare, and e-commerce sectors. My expertise spans full-stack development, cloud migration, and implementing agile methodologies that significantly enhance operational efficiency and drive business growth. I am seeking a challenging leadership role within a forward-thinking organization where my technical acumen and strategic vision can contribute to transformative digital initiatives and sustainable business success. I am extremely passionate about mentoring junior developers and establishing robust processes that foster innovation while maintaining code quality and security compliance.
    In my previous roles I've demonstrated exceptional capability in translating complex technical concepts into actionable strategies that align perfectly with organizational objectives. Known for my meticulous attention to detail and ability to work effectively under pressure, I consistently deliver high-quality results while managing multiple priorities simultaneously. My approach combines strategic thinking with hands-on problem-solving, enabling me to identify opportunities for improvement and implement effective solutions that drive significant business value.
    ## TECH ARSENAL
    * Java / Spring Boot / Hibernate
    * Python (Intermediate)
    * React.js & Vue.js
    * Node.js / Express
    * GraphQL & REST API Design
    * Microservices Architecture
    * AWS Cloud Services (EC2, S3, Lambda, CloudFormation)
    * Docker, Kubernetes
    * CI/CD (Jenkins, GitLab CI)
    * Agile Methodologies (Scrum/Kanban)
    * SQL databases (PostgreSQL, MySQL)
    * NoSQL databases (MongoDB, DynamoDB)
    * System design & architecture
    * TDD & BDD practices
    * Performance optimization
    * Security best practices
    * Technical documentation
    ## PROFESSIONAL JOURNEY
    ### FINTECH INNOVATIONS LTD, London, UK
    #### Senior Software Architect | April 2019 - Present
    Leading architecture and development of a cloud-native payment processing platform handling over £2 billion in annual transactions. Spearheaded the transition from monolithic architecture to microservices, resulting in 40% improved system reliability and 30% faster deployment cycles.
    Key Contributions:
    * Designed and implemented a scalable microservices architecture using Spring Boot, Docker, and Kubernetes that supports peak transaction volumes exceeding 10,000 TPS
    * Led migration of legacy systems to AWS cloud infrastructure, achieving 99.99% uptime and reducing operational costs by 25%
    * Established coding standards, review processes, and CI/CD pipelines that decreased production defects by 35%
    * Pioneered adoption of event-driven architecture using Kafka for real-time data processing, improving transaction monitoring capabilities
    * Mentored team of 12 developers across 3 geographic locations, facilitating knowledge sharing sessions and technical workshops
    * Collaborated with product management to define technical roadmap and prioritize feature development based on business impact
    * Implemented comprehensive security measures including OAuth 2.0, API gateway protection, and encryption strategies that ensured PCI-DSS compliance
    * Enhanced system observability by integrating ELK stack and Prometheus, reducing mean time to resolution for production issues by 50%
    * Technical lead for integration with 5 major payment networks, expanding service capabilities and market reach
    ACHIEVEMENTS: Recognized with company's "Innovation Excellence Award" for development of ML-based fraud detection system that reduced fraudulent transactions by 45% while maintaining false positive rate below 0.1%.
    #### Lead Backend Engineer | April 2019 - March 2021
    Initially joined as Lead Backend Engineer and was promoted to Senior Software Architect after demonstrating exceptional technical leadership and innovative problem-solving abilities.
    * Developed core payment processing APIs using Java Spring Boot that processed over 5 million transactions monthly
    * Designed and implemented database schemas and optimization strategies that improved query performance by 60%
    * Established automated testing frameworks achieving 90%+ code coverage for critical payment flows
    * Collaborated with frontend teams to design effective APIs and data models
    * Implemented robust error handling and monitoring solutions that improved system resilience
    * Led weekly code reviews and knowledge sharing sessions to improve team capabilities
    ### HEALTH SYSTEMS SOLUTIONS, Manchester, UK
    #### Technical Lead | June 2016 - March 2019
    Directed development of patient management systems used by 15+ NHS trusts. Successfully delivered major system upgrade while ensuring zero downtime for critical healthcare operations.
    * Led team of 8 developers in building and maintaining Java/Spring healthcare data management applications
    * Architected and implemented integration solutions with legacy healthcare systems using HL7 standards
    * Designed RESTful API layer that enabled secure interoperability between disparate healthcare systems
    * Implemented role-based access control system ensuring GDPR compliance for sensitive patient data
    * Coordinated with QA team to establish comprehensive test automation strategy using Selenium and JUnit
    * Reduced system incidents by 40% through implementation of proactive monitoring and alerting mechanisms
    * Facilitated transition to agile development practices, increasing sprint velocity by 25% over 6 months
    * Collaborated with product owners to translate complex healthcare workflows into technical requirements
    * Regular presentations to stakeholders including hospital administrators and clinical staff
    Key project: Patient Data Exchange Platform
    * Led design and implementation of a scalable data exchange platform allowing secure sharing of patient information between different healthcare providers
    * Implemented encryption and anonymization techniques to protect sensitive data in compliance with GDPR and NHS Digital standards
    * Solution reduced administrative overhead by an estimated 15,000 person-hours annually across participating trusts
    ### DIGITAL RETAIL SOLUTIONS, London, UK
    #### Senior Developer | September 2013 - May 2016
    Part of core development team for high-traffic e-commerce platform supporting 50+ retail brands. Implemented performance optimizations that reduced page load times by 40% and improved conversion rates by 15%.
    * Developed and maintained backend services using Java, Spring, and Hibernate for e-commerce platform handling peak loads of 10,000 concurrent users
    * Created responsive frontend components using React.js and Redux that improved mobile conversion rates by 20%
    * Implemented product recommendation engine using collaborative filtering techniques that increased average order value by 12%
    * Designed and developed inventory management system integrating with multiple warehouse management solutions
    * Contributed to CI/CD pipeline automation reducing deployment time from days to hours
    * Optimized MySQL database queries and implemented caching strategies that significantly improved system performance
    * Developed RESTful APIs consumed by mobile applications and third-party integrations
    * Participated in 24/7 support rotation, demonstrating strong troubleshooting skills in production environments
    * Mentored junior developers on best practices for code quality and performance optimization
    ### GLOBAL BANKING CORPORATION, Various Locations
    #### Software Developer | July 2010 - August 2013 (London, UK)
    #### Junior Developer | February 2008 - June 2010 (Edinburgh, UK)
    Progressed from Junior Developer to Software Developer through consistent delivery of high-quality solutions and demonstrating strong technical capabilities.
    As Software Developer (London):
    * Developed Java applications for trade processing systems handling $1.5B daily transaction volume
    * Implemented real-time market data integration services improving trading decision accuracy
    * Contributed to design and development of regulatory reporting system ensuring compliance with post-2008 financial regulations
    * Optimized batch processing jobs reducing nightly processing time by 35%
    * Collaborated with business analysts and traders to implement new financial products on trading platform
    As Junior Developer (Edinburgh):
    * Maintained and enhanced legacy banking applications written in Java and C++
    * Developed automated test suites improving code coverage from 65% to 85%
    * Assisted in data migration projects during system upgrades
    * Created internal tools that streamlined development workflows
    * Participated in code reviews and contributed to technical documentation
    ## ACADEMIC FOUNDATION
    ### University of Cambridge
    #### Master of Science, Computer Science | 2006 - 2007
    * Specialization: Distributed Systems and Security
    * Dissertation: "Scalable Approaches to Secure Distributed Computing in Financial Applications"
    * Grade: Distinction
    ### University of Manchester
    #### Bachelor of Science (Honours), Computer Science with Mathematics | 2003 - 2006
    * First Class Honours
    * Dissertation: "Algorithmic Optimization for High-Frequency Trading Systems"
    * Relevant coursework: Data Structures & Algorithms, Software Engineering, Database Systems, Computer Networks, Artificial Intelligence, Cryptography
    ## SPECIALIZED TRAINING AND CERTIFICATIONS
    * AWS Certified Solutions Architect - Professional (2022)
    * Google Cloud Professional Cloud Architect (2021)
    * Certified Kubernetes Administrator (CKA) (2020)
    * Certified Scrum Master (CSM) (2018)
    * Oracle Certified Professional, Java SE 11 Developer (2020)
    * ITIL Foundation Certificate in IT Service Management (2015)
    * Microsoft Certified: Azure Solutions Architect Expert (2023)
    ## TECHNICAL SKILLS MATRIX
    PROGRAMMING LANGUAGES
    * Java - Expert (10+ years)
    * Python - Advanced (6 years)
    * JavaScript/TypeScript - Advanced (8 years)
    * SQL - Expert (10+ years)
    * Go - Intermediate (3 years)
    * C# - Basic (1 year)
    WEB TECHNOLOGIES
    * React.js - Advanced (5 years)
    * Angular - Intermediate (3 years)
    * Node.js - Advanced (6 years)
    * HTML5/CSS3 - Advanced (8 years)
    * GraphQL - Advanced (4 years)
    * REST API Design - Expert (7 years)
    CLOUD & DEVOPS
    * AWS - Expert (7 years)
    * Docker - Expert (6 years)
    * Kubernetes - Advanced (4 years)
    * CI/CD (Jenkins, GitHub Actions) - Expert (7 years)
    * Infrastructure as Code (Terraform) - Advanced (5 years)
    * Monitoring & Observability (ELK, Prometheus) - Advanced (5 years)
    DATABASES
    * PostgreSQL - Expert (8 years)
    * MongoDB - Advanced (6 years)
    * MySQL - Advanced (7 years)
    * Redis - Advanced (5 years)
    * DynamoDB - Intermediate (3 years)
    * Cassandra - Basic (2 years)
    METHODOLOGIES & PRACTICES
    * Agile (Scrum, Kanban) - Expert (9 years)
    * TDD/BDD - Advanced (7 years)
    * Domain-Driven Design - Advanced (5 years)
    * Microservices Architecture - Expert (6 years)
    * Event-Driven Architecture - Advanced (4 years)
    * System Design & Scalability - Expert (8 years)
    ## LANGUAGES
    English - Native Proficiency
    Spanish - Fluent (C1)
    French - Intermediate (B1)
    German - Basic (A2)
    I lived in Madrid for three months during a university exchange program which significantly improved my Spanish language skills. I regularly use French in business contexts when working with our Paris office, and I'm currently taking evening classes to improve my German proficiency because our company is expanding into the German market.
    ## PROFESSIONAL AFFILIATIONS
    * Member, British Computer Society (BCS)
    * IEEE Computer Society
    * Association for Computing Machinery (ACM)
    * Agile Alliance
    * Women in Tech London (Committee Member)
    * FinTech Innovation Network (Regular Speaker)
    ## PUBLICATIONS AND PRESENTATIONS
    * "Implementing Secure Microservices in Regulated Financial Environments" - FinTech Summit London, 2022
    * "Scalable Event-Driven Architectures: Lessons from High-Volume Payment Processing" - published in Journal of Software Practice and Experience, 2021
    * "Transitioning from Monoliths to Microservices: A Case Study" - DevOps Conference Berlin, 2020
    * "Optimizing CI/CD Pipelines for Enterprise-Scale Applications" - Jenkins World, 2019
    * "Practical Approaches to GDPR Compliance in Healthcare Systems" - HealthTech Innovation Conference, 2018
    * Co-author, "Cloud-Native Transformation Strategies" - Technical whitepaper, 2021
    ## ACHIEVEMENTS & NOTABLE PROJECTS
    * Led architecture team that won "Most Innovative Financial Solution" at European FinTech Awards 2022 for real-time cross-border payment system
    * Reduced infrastructure costs by 35% while improving performance through cloud optimization initiatives
    * Designed authentication system securing access for 3 million+ users with zero security breaches over 3 years
    * Patentholder for innovative approach to distributed transaction processing (Patent #GB2576412)
    * Created open-source library for financial data visualization with 5,000+ GitHub stars
    * Mentored 15+ junior developers who progressed to senior roles throughout the industry
    ## Earlier Career Highlights
    Before joining Global Banking Corporation, I worked briefly at several organizations where I developed foundational skills:
    Quick Software Solutions (2007-2008)
    Graduate Developer
    Developed small business applications using Java and SQL
    Created internal tools for project management
    Tech Internships:
    Summer Intern at Microsoft Research (2005)
    Assisted research team on distributed computing projects
    Implemented experimental algorithms in C++ and Java
    Summer Intern at IBM (2004)
    Contributed to QA testing automation
    Created documentation for internal frameworks
    ## COMMUNITY ENGAGEMENT
    * Volunteer instructor, Code First Girls (2018-Present): Teaching coding fundamentals to women entering tech
    * STEM Ambassador: Regular speaker at local schools promoting technology careers
    * Mentor, Women in FinTech Program (2020-Present): Providing career guidance and technical mentorship
    * Organize quarterly "Tech for Good" hackathons addressing social challenges
    * Open Source Contributor: Active contributions to several Java and Spring framework projects
    ## PERSONAL PROJECTS
    * Developed "FinTrack" - Personal finance management application with 10,000+ users
    * Created "DevUtils" - Chrome extension for developers with 5,000+ installations
    * Maintain technical blog (techinsights.jenniferrt.com) with monthly articles on software architecture
    * Weekend project: Raspberry Pi-based home automation system controlling lighting, heating and security
    ## ADDITIONAL INFORMATION
    * Availability: 3-month notice period required for current position
    * Willing to travel up to 20% for business requirements
    * Full clean UK driving license
    * Eligible to work in UK and EU (dual citizenship)
    References available upon request.
    I've successfully balanced delivering complex technical projects while maintaining focus on business objectives throughout my career. I'm particularly adept at translating between technical and non-technical stakeholders, ensuring alignment across organizational levels. Outside of work, I'm an avid runner having completed the London Marathon twice, and I enjoy landscape photography during my travels. I believe that continuous learning is essential in technology, and I dedicate at least 5 hours weekly to exploring new technologies and approaches.
    RECENT PROJECTS
    At Fintech Innovations, I've led several transformative initiatives:
    * Payment Gateway Modernization: Architected complete rebuild of legacy payment gateway using microservices architecture, improving transaction processing speed by 60% and enabling support for 15 additional payment methods
    * Fraud Detection Engine: Led development of machine learning-based fraud detection system that reduced fraudulent transactions by 45% while keeping false positives under 0.1%
    * Regulatory Compliance Framework: Designed flexible compliance framework ensuring adherence to PSD2, GDPR and other regulatory requirements across multiple jurisdictions
    * Cloud Migration: Orchestrated migration of core payment systems to AWS, implementing infrastructure-as-code practices that improved deployment consistency and reduced provisioning time from days to hours
    * Development Process Transformation: Implemented trunk-based development and continuous deployment practices that reduced time-to-market for new features by 60%
    Contact me at jenniferrt@emailprovider.co or +44 7700 900129 to discuss how my technical leadership and strategic vision can benefit your organization.
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
        "profileStatement": "Senior Software Architect and Technology Leader with 15+ years of experience driving digital transformation across financial services, healthcare, and e-commerce sectors. Designs and implements scalable cloud-native architectures that process over £2 billion in annual transactions, achieving 99.99% uptime and 40% improved system reliability. Expert in microservices architecture, AWS/Azure cloud infrastructure, and agile methodologies, with recognized innovation in ML-based fraud detection systems reducing fraudulent transactions by 45%. Translates complex technical concepts into business-aligned strategies while mentoring technical teams and establishing robust processes that maintain security compliance in regulated environments.",
        "feedback": {
        "strengths": [
            "Clearly establishes professional identity and extensive experience (15+ years)",
            "Effectively communicates breadth of industry experience across multiple sectors",
            "Demonstrates valuable technical expertise in relevant areas",
            "Shows important leadership qualities through mentoring and process establishment",
            "Concisely presents core value proposition as a technology leader"
        ],
        "areas_to_improve": [
            "Include specific quantifiable achievements to demonstrate impact (e.g., transaction volumes, uptime percentages)",
            "Highlight relevant certifications to strengthen credibility (AWS, Azure)",
            "Emphasize current role and specialized expertise in software architecture more prominently",
            "Add relevant keywords for ATS optimization (e.g., microservices, cloud-native)",
            "Incorporate more industry-specific expertise to better target roles in fintech/financial services"
        ]
        }
    }
    }
</output_json4>
</example4>
</few_shot_examples>