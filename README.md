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
    sudo apt-get install -y libopenjp2-7-dev
    sudo apt-get install -y libhdf5-dev
    sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test
    sudo apt-get install -y libatlas-base-dev
    sudo apt-get install -y libjasper-dev
    sudo apt-get install -y python3-pip
    sudo apt-get install -y python3-h5py
    sudo apt-get install -y python3-opencv
    sudo pip3 install flask
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