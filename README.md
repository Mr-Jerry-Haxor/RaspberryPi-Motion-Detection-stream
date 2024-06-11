# RaspberryPi-MachineLearning

## Essential Libraries to Install
To set up the project, you need to install several libraries. Run the following commands in your terminal:

1. Clone the repository:
    ```
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```
    cd RaspberryPi-MachineLearning
    ```

3. Install the required libraries:
    ```
    sudo apt-get install -y libopenjp2-7-dev libhdf5-dev libqtgui4 libqtwebkit4 libqt4-test libatlas-base-dev libjasper-dev python3-pip python3-h5py python3-opencv
    ```

4. Install the Python dependencies:
    ```
    sudo pip3 install -r requirements.txt
    ```

## Accessing the Application
Open your browser and type the following URL:


```
http://ip-address:5000
```


### Known Issues
If you encounter any issues while installing libraries like python3-opencv or flask, run the following command to update your package lists and fix any missing package dependencies:

```
sudo apt-get update --fix-missing
```