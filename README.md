# stockapp

Installing:
  Install / Update pip
    sudo apt-get install python3-pip
    pip3 install -U pip
  
  Install Flask
    pip3 install --upgrade flask
    
  Clone repo
    git clone <repo>
    
  Run application
    cd stockapp
    export FLASK_APP=stockapp
    export FLASK_DEBUG=true
    flask run --host=0.0.0.0  # < makes server listen to all addresses, not just localhost.  On port 5000
