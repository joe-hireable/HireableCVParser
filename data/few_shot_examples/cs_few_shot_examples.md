<few_shot_examples>
<example1>
<input1>
  <task>
  You must optimize the core skills section of a CV/résumé provided in the `cv` section of this prompt, with reference to the job description in the `jd` section. 
  <section>
  <${section}>
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
    - Average: Regular usage with fundamental understanding
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
  5. Include only the most relevant skills, maximum of 14 distinct skills
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
      "skills": [
        {
          "name": "Python",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "JavaScript",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "React",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "AWS",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "Microservices Architecture",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "SQL",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "Docker",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "CI/CD",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "RESTful API Design",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "Machine Learning",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "Java",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "NoSQL",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "Technical Leadership",
          "proficiency": "Advanced",
          "skillType": "soft"
        },
        {
          "name": "Mentoring",
          "proficiency": "Advanced",
          "skillType": "soft"
        }
      ],
      "feedback": {
        "strengths": [
          "Comprehensive technical skills across the full stack development spectrum",
          "Clear indication of proficiency levels supported by years of experience",
          "Strong expertise in modern technologies like microservices and containerization",
          "Balanced mix of programming languages, frameworks, and cloud technologies",
          "Technical leadership skills backed by concrete mentoring experience"
        ],
        "areas_to_improve": [
          "Consider consolidating similar skills (e.g., JavaScript and TypeScript) to avoid redundancy",
          "Highlight skills that demonstrate measurable business impact more prominently",
          "Add more contextual examples of how soft skills were applied in specific projects",
          "Reduce the comprehensive list to focus on the most relevant skills for target roles",
          "Consider organizing skills by relevance to job functions rather than by technical category"
        ]
      }
    }
  }
</output_json1>
</example1>
<example2>
<input2>
  <task>
  You must optimize the core skills section of a CV/résumé provided in the `cv` section of this prompt, with reference to the job description in the `jd` section. 
  <section>
  [
                  {
                      "name": "Python",
                      "proficiency": "Expert",
                      "skillType": "hard"
                  },
                  {
                      "name": "JavaScript/TypeScript",
                      "proficiency": "Expert",
                      "skillType": "hard"
                  },
                  {
                      "name": "React",
                      "proficiency": "Expert",
                      "skillType": "hard"
                  },
                  {
                      "name": "AWS",
                      "proficiency": "Expert",
                      "skillType": "hard"
                  },
                  {
                      "name": "CI/CD",
                      "proficiency": "Expert",
                      "skillType": "hard"
                  },
                  {
                      "name": "Microservices",
                      "proficiency": "Expert",
                      "skillType": "hard"
                  },
                  {
                      "name": "Go",
                      "proficiency": "Advanced",
                      "skillType": "hard"
                  },
                  {
                      "name": "Java",
                      "proficiency": "Advanced",
                      "skillType": "hard"
                  },
                  {
                      "name": "Docker/Kubernetes",
                      "proficiency": "Advanced",
                      "skillType": "hard"
                  },
                  {
                      "name": "Database Optimization",
                      "proficiency": "Advanced",
                      "skillType": "hard"
                  },
                  {
                      "name": "GraphQL",
                      "proficiency": "Advanced",
                      "skillType": "hard"
                  },
                  {
                      "name": "System Design",
                      "proficiency": "Advanced",
                      "skillType": "hard"
                  },
                  {
                      "name": "Machine Learning",
                      "proficiency": "Intermediate",
                      "skillType": "hard"
                  },
                  {
                      "name": "Leadership",
                      "proficiency": "Advanced",
                      "skillType": "soft"
                  }
                  ]
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
    - Average: Regular usage with fundamental understanding
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
  5. Include only the most relevant skills, maximum of 14 distinct skills
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
</input2>
<output_json2>
  {
    "status": "success",
    "errors": null,
    "data": {
      "skills": [
        {
          "name": "Python",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "JavaScript/TypeScript",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "React",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "AWS",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "CI/CD",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "Microservices Architecture",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "Go",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "Java",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "Docker",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "Kubernetes",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "SQL Databases",
          "proficiency": "Expert",
          "skillType": "hard"
        },
        {
          "name": "GraphQL",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "System Design",
          "proficiency": "Advanced",
          "skillType": "hard"
        },
        {
          "name": "Leadership",
          "proficiency": "Advanced",
          "skillType": "soft"
        }
      ],
      "feedback": {
        "strengths": [
          "The skills section effectively highlights the candidate's full-stack expertise across frontend, backend, and infrastructure domains.",
          "Proficiency levels accurately reflect the years of experience detailed in the CV (e.g., Python: 9+ years, React: 7+ years).",
          "The balance of programming languages, frameworks, and architectural skills demonstrates comprehensive technical knowledge.",
          "The separation of Docker (Expert) and Kubernetes (Advanced) provides more precise skill proficiency representation.",
          "The inclusion of leadership as a soft skill reflects the management experience described in the work history."
        ],
        "areas_to_improve": [
          "Consider adding Node.js/Express as an expert-level skill (6+ years experience) to better highlight backend capabilities.",
          "Include specific database technologies (PostgreSQL, MongoDB) rather than the generic SQL Databases category.",
          "Add a data engineering skill like ETL Pipelines or Data Visualization given the significant experience mentioned.",
          "Consider including an additional soft skill such as mentorship or cross-functional collaboration evident in the work history.",
          "Machine Learning could be replaced with a more specific ML skill like Fraud Detection (listed as Expert level in the CV)."
        ]
      }
    }
  }
</output_json2>
</example2>
</few_shot_examples>