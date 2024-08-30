# ba_supplementary
Here supplementary files (like starter files for the AI-modules) for my bachelor thesis can be found. Although the setup of `starter.py` and other files is originally intended for the AI-tools from the `bimkit-demo-text` project by Phillip Schönfelder, with minor alterations it can be suited to work with other projects as well.

**Backend:** https://github.com/ghjez/ba_backend  
**Frontend:** https://github.com/ghjez/ba_frontend  

Starter script
---
The `starter.py` script provides the handling of inputs and outputs via HTTP-requests for containerized processing modules. To incorporate the script into the existing project:
1. Install Flask if your project does not use it already.
2. Add the `starter.py` file to the `src` folder (or any folder you deem suitable).
3. Provide paths to the upload and output folders: 
```python
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/outputData'
```
4. If other project than `bimkit-demo-text`is used, call your processing function here :
```python
processed_data = your_processing_function(...)
```

Dockerfile setup
---
1. Comment out the following lines:
```python
# COPY --from="default-route-openshift-image-registry.apps.k8s.nt.ag/bimkit-ntag-portal/bimkit-starter:latest" /app .
# RUN pip3 install -r requirements.txt
```
2. Make sure the Dockerfile has these commands (among others of course):
```Dockerfile
# setup file structure
RUN mkdir -p /tmp/outputData/final/original/
RUN mkdir -p /tmp/outputData/final/visual/
RUN mkdir -p /tmp/outputData/cache/
RUN mkdir -p /tmp/outputData/zipcache/
RUN mkdir -p /app/uploads/

# handle user privileges
RUN chmod -R 777 /app
RUN chmod -R 777 /tmp
```

Alternatively, if your project's file structure differs significantly, adjust the paths in the `starter.py` and set the user privileges accordingly.

`app.py` setup
---
When clearing folders before processing:
1. In `folders[]` comment out 
```python 
#"/app/uploads/*",
```
2. Clear the uploads folder *after* the processing (don't forget the square brackets).
```python
clear_folders(["/app/uploads/*"])
```
If you are working with a different project, the rule of thumb for clearing folders is:
1. Before the processing, clear all folders ___except___ the upload/input folder. 
2. After the processing clear the upload/input folder.

Running the containers
---
It is important to run the containers in the "detached" mode (`-d` flag) and bind the ports properly.
```python
# starter.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port={your_port}) # Port here
```
```bash
docker build -t {name} . --network=host
docker run -d -p {your_port}:{your_port} {name}:latest 
                # Should be the same here
```
You can of course run the containers from the CLI every time. However, using the Docker Desktop dashboard will make the management of multiple containers easier.
