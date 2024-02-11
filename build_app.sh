git add .
git commit -m "$1"
git push origin 
docker build -t palondomus/amarimovieswishlist:bestest .
docker push palondomus/amarimovieswishlist:bestest
docker run -it -p 8080:8080 palondomus/amarimovieswishlist:bestest