pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'
        EC2_HOST = '43.204.97.161'
        SSH_KEY = 'VENSNR01.pem'  // Make sure this matches Jenkins credentials
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/venkyredd/python-app'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Application Locally') {
            steps {
                sh 'nohup python3 app.py &'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['VENSNR01.pem']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST << EOF
                    # Ensure the project directory exists
                    mkdir -p /home/ubuntu/python-app
                    cd /home/ubuntu/python-app
                    
                    # Clone repo if not already present
                    if [ ! -d .git ]; then
                        git clone your-repo-url .
                    else
                        git pull origin main
                    fi

                    # Install dependencies
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    
                    # Kill the previous process (if running)
                    pkill -f app.py || true

                    # Start the application
                    nohup python3 app.py > app.log 2>&1 &
                    EOF
                    """
                }
            }
        }
    }
}
