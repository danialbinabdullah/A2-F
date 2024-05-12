## News Data Extraction and Processing

### Data Extraction:

**Data extraction** was a crucial step in gathering news articles from Dawn.com and BBC.com. BeautifulSoup, a Python library for web scraping, was employed to parse the HTML structure of the websites and extract relevant information such as article titles, descriptions, and links.

### Extracting Data from Dawn.com and BBC.com:

For **Dawn.com**, the script accessed the landing page and extracted article data using BeautifulSoup. Similarly, for **BBC.com**, the script navigated through the RSS feed to gather article details. This process involved analyzing the website's structure to locate and extract the desired information accurately.

### Handling Dynamic Content:

Both **Dawn.com** and **BBC.com** frequently update their content, presenting challenges in extracting data consistently. To address this, the script dynamically fetched the latest articles each time it ran, ensuring the dataset remained up-to-date.

### Data Transformation:

After extracting raw data from the websites, it underwent a series of transformations to prepare it for analysis. This included cleaning, formatting, and structuring the data to enhance its usability.

### Preprocessing Text Data:

Text preprocessing involved removing HTML tags, non-alphabetic characters, and converting text to lowercase. Regular expressions were utilized to perform pattern-based substitutions, resulting in clean and standardized text data.

### Formatting Data for Analysis:

Once cleaned, the data was formatted into a structured format in **cleaned.csv** suitable for analysis. This involved organizing the data into rows and columns, with each row representing an individual article and each column representing specific attributes such as ID, title, and source.

### Data Storage and Version Control

**Storing Data on Google Drive**:

Google Drive provided a convenient and reliable storage solution for the processed data. The script saved the cleaned article data into CSV files, which were then uploaded to Google Drive using the Google Drive API.

**Integrating DVC for Version Control**:

Data Version Control (DVC) was integrated into the workflow to track changes to the dataset over time. DVC maintained a versioned copy of the data on Google Drive, enabling easy rollback to previous versions if needed.

**Versioning with Git**:

In addition to DVC, Git was utilized for version control of the entire project repository. Each commit to the repository was accompanied by a descriptive message detailing the changes made, providing a comprehensive history of project development.

**Link to Google Drive**:

The processed data stored on Google Drive was accessible via the provided drive link: [Google Drive Link.](https://drive.google.com/drive/folders/1rUYRBwHNi4PrTZCOjtW_Pm6KeKYZl0Ke)

### Apache Airflow DAG Development

**Implementing the DAG**:

Apache Airflow was employed to orchestrate the workflow, automating the extraction, transformation, and storage processes. The Airflow DAG (Directed Acyclic Graph) defined the sequence of tasks and their dependencies, ensuring smooth execution of the workflow.

**Task Dependencies**:

Each task in the DAG was configured with dependencies to dictate its execution order. For example, data extraction tasks were scheduled to run before data transformation tasks to ensure that the necessary input data was available.

**Scheduling**:

The DAG was scheduled to run periodically, fetching new data at regular intervals. This scheduling mechanism ensured that the dataset remained up-to-date, reflecting the latest news articles from Dawn.com and BBC.com.

### Challenges Faced

**Compatibility with Windows**:

One notable challenge encountered was the compatibility of Apache Airflow with Windows operating systems. 

**Error Handling**:

Another challenge was implementing robust error handling mechanisms within the DAG. This involved anticipating and addressing potential failure points, such as network errors during data extraction or formatting issues during data transformation.

**Performance Optimization**:

Optimizing the performance of the data extraction process was an ongoing concern. Efforts were made to minimize latency and resource usage, particularly when fetching data from remote servers such as Dawn.com and BBC.com.

### Conclusion

In conclusion, the assignment involved a comprehensive approach to news data extraction, transformation, and automation. By leveraging tools such as BeautifulSoup, Google Drive, DVC, and Apache Airflow, a robust workflow was developed to gather, process, and store news articles from multiple sources. Despite encountering challenges such as compatibility issues and error handling complexities, the project demonstrated effective utilization of various technologies to achieve its objectives.

