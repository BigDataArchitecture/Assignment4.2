# Assignment4.2

In this assignment we have done 4 things

1) Implemented AIRFLOW for making cache files
2) Implemented JWT tokens for verification of our API and Webapp
3) Implemented Cache Logic function to get payloads faster
4) Tried to learn parallel processing!


**Logic Architecture Diagram**
<img align="left" alt="GIF" src="https://github.com/BigDataArchitecture/Assignment4.2/blob/main/Images/architecture.drawio%20(1).png" width="980" height="400" />
<br>



**1) Airflow Implementation**

Apache Airflow is an open-source tool to programmatically author, schedule, and monitor workflows. 

To install airflow, follow following steps:

1) Make sure you have conda installed
conda create -n airflow python=3.7
conda activate airflow

```
pip install -U apache-airflow
```
```
mkdir -p ~/airflow/dags
```
```
export AIRFLOW_HOME='~/airflow'
```
```
export PATH=$PATH:~/.local/bin
```
```
cd ~/airflow
```
```
airflow d binit
```
```
airflow scheduler
```

Once all installation is done put the dag file in airflow/dags folder and it will be sceduled it.

Note: Below is our airflow image running for 3 days every hour
<img align="left" alt="GIF" src="https://github.com/BigDataArchitecture/Assignment4.2/blob/main/Images/AIrlfow.png" width="980" height="400" />


**WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK**

Contribution:
Parth: 50%
Sree: 25%
Ankana: 25%
