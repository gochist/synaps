library identifier: 'custom-lib@master', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/gochist/jenkinslib.git',
   credentialsId: 'github'])

pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_TO', choices: ['dev9', 'dev'],
               description: '배포할 대상 선택')
    }

    stages {
        stage('Build') {
            steps {
//                 script {
//                     echo test.readjson()
//                 }
//                 echo test.readfile
                echo 'Building..'

                test name: "test"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
