# TECHNICAL TEST : E-COMMERCE DATA PIPELINE

You were recently hired by an E-commerce company as a Data Engineer. Your mission is to build a simple but modern data pipeline to analyze sales performance using the provided datasets.

## **Datasets**
* **Products**: Available product catalog (`data/products.csv`)
* **Items**: Individual line items (`data/items.csv`)
* **Orders**: Customer transaction records (`data/orders.csv`)
* **Customers**: Customer master data (`data/customer.csv`)

##  **Requirements**

You will use **Python** as the main programming language. 

It is possible to use containerized tools if considered useful.


### **Core Tasks**

1. **Data Processing Setup**
   - Choose a modern data processing tool (e.g. DuckDB, Polars, Pandas or any other)
   - Load and explore the four datasets
   - Document any data quality issues you find

2. **Data Modeling & Transformation**
   - Create a simple data model joining all datasets
   - Build daily customer summary metrics:
     - Daily spending per customer
     - Number of orders per customer per day
     - Average order value
   - Implement this as reusable code/functions

3. **Production grade code**
   - Apply software engineering best practices for maintainable, scalable code

### **Optional Enhancements (if time permits)**

- Simple visualization of key metrics
- Basic data validation checks
- Export results to a structured format (JSON/Parquet)
- To automate this and make it run every day
- To bring it in a "Infra-as-Code" way
- Anything you want to show


## **Evaluation Focus**

- **Code Quality**: Clean, readable, well-structured code
- **Data Engineering Thinking**: Proper data handling and transformation logic
- **Problem Solving**: How you approach and solve the business questions
- **Documentation**: Clear explanations and instructions
- **Modern Practices**: Use of appropriate tools and containerization

---


**Note**: Focus on demonstrating your data engineering thought process rather than building production-scale infrastructure. Quality over complexity!