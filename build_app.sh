git add .
git commit -m "$1"
git push origin 
docker build -t palondomus/amarimovieswishlist:5 .
docker push palondomus/amarimovieswishlist:5
docker run -it -p 8080:8080 palondomus/amarimovieswishlist:5