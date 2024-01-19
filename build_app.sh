git add .
git commit -m "$1"
git push origin 
docker build -t palondomus/caesaraifastapi:latest .
docker push palondomus/caesaraifastapi:latest
docker run -it -p 8080:8080 palondomus/caesaraifastapi:latest