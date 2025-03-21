pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'
        EC2_HOST = '43.204.97.161'
        SSH_CREDENTIAL_ID = 'fa7b8283-1216-4a7e-8b09-3bcc2366ace5'
        VENV_PATH = '.venv'  // Virtual environment path
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/venkyredd/python-app'
            }
        }

        stage('Setup Virtual Environment & Install Dependencies') {
            steps {
                sh """
                python3 -m venv $VENV_PATH  # Create a virtual environment
                . $VENV_PATH/bin/activate  # Activate the virtual environment
                pip install --upgrade pip  # Upgrade pip
                pip install -r requirements.txt  # Install dependencies
                deactivate  # Deactivate after installation
                """
            }
        }

        stage('Run Application Locally') {
            steps {
                sh """
                . $VENV_PATH/bin/activate
                nohup python3 app.py > app.log 2>&1 &
                deactivate
                """
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([SSH_CREDENTIAL_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST << 'EOF'
                    set -e  # Exit on error

                    # Ensure project directory exists
                    mkdir -p /home/ubuntu/python-app
                    cd /home/ubuntu/python-app

                    # Clone repo if not already present, otherwise pull latest changes
                    if [ ! -d .git ]; then
                        git clone https://github.com/venkyredd/python-app .
                    else
                        git reset --hard
                        git pull origin main
                    fi

                    # Setup virtual environment and install dependencies
                    python3 -m venv $VENV_PATH
                    . $VENV_PATH/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    deactivate

                    # Kill any existing process running on port 5000 (assuming Flask app)
                    pkill -f "python3 app.py" || true

                    # Start the application
                    . $VENV_PATH/bin/activate
                    nohup python3 app.py > app.log 2>&1 &
                    deactivate
                    EOF
                    """
                }
            }
        }
    }
}
