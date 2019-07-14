### A framework for programmable Grafana dashboard generation

- Uses Jinja2 templates
- Define your metrics and data for monitoring in a file(s).
- Trigger program to generate substituted dashboard JSON.
- Push dashboards to Grafana.
 
- Currently supports CloudWatch datasource dashboards

- A parent/child relationship is supported.
- A parent is a collection of unique-identifiers, that can define your monitoring environment. 
- Can define multiple parents and children.


### Layout
- The dashboards are for individual metrics and are laid out in uniform rows.

### Templates
- AWS CloudWatch datasource backed dashboards for a few services and metrics
- Graphite datasource backed dashboards

### Pre-requisites
- Generate an API key from the instance where Grafana is running. 
- Create a folder in Grafana, where you would like to upload files into Grafana

### Generate Dashboards
```
#!/bin/bash
parent=$1
child=$2
grafana_folder_name=$3
python dashboard_generator.py $parent $child $grafana_folder_name
```

# Upload Dashboards
```
python push_dashboard.py $parent $output_json_file_name $grafana_folder_name $grafana_api_token $grafana_base_url
```
