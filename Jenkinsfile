pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root --shm-size=2g'
        }
    }
    environment { DISPLAY=":99" }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install System Dependencies') {
            steps {
                sh '''
                  apt-get update && apt-get install -y wget unzip curl gnupg xvfb fonts-liberation                     libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2                     libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1                     libxdamage1 libxrandr2 xdg-utils libu2f-udev libvulkan1 libgbm1 libgtk-3-0
                  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
                  echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
                  apt-get update && apt-get install -y google-chrome-stable
                  CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
                  DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
                  wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip"
                  unzip /tmp/chromedriver.zip -d /usr/local/bin
                  chmod +x /usr/local/bin/chromedriver
                '''
            }
        }
        stage('Install Python Dependencies') { steps { sh 'pip install --upgrade pip && pip install -r requirements.txt' } }
        stage('Run Tests') {
            steps { sh 'xvfb-run pytest -v --maxfail=1 --disable-warnings --html=report.html --self-contained-html' }
        }
        stage('Archive Reports & Screenshots') {
            steps {
                archiveArtifacts artifacts: 'report.html', fingerprint: true
                archiveArtifacts artifacts: 'utils/screenshots/error_screenshots/**/*', allowEmptyArchive: true
            }
        }
    }
    post { always { junit '**/test-results.xml' } }
}
