git add .
git commit -m "$1"
git push origin 
docker build -t palondomus/amarimovieswishlist:latest .
docker push palondomus/amarimovieswishlist:latest
docker run -it -p 8080:8080 palondomus/amarimovieswishlist:latest